/**
 * SchoolHUB — Navigation with animated transitions
 * Sliding blue indicator + page content slide+fade, always in sync
 */

(function () {
  const DURATION = 520; // ms — must match CSS --duration
  const SLIDE_OFFSET = 70; // px — how far content slides during exit/enter

  const pillWrapper = document.getElementById('pillWrapper');
  const indicator   = document.getElementById('navIndicator');
  const appContent  = document.getElementById('appContent');
  const pageContent = document.getElementById('page-content');

  if (!pillWrapper || !indicator || !pageContent) return;

  // ── Collect all nav links ──────────────────────────────────────────────────
  const links = Array.from(pillWrapper.querySelectorAll('.nav-link'));

  // ── Find index of currently active link ───────────────────────────────────
  function getActiveIndex() {
    const active = pillWrapper.querySelector('.nav-link.active');
    return active ? links.indexOf(active) : 0;
  }

  let currentIndex = getActiveIndex();
  let animating = false;

  // ── Position indicator under a given link element ─────────────────────────
  function positionIndicator(linkEl) {
    if (!linkEl) return;
    const wrapRect = pillWrapper.getBoundingClientRect();
    const linkRect = linkEl.getBoundingClientRect();
    indicator.style.left  = (linkRect.left - wrapRect.left) + 'px';
    indicator.style.width = linkRect.width + 'px';
  }

  // Set initial position instantly (no transition on load)
  indicator.style.transition = 'none';
  positionIndicator(links[currentIndex]);
  // Re-enable transition after one frame
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      indicator.style.transition = '';
    });
  });

  // ── Reposition on resize ───────────────────────────────────────────────────
  window.addEventListener('resize', () => {
    indicator.style.transition = 'none';
    positionIndicator(links[currentIndex]);
    requestAnimationFrame(() => {
      requestAnimationFrame(() => { indicator.style.transition = ''; });
    });
  });

  // ── Animate page content out ───────────────────────────────────────────────
  function exitPage(direction) {
    return new Promise(resolve => {
      const half = DURATION / 2;
      pageContent.style.transition = `transform ${half}ms cubic-bezier(0.77,0,0.175,1), opacity ${half}ms ease`;
      pageContent.style.transform  = `translateX(${direction * -SLIDE_OFFSET}px)`;
      pageContent.style.opacity    = '0';
      setTimeout(resolve, half);
    });
  }

  // ── Animate page content in ────────────────────────────────────────────────
  function enterPage(direction) {
    const half = DURATION / 2;
    pageContent.style.transition = 'none';
    pageContent.style.transform  = `translateX(${direction * SLIDE_OFFSET}px)`;
    pageContent.style.opacity    = '0';

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        pageContent.style.transition = `transform ${half}ms cubic-bezier(0.77,0,0.175,1), opacity ${half}ms ease`;
        pageContent.style.transform  = 'translateX(0)';
        pageContent.style.opacity    = '1';
      });
    });
  }

  // ── Fetch new page and extract #page-content HTML ─────────────────────────
  async function fetchPage(url) {
    const res  = await fetch(url, { headers: { 'X-Requested-With': 'SchoolHUBNav' } });
    const text = await res.text();
    const parser = new DOMParser();
    const doc  = parser.parseFromString(text, 'text/html');

    // Extract inner content
    const newContent = doc.getElementById('page-content');
    const newTitle   = doc.title;
    return {
      html:  newContent ? newContent.innerHTML : '',
      title: newTitle,
    };
  }

  // ── Main navigation handler ────────────────────────────────────────────────
  async function navigateTo(linkEl, targetIndex) {
    if (animating || targetIndex === currentIndex) return;
    animating = true;

    // Direction: +1 = going right (slide left), -1 = going left (slide right)
    const direction = targetIndex > currentIndex ? 1 : -1;

    // Update active state immediately
    links.forEach(l => l.classList.remove('active'));
    linkEl.classList.add('active');

    // START both animations simultaneously
    positionIndicator(linkEl);           // indicator slides
    appContent.classList.add('nav-animating');  // blur overlay
    exitPage(direction);                 // content exits

    const url = linkEl.getAttribute('href');

    // Fetch while exit animation plays
    let fetched;
    try {
      fetched = await fetchPage(url);
    } catch (e) {
      // On error — fall back to normal navigation
      window.location.href = url;
      return;
    }

    // Wait for exit animation to finish
    await new Promise(r => setTimeout(r, DURATION / 2));

    // Inject new content
    pageContent.innerHTML = fetched.html;
    document.title = fetched.title;
    history.pushState({ index: targetIndex, url }, '', url);

    // Enter animation
    enterPage(direction);

    // Re-run any inline scripts in the new content
    pageContent.querySelectorAll('script').forEach(oldScript => {
      const s = document.createElement('script');
      s.textContent = oldScript.textContent;
      oldScript.replaceWith(s);
    });

    currentIndex = targetIndex;

    // Remove blur after full duration
    setTimeout(() => {
      appContent.classList.remove('nav-animating');
      animating = false;
    }, DURATION / 2 + 80);
  }

  // ── Intercept link clicks ──────────────────────────────────────────────────
  links.forEach((link, idx) => {
    link.addEventListener('click', e => {
      const href = link.getAttribute('href');
      // Skip logout, external, hash-only links
      if (!href || href.startsWith('#') || href.includes('logout')) return;
      e.preventDefault();
      navigateTo(link, idx);
    });
  });

  // ── Browser back/forward ───────────────────────────────────────────────────
  window.addEventListener('popstate', async (e) => {
    if (animating) return;
    const state = e.state;
    const targetUrl = state?.url || window.location.pathname;
    const targetIndex = state?.index ?? 0;

    const matchingLink = links.find(l => l.getAttribute('href') === targetUrl) || links[targetIndex];
    if (!matchingLink) return;

    animating = true;
    const direction = targetIndex > currentIndex ? 1 : -1;

    links.forEach(l => l.classList.remove('active'));
    matchingLink.classList.add('active');
    positionIndicator(matchingLink);
    appContent.classList.add('nav-animating');
    exitPage(direction);

    let fetched;
    try { fetched = await fetchPage(targetUrl); }
    catch { window.location.reload(); return; }

    await new Promise(r => setTimeout(r, DURATION / 2));
    pageContent.innerHTML = fetched.html;
    document.title = fetched.title;
    enterPage(direction);

    currentIndex = targetIndex;
    setTimeout(() => {
      appContent.classList.remove('nav-animating');
      animating = false;
    }, DURATION / 2 + 80);
  });

  // Push initial state so popstate works on first navigation
  history.replaceState({ index: currentIndex, url: window.location.pathname }, '', window.location.pathname);

})();
// Melian site: parallax, the pinned story, the live phone and scroll reveals.
// No libraries. One rAF loop reads scroll once per frame and writes transforms only.
(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(pointer: fine)").matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const lang = document.documentElement.lang || "en";
  const T = window.MELIAN_STRINGS || {};

  // ---------- Reveal on scroll ----------
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  }, { rootMargin: "0px 0px -12% 0px" });
  $$(".reveal").forEach((el) => io.observe(el));

  // ---------- Nav hides on scroll down, returns on scroll up ----------
  const nav = $(".nav");
  let lastY = scrollY;

  // ---------- Stars around the hero phone ----------
  const stars = $(".stars");
  if (stars) {
    const spots = [[8, 12], [86, 8], [92, 46], [4, 58], [78, 84], [18, 90], [50, -2], [100, 70]];
    spots.forEach(([x, y], i) => {
      const b = document.createElement("b");
      b.style.left = x + "%"; b.style.top = y + "%";
      b.style.animationDelay = (i * 0.6) + "s";
      const s = 0.5 + ((i * 37) % 10) / 12;
      b.style.scale = s;
      b.dataset.depth = (0.15 + s * 0.35).toFixed(2);
      stars.appendChild(b);
    });
  }

  // ---------- Live phone: ticking timer, real buttons ----------
  const pad = (n) => String(n).padStart(2, "0");
  const fmtClock = (d) => d.toLocaleTimeString(lang === "it" ? "it-IT" : "en-GB", { hour: "2-digit", minute: "2-digit" });
  const fmtSince = (ms) => {
    const m = Math.max(0, Math.floor(ms / 60000));
    return m < 60 ? `${m}m` : `${Math.floor(m / 60)}h ${pad(m % 60)}m`;
  };
  const kinds = {
    feed: { color: "var(--feed)", icon: "●", label: T.feedRow || "Feed · 110 ml" },
    wet: { color: "var(--wet)", icon: "●", label: T.wetRow || "Wet nappy" },
    dirty: { color: "var(--dirty)", icon: "●", label: T.dirtyRow || "Dirty nappy" },
    both: { color: "var(--both)", icon: "●", label: T.bothRow || "Wet & dirty" },
  };
  const INTERVAL = 3 * 3600 * 1000;

  $$(".phone[data-live]").forEach((phone) => {
    let lastFeed = Date.now() - (100 * 60 * 1000); // 1h 40m ago, like the store screenshot
    const counts = { formula: 840, feeds: 8, wet: 4, dirty: 5 };
    const goals = { formula: 900, feeds: 9, wet: 6, dirty: 0 };
    const time = $(".ring strong", phone);
    const next = $(".ring em", phone);
    const bar = $(".ring .bar", phone);
    const C = 2 * Math.PI * 46;
    if (bar) { bar.style.strokeDasharray = C; }
    const islandT = $(".island .t", phone);

    const minis = {};
    $$(".mini", phone).forEach((m) => { minis[m.dataset.k] = m; });
    const paintMinis = () => {
      for (const k in minis) {
        const m = minis[k];
        $("strong", m).textContent = counts[k];
        const b = $(".b", m);
        const c = 2 * Math.PI * 15;
        b.style.strokeDasharray = c;
        const frac = goals[k] ? Math.min(1, counts[k] / goals[k]) : 0.0001;
        b.style.strokeDashoffset = c * (1 - frac);
      }
    };

    const tick = () => {
      const since = Date.now() - lastFeed;
      if (time) time.textContent = fmtSince(since);
      if (next) next.textContent = (T.next || "next") + " ~" + fmtClock(new Date(lastFeed + INTERVAL));
      if (bar) bar.style.strokeDashoffset = C * (1 - Math.min(1, since / INTERVAL));
      if (islandT) islandT.textContent = fmtSince(since);
    };

    const list = $(".timeline ul", phone);
    const add = (kind, at = new Date(), fresh = true) => {
      if (!list) return;
      const k = kinds[kind];
      const li = document.createElement("li");
      if (fresh) li.className = "new";
      li.innerHTML = `<time>${fmtClock(at)}</time><i style="background:${k.color}">${k.icon}</i><span>${k.label}</span>`;
      list.prepend(li);
      while (list.children.length > 3) list.lastElementChild.remove();
    };

    // seed the timeline with a believable evening
    const now = Date.now();
    add("feed", new Date(now - 100 * 60000 - 3 * 3600000), false);
    add("wet", new Date(now - 130 * 60000), false);
    add("feed", new Date(lastFeed), false);

    $$(".act", phone).forEach((btn) => {
      btn.addEventListener("click", (ev) => {
        const kind = btn.dataset.kind;
        const r = btn.getBoundingClientRect();
        const dot = document.createElement("span");
        const size = Math.max(r.width, r.height) / 2;
        dot.className = "ripple";
        dot.style.width = dot.style.height = size + "px";
        dot.style.left = ((ev.clientX || r.left + r.width / 2) - r.left - size / 2) + "px";
        dot.style.top = ((ev.clientY || r.top + r.height / 2) - r.top - size / 2) + "px";
        btn.appendChild(dot);
        setTimeout(() => dot.remove(), 700);
        if (kind === "feed") { lastFeed = Date.now(); counts.feeds++; counts.formula += 110; }
        if (kind === "wet" || kind === "both") counts.wet++;
        if (kind === "dirty" || kind === "both") counts.dirty++;
        add(kind);
        paintMinis(); tick();
        if (navigator.vibrate) navigator.vibrate(8);
      });
    });

    paintMinis(); tick();
    setInterval(tick, 1000 * 20);
    phone.classList.add("live");
  });

  // ---------- Tilt the hero phone toward the pointer ----------
  const heroPhone = $(".hero .phone");
  let tiltX = 0, tiltY = 0, tx = 0, ty = 0;
  if (heroPhone && fine && !reduce) {
    addEventListener("pointermove", (e) => {
      tx = (e.clientX / innerWidth - 0.5) * 2;
      ty = (e.clientY / innerHeight - 0.5) * 2;
    }, { passive: true });
  }

  // ---------- Statement rows slide sideways ----------
  const rows = $$(".statement .row");
  // ---------- Words of the maker note light up as you read ----------
  const quote = $(".note blockquote");
  let words = [];
  if (quote) {
    quote.innerHTML = quote.textContent.trim().split(/\s+/).map((w) => `<span class="w">${w}</span>`).join(" ");
    words = $$(".w", quote);
  }

  // ---------- Story ----------
  const story = $(".story");
  const chapters = story ? $$(".chapter", story) : [];
  const bars = story ? $$(".progress i", story) : [];

  const depthEls = $$("[data-depth]");

  const frame = () => {
    const y = scrollY;
    const vh = innerHeight;

    if (nav) {
      if (y > lastY + 6 && y > 200) nav.classList.add("hide");
      else if (y < lastY - 6) nav.classList.remove("hide");
    }
    lastY = y;

    if (!reduce) {
      for (const el of depthEls) {
        const d = parseFloat(el.dataset.depth);
        el.style.transform = `translate3d(0, ${(-y * d).toFixed(1)}px, 0)`;
      }
      if (heroPhone) {
        tiltX += (tx - tiltX) * 0.08; tiltY += (ty - tiltY) * 0.08;
        const lift = Math.min(y, vh) * 0.12;
        heroPhone.style.transform = `translateY(${lift.toFixed(1)}px) rotateY(${(tiltX * 10).toFixed(2)}deg) rotateX(${(-tiltY * 8 + 4).toFixed(2)}deg) rotateZ(${(tiltX * -1.5).toFixed(2)}deg)`;
        heroPhone.style.setProperty("--lx", (50 + tiltX * 40) + "%");
        heroPhone.style.setProperty("--ly", (tiltY * 30) + "%");
      }
      for (const [i, row] of rows.entries()) {
        const r = row.getBoundingClientRect();
        const p = (r.top - vh) / (vh + r.height);
        row.style.transform = `translate3d(${((i % 2 ? -1 : 1) * p * 30).toFixed(2)}%, 0, 0)`;
      }
    }

    if (story) {
      const r = story.getBoundingClientRect();
      const total = r.height - vh;
      const p = Math.min(1, Math.max(0, -r.top / total));
      const n = chapters.length;
      const step = Math.min(n, Math.floor(p * n) + 1);
      if (story.dataset.step !== String(step)) {
        story.dataset.step = step;
        chapters.forEach((c, i) => c.classList.toggle("on", i === step - 1));
      }
      bars.forEach((b, i) => b.style.setProperty("--p", Math.min(1, Math.max(0, p * n - i)).toFixed(3)));
    }

    if (words.length) {
      const r = quote.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
      const lit = Math.round(p * words.length);
      words.forEach((w, i) => w.classList.toggle("lit", i < lit || reduce));
    }

    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
})();

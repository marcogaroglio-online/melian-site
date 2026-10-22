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

  // ---------- Live phones ----------
  // The demo runs on a pretend evening that starts at 21:41 today (the status bar's 9:41) and moves with
  // real time. The story's two phones share one day, so a tap on one shows up on the other.
  const MIN = 60000;
  const INTERVAL = 180 * MIN;
  const L = lang === "it" ? "it-IT" : "en-US";
  const loadAt = Date.now();
  const evening = new Date(); evening.setHours(21, 41, 0, 0);
  const simNow = () => new Date(evening.getTime() + (Date.now() - loadAt));
  const at = (base, minutes) => new Date(base.getTime() + minutes * MIN);
  const clock = (d) => d.toLocaleTimeString(L, { hour: "numeric", minute: "2-digit" });
  const clockHTML = (d) => clock(d).replace(/[\s ]?(AM|PM)$/, "<small> $1</small>");
  const bareClock = (d) => clock(d).replace(/[\s ]?(AM|PM)$/, "");
  const span = (ms) => {
    const m = Math.max(0, Math.floor(ms / MIN));
    return m < 60 ? `${m}m` : `${Math.floor(m / 60)}h ${m % 60}m`;
  };
  const spell = (ms) => {
    const m = Math.max(0, Math.ceil(ms / MIN)), h = Math.floor(m / 60), r = m % 60;
    const unit = (n, [one, many]) => `${n} ${n === 1 ? one : many}`;
    return [h && unit(h, T.hour || ["hour", "hours"]), (r || !h) && unit(r, T.minute || ["minute", "minutes"])].filter(Boolean).join(", ");
  };
  const fill = (circle, frac) => {
    if (!circle) return;
    const c = 2 * Math.PI * circle.r.baseVal.value;
    circle.style.strokeDasharray = c;
    circle.style.strokeDashoffset = c * (1 - Math.max(0, Math.min(1, frac)));
  };
  const icons = {};
  const iconFrom = (sel, k) => { const el = $(sel + " svg"); if (el && !icons[k]) icons[k] = el.outerHTML; };

  class Day {
    constructor() {
      const now = simNow();
      this.first = at(now, -100);
      this.lastFeed = this.first;
      this.counts = { formula: 840, feeds: 8, wet: 4, dirty: 5 };
      this.events = [
        { kind: "dirty", at: at(this.first, 17) },
        { kind: "feed", at: this.first, ml: 110, gap: 177 * MIN },
        { kind: "wet", at: at(this.first, -163) },
        { kind: "feed", at: at(this.first, -177), ml: 120, gap: 165 * MIN },
      ];
      this.views = [];
    }
    log(kind) {
      const now = simNow();
      if (kind === "feed") {
        this.events.unshift({ kind, at: now, ml: 110, gap: now - this.lastFeed, fresh: true });
        this.lastFeed = now; this.counts.feeds++; this.counts.formula += 110;
      } else {
        this.events.unshift({ kind, at: now, fresh: true });
        if (kind !== "dirty") this.counts.wet++;
        if (kind !== "wet") this.counts.dirty++;
      }
      this.views.forEach((v) => v());
      this.events[0].fresh = false;
    }
  }

  const label = (e) => ({ feed: (T.feed_row || "Feed · {} ml").replace("{}", e.ml), wet: T.wet_row, dirty: T.dirty_row, both: T.both_row })[e.kind];

  const mount = (phone, day) => {
    iconFrom(".phone .act.feed", "feed"); iconFrom(".phone .act.wet", "wet");
    iconFrom(".phone .act.dirty", "dirty"); iconFrom(".phone .act.both", "both");
    const minis = $$(".mini", phone);
    const list = $(".tl", phone);
    const render = () => {
      const now = simNow();
      const next = new Date(day.lastFeed.getTime() + INTERVAL);
      const since = now - day.lastFeed;
      const frac = since / INTERVAL;
      $$("[data-clock]", phone).forEach((el) => { el.textContent = bareClock(now); });
      const set = (sel, text) => $$(sel, phone).forEach((el) => { el.textContent = text; });
      set("[data-since]", span(since));
      set("[data-nextline]", (T.next || "next ~{}").replace("{}", clock(next)));
      set("[data-next]", clock(next));
      set("[data-countdown]", spell(next - now));
      set("[data-around]", (T.la_around || "around {}").replace("{}", clock(next)));
      fill($(".bring .bar", phone), frac);
      fill($(".isl .bar", phone), frac);
      fill($(".la-ring .bar", phone), frac);
      for (const m of minis) {
        const n = day.counts[m.dataset.k], goal = +m.dataset.goal || 0;
        $("strong", m).textContent = n;
        m.classList.toggle("done", goal > 0 && n >= goal);
        fill($(".mring .bar", m), goal ? n / goal : 0);
      }
      if (list) {
        list.innerHTML = day.events.slice(0, 4).map((e) =>
          `<li${e.fresh ? ' class="new"' : ""}><time>${clockHTML(e.at)}</time><i class="dot k-${e.kind}">${icons[e.kind] || ""}</i>` +
          `<span class="what">${label(e)}</span><em class="gap">${e.gap ? span(e.gap) : ""}</em></li>`).join("");
      }
    };
    // static parts of the Lock Screen and Days layers
    $$("[data-date]", phone).forEach((el) => {
      el.textContent = simNow().toLocaleDateString(lang === "it" ? "it-IT" : "en-GB", { weekday: "long", day: "numeric", month: "long" });
    });
    $$("[data-day]", phone).forEach((el) => {
      el.textContent = simNow().toLocaleDateString(L, { day: "numeric", month: "short", year: "numeric" });
    });
    $$("[data-at]", phone).forEach((el) => { el.innerHTML = clockHTML(at(day.first, +el.dataset.at)); });
    const dayFrac = { formula: 1, feeds: 1, wet: 4 / 6, dirty: 0 };
    $$(".d-row", phone).forEach((r) => fill($(".dr .bar", r), dayFrac[r.dataset.k]));

    $$(".act", phone).forEach((btn) => {
      btn.addEventListener("click", (ev) => {
        const r = btn.getBoundingClientRect();
        const dot = document.createElement("span");
        const size = Math.max(r.width, r.height) / 2;
        dot.className = "ripple";
        dot.style.width = dot.style.height = size + "px";
        dot.style.left = ((ev.clientX || r.left + r.width / 2) - r.left - size / 2) + "px";
        dot.style.top = ((ev.clientY || r.top + r.height / 2) - r.top - size / 2) + "px";
        btn.appendChild(dot);
        setTimeout(() => dot.remove(), 700);
        day.log(btn.dataset.kind);
        if (navigator.vibrate) navigator.vibrate(8);
      });
    });
    day.views.push(render);
    render();
    setInterval(render, 15000);
    phone.classList.add("live");
  };

  const heroDay = new Day(), storyDay = new Day();
  $$(".phone[data-live]").forEach((phone) => mount(phone, phone.closest(".story") ? storyDay : heroDay));

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
  // On phones the story stacks: size the phone to the room left above the chapter text.
  const stacked = matchMedia("(max-width: 900px)");
  const fitStory = () => {
    if (!story) return;
    if (!stacked.matches) { story.style.removeProperty("--fit"); return; }
    const room = $(".phones", story).clientHeight;
    story.style.setProperty("--fit", Math.max(.3, Math.min(.62, (room - 12) / 691)).toFixed(3));
  };
  fitStory();
  addEventListener("resize", fitStory);
  stacked.addEventListener("change", fitStory);

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

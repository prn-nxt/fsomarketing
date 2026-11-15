# Images — how to add real photography

The site's main visuals are **custom inline SVG/CSS** (the score gauge, the Four Bucket diagram, the
certificate mock, backgrounds). They load instantly, never break, and match the FSO brand — so the
site needs **no external images to look complete**.

If you'd like to add real photography (e.g. business owners, advisors, meetings), here's the safe way.

## 1. Get free, license-clear photos
Use **Unsplash** (unsplash.com), **Pexels** (pexels.com) or **Pixabay** (pixabay.com). All allow
free commercial use. Good search terms for FSO:
`small business owner india`, `finance meeting`, `accountant advisor`, `factory SME`,
`business handshake`, `financial dashboard`.

## 2. Optimise before uploading
- Resize to the size actually shown (≤ 1200px wide is plenty for these sections).
- Export as **WebP** (best) or JPEG at ~70–80% quality.
- Save into this `assets/img/` folder, e.g. `owner-portrait.webp`.

## 3. Drop it into a media slot
Find a `<div class="media-frame">…</div>` in the HTML (e.g. on `about.html` or `certification.html`).
Replace the inline `<svg>` with:

```html
<div class="media-frame is-photo">
  <img src="assets/img/owner-portrait.webp" width="1200" height="900"
       alt="Business owner reviewing their FSO scorecard" loading="lazy" decoding="async">
</div>
```

- Always set `width`/`height` (prevents layout shift → better Core Web Vitals).
- Always write a descriptive `alt` (accessibility + SEO).
- Keep `loading="lazy"` for below-the-fold images.
- The `.media-frame` has a branded gradient behind the image, so even if a photo ever fails to load,
  the panel still looks intentional — never a broken-image icon.

## 4. Attribution
Unsplash/Pexels don't legally require credit, but it's courteous. Keep a note here of any photos used:

| File | Source | Photographer | URL |
|------|--------|--------------|-----|
| _example.webp_ | Unsplash | _name_ | _link_ |

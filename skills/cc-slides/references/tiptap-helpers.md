# Tiptap JSON Helpers Reference

These helper functions produce valid Tiptap JSONContent for the `contentJson` field of slidesV3 documents.

## Document Structure

```typescript
function makeDoc(blocks: any[]) {
  return { type: "doc", content: blocks };
}
```

## Headings

```typescript
function h1(text: string) {
  return { type: "heading", attrs: { level: 1 }, content: [{ type: "text", text }] };
}
function h2(text: string) {
  return { type: "heading", attrs: { level: 2 }, content: [{ type: "text", text }] };
}
function h3(text: string) {
  return { type: "heading", attrs: { level: 3 }, content: [{ type: "text", text }] };
}
```

## Text Nodes

```typescript
function text(t: string) {
  return { type: "text", text: t };
}
function bold(t: string) {
  return { type: "text", marks: [{ type: "bold" }], text: t };
}
function italic(t: string) {
  return { type: "text", marks: [{ type: "italic" }], text: t };
}
function boldItalic(t: string) {
  return { type: "text", marks: [{ type: "bold" }, { type: "italic" }], text: t };
}
function code(t: string) {
  return { type: "text", marks: [{ type: "code" }], text: t };
}
```

## Paragraphs

```typescript
// Paragraphs contain text nodes (text, bold, italic, code, etc.)
function p(...nodes: any[]) {
  return { type: "paragraph", content: nodes };
}

// Examples:
p(text("Hello world"))
p(text("Use "), code("/effort"), text(" to set thinking depth"))
p(bold("Important:"), text(" this is a key point"))
```

## Code Blocks

```typescript
function codeBlock(t: string) {
  return { type: "codeBlock", content: [{ type: "text", text: t }] };
}
```

## Lists

```typescript
function li(...content: any[]) {
  // Each item wraps strings in paragraphs automatically
  return { type: "listItem", content: content.map(c =>
    typeof c === "string" ? p(text(c)) : c
  )};
}

function ol(...items: any[]) {
  return { type: "orderedList", content: items };
}

function ul(...items: any[]) {
  return { type: "bulletList", content: items };
}

// Examples:
ul(
  li(p(bold("Feature:"), text(" description here"))),
  li(p(code("command"), text(" - what it does"))),
  li("Simple string items work too")
)
```

## Horizontal Rule

```typescript
function hr() {
  return { type: "horizontalRule" };
}
```

## Links

```typescript
function link(text: string, href: string) {
  return {
    type: "text",
    marks: [{ type: "link", attrs: { href, target: "_blank", rel: "noopener noreferrer nofollow" } }],
    text
  };
}
```

## Images

```typescript
// For Convex storage images, use the storage-image API:
function storageImage(storageId: string) {
  return {
    type: "image",
    attrs: { src: `/api/storage-image?storageId=${storageId}` }
  };
}
```

## Tables

```typescript
function table(rows: any[]) {
  return { type: "table", content: rows };
}

function tableRow(cells: any[]) {
  return { type: "tableRow", content: cells };
}

function tableHeader(...content: any[]) {
  return { type: "tableHeader", content: content.length ? content : [p()] };
}

function tableCell(...content: any[]) {
  return { type: "tableCell", content: content.length ? content : [p()] };
}
```

## HTML Embeds (interactive mini-apps)

An `htmlEmbed` block renders a sandboxed `<iframe>` inside the slide. It
always takes the full slide body and must sit at the top level of the doc
(not nested inside a column).

**JSON:**

```typescript
type HtmlEmbedMode = "srcdoc" | "url";

function htmlEmbedSrcdoc(html: string, height = "70vh") {
  return {
    type: "htmlEmbed",
    attrs: { mode: "srcdoc", html, url: "", height },
  };
}

function htmlEmbedUrl(url: string, height = "70vh") {
  return {
    type: "htmlEmbed",
    attrs: { mode: "url", html: "", url, height },
  };
}
```

- `mode: "srcdoc"` — `html` is a complete document (`<!doctype html>…`)
  rendered inside a sandboxed iframe. No `allow-same-origin`, so the
  mini-app cannot touch localStorage/cookies or reach back into the parent
  — design it stateless (in-memory only) and load any deps from a public
  CDN (unpkg, jsdelivr, esm.sh, cdn.tailwindcss.com).
- `mode: "url"` — `url` is iframed directly with no sandbox. Use only for
  sources you trust.
- `height` accepts any CSS length. Typical values: `"70vh"` (default),
  `"80vh"`, `"420px"`.

**HTML mirror:** the wrapper `<div>` carries data-* attributes that
preserve authoring state; the inner `<iframe>` is what actually renders.
The runtime copies `data-embed-height` onto the iframe as inline style at
view time.

Srcdoc form — the `srcdoc` attribute must be HTML-escaped (`&quot;`,
`&lt;`, `&gt;`, `&amp;`), and so must `data-html`:

```html
<div
  data-mode="srcdoc"
  data-html="<!doctype html>&lt;html&gt;…escaped full doc…&lt;/html&gt;"
  data-url=""
  data-height="70vh"
  data-type="html-embed"
  class="html-embed"
>
  <iframe
    class="html-embed-iframe"
    data-embed-height="70vh"
    loading="lazy"
    referrerpolicy="no-referrer"
    sandbox="allow-scripts allow-forms allow-popups allow-modals allow-downloads allow-presentation allow-pointer-lock"
    srcdoc="<!doctype html>&lt;html&gt;…escaped full doc…&lt;/html&gt;"
  ></iframe>
</div>
```

URL form:

```html
<div
  data-mode="url"
  data-html=""
  data-url="https://example.com/app"
  data-height="70vh"
  data-type="html-embed"
  class="html-embed"
>
  <iframe
    class="html-embed-iframe"
    data-embed-height="70vh"
    loading="lazy"
    referrerpolicy="no-referrer"
    src="https://example.com/app"
  ></iframe>
</div>
```

**Generating the mirror HTML safely** — escape the HTML string once and
reuse it for both the wrapper's `data-html` attribute and the iframe's
`srcdoc` attribute:

```typescript
function escapeHtmlAttr(s: string) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function htmlEmbedHtml(html: string, height = "70vh") {
  const esc = escapeHtmlAttr(html);
  const sandbox =
    "allow-scripts allow-forms allow-popups allow-modals allow-downloads allow-presentation allow-pointer-lock";
  return (
    `<div data-mode="srcdoc" data-html="${esc}" data-url="" ` +
    `data-height="${height}" data-type="html-embed" class="html-embed">` +
    `<iframe class="html-embed-iframe" data-embed-height="${height}" ` +
    `loading="lazy" referrerpolicy="no-referrer" ` +
    `sandbox="${sandbox}" srcdoc="${esc}"></iframe></div>`
  );
}

function htmlEmbedUrlHtml(url: string, height = "70vh") {
  const escUrl = escapeHtmlAttr(url);
  return (
    `<div data-mode="url" data-html="" data-url="${escUrl}" ` +
    `data-height="${height}" data-type="html-embed" class="html-embed">` +
    `<iframe class="html-embed-iframe" data-embed-height="${height}" ` +
    `loading="lazy" referrerpolicy="no-referrer" ` +
    `src="${escUrl}"></iframe></div>`
  );
}
```

**Example:**

```typescript
const miniApp = `<!doctype html>
<html><head><style>
  body { margin:0; font-family:system-ui; background:#0b1220; color:#fff;
    min-height:100vh; display:flex; align-items:center; justify-content:center;
    flex-direction:column; gap:16px; }
  button { padding:10px 20px; border:1px solid #fff; background:transparent;
    color:#fff; border-radius:6px; font-size:16px; cursor:pointer; }
  #c { font-size:48px; font-weight:800; }
</style></head><body>
  <div id="c">0</div>
  <button onclick="c.textContent=+c.textContent+1">Click me</button>
</body></html>`;

const slideContent = makeDoc([
  h1("Live Demo"),
  htmlEmbedSrcdoc(miniApp, "70vh"),
]);

const slideHtml =
  `<h1>Live Demo</h1>` +
  htmlEmbedHtml(miniApp, "70vh");
```

**Authoring rules:**

- Keep it self-contained. If you need React, Three.js, Tailwind, etc., load
  them from a CDN inside the HTML string.
- Set `body { margin: 0; }` and design a layout that fills whatever size
  the iframe gets (roughly 1200×600 on desktop, smaller on mobile).
- The iframe background is white unless you paint your own.
- Default the design to the dark presentation background; any color-scheme
  handling must happen inside the iframe since it can't read the parent.

## Complete Slide Example

```typescript
const slideContent = makeDoc([
  h1("Slide Title"),
  h3("Subtitle or tagline"),
  p(text("Introductory context")),
  codeBlock("npm install something"),
  hr(),
  h3("Key Points"),
  ul(
    li(p(bold("Point 1:"), text(" explanation"))),
    li(p(bold("Point 2:"), text(" explanation"))),
    li(p(code("command"), text(" - what it does")))
  ),
  hr(),
  h3("When to Use"),
  ol(
    li(p(text("Use case one"))),
    li(p(text("Use case two")))
  ),
]);
```

## HTML Mirror

Every slide also needs `contentHtml` that mirrors the JSON. Generate it from the same content:

```html
<h1>Slide Title</h1>
<h3>Subtitle or tagline</h3>
<p>Introductory context</p>
<pre><code>npm install something</code></pre>
<hr>
<h3>Key Points</h3>
<ul>
<li><p><strong>Point 1:</strong> explanation</p></li>
<li><p><strong>Point 2:</strong> explanation</p></li>
<li><p><code>command</code> - what it does</p></li>
</ul>
<hr>
<h3>When to Use</h3>
<ol>
<li><p>Use case one</p></li>
<li><p>Use case two</p></li>
</ol>
```

Note: The HTML uses `<strong>` for bold, `<em>` for italic, `<code>` for inline code, and `<pre><code>` for code blocks. List items wrap content in `<p>` tags.

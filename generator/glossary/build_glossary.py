"""Build glossary.html (repo root) from terms.json + review.py.

    python3 generator/glossary/build_glossary.py

Refuses to write if a review key names no term, or if any card link fails to
resolve to an id="<anchor>" in its target page (the roadmap.html check).
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from review import R  # noqa: E402

def esc(s):
    return html.escape(s, quote=True)

def slug(s):
    return "t-" + re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# A repeated key in R's dict literal silently drops the earlier override; refuse it.
import ast, collections  # noqa: E402
_tree = ast.parse(open(os.path.join(HERE, "review.py"), encoding="utf-8").read())
_keys = [k.value for n in ast.walk(_tree) if isinstance(n, ast.Dict)
         for k in n.keys if isinstance(k, ast.Constant) and k.value in R]
_dups = [k for k, c in collections.Counter(_keys).items() if c > 1]
if _dups:
    sys.exit(f"review.py repeats keys: {_dups}")

terms = json.load(open(os.path.join(HERE, "terms.json")))
by_term = {e["t"]: e for e in terms}
unknown = sorted(set(R) - set(by_term))
if unknown:
    sys.exit(f"review.py names terms not in terms.json: {unknown}")

errors, page_cache, sections = [], {}, {}
for e in terms:
    e = dict(e, **{k: v for k, v in R.get(e["t"], {}).items() if k in ("m", "w")})
    e["src"] = R.get(e["t"], {}).get("src", [])
    e["s"] = html.unescape(e["s"])
    cards = []
    for title, href, mod in e["cards"]:
        if "#" not in href:  # card in a module that has no built page yet
            print(f"note: {e['t']}: skipped unpublished card '{html.unescape(title)}' (module {mod})")
            continue
        f, anchor = href.split("#", 1)
        if f not in page_cache:
            p = os.path.join(ROOT, f)
            page_cache[f] = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
        if f'id="{anchor}"' not in page_cache[f]:
            errors.append(f"{e['t']}: {href}")
        cards.append((html.unescape(title), href, mod))
    e["cards"] = cards
    sections.setdefault(e["s"], []).append(e)
if errors:
    sys.exit("unresolved card links:\n  " + "\n  ".join(errors))

ids = [slug(e["t"]) for es in sections.values() for e in es]
assert len(ids) == len(set(ids)), "duplicate term slugs"

def entry(e):
    text = " ".join([e["t"], e["m"], e["w"]]).lower()
    out = [f'<article class="term" id="{slug(e["t"])}" data-q="{esc(text)}">',
           f'<h3><a href="#{slug(e["t"])}">{esc(e["t"])}</a></h3>',
           '<div class="body">',
           f'<p class="m">{esc(e["m"])}</p>',
           f'<p class="w"><span class="lab">Comes up</span>{esc(e["w"])}</p>']
    if e["cards"]:
        links = "".join(
            f'<li><a href="{esc(h)}"><span class="mn" style="color:var(--m{m})">{m}</span>{esc(t)}</a></li>'
            for t, h, m in e["cards"])
        out.append(f'<div class="named"><span class="lab">Named in</span><ul>{links}</ul></div>')
    else:
        out.append('<p class="named none"><span class="lab">Named in</span>No published card yet.</p>')
    if e["src"]:
        srcs = "; ".join(f'<a href="{esc(u)}" rel="noopener">{esc(l)}</a>' if u else esc(l)
                         for l, u in e["src"])
        out.append(f'<p class="src"><span class="lab">Source</span>{srcs}</p>')
    out.append("</div></article>")
    return "".join(out)

n_terms = len(terms)
n_cited = sum(1 for es in sections.values() for e in es if e["src"])
n_links = sum(len(e["cards"]) for es in sections.values() for e in es)
nav = "".join(f'<a href="#{slug(s)}">{esc(s)} <span>{len(es)}</span></a>' for s, es in sections.items())
body = "".join(
    f'<section class="sec" id="{slug(s)}"><h2>{esc(s)} <span class="c">{len(es)}</span></h2>'
    + "".join(entry(e) for e in sorted(es, key=lambda e: e["t"].lower())) + "</section>"
    for s, es in sections.items())

tpl = open(os.path.join(HERE, "glossary.tpl.html"), encoding="utf-8").read()

# The palette is copied, not imported (DESIGN.md, TASKS.md #20). Refuse to build if
# this copy's light and dark values drift from the hub's.
def tokens(src):
    blocks = re.findall(r":root(?:\[data-theme=\"dark\"\])?\s*\{([^}]*)\}", src)
    return [dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9A-Fa-f]{3,8})", b)) for b in blocks[:2]]
hub = tokens(open(os.path.join(ROOT, "index.html"), encoding="utf-8").read())
mine = tokens(tpl)
drift = [(k, h[k], m[k]) for h, m in zip(hub, mine) for k in h if k in m and h[k].lower() != m[k].lower()]
if len(hub) < 2 or drift:
    sys.exit(f"palette drift vs index.html: {drift or 'could not read both :root blocks'}")

page = (tpl.replace("{{NAV}}", nav).replace("{{BODY}}", body)
           .replace("{{N_TERMS}}", str(n_terms)).replace("{{N_SECTIONS}}", str(len(sections)))
           .replace("{{N_CITED}}", str(n_cited)).replace("{{N_LINKS}}", str(n_links)))
assert "{{" not in page, "unfilled template slot"
out = os.path.join(ROOT, "glossary.html")
open(out, "w", encoding="utf-8").write(page)
print(f"{n_terms} terms | {len(sections)} sections | {n_cited} cited | {n_links} card links, 0 unresolved -> {out}")

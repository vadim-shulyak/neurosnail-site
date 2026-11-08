"""Builds the site from the legal texts: python3 build.py (policy is copied word for word from 08-legal)."""
import html, pathlib, re

ROOT = pathlib.Path(__file__).parent
LEGAL = ROOT.parent / "personality-architecture-docs/08-legal"

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"([\w.]+@[\w.]+\.\w+)", r'<a href="mailto:\1">\1</a>', s)

def body(md):
    out, items = [], []
    def flush():
        if items: out.append("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"); items.clear()
    for line in md.strip().split("\n"):
        if line.startswith("- "): items.append(inline(line[2:])); continue
        flush()
        if not line.strip(): continue
        if line.startswith("## "): out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("# "): out.append(f"<h1>{inline(line[2:])}</h1>")
        else: out.append(f"<p>{inline(line)}</p>")
    flush()
    return "\n".join(out)

def page(title, content, root=""):
    return f"""<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="{root}icon.png">
<link rel="apple-touch-icon" href="{root}icon.png">
<style>
  body {{ margin: 0; background: #F8F2E9; color: #2A201B; font: 17px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  main {{ max-width: 680px; margin: 0 auto; padding: 40px 16px 64px; }}
  h1 {{ font-size: 30px; line-height: 1.2; margin: 0 0 12px; }}
  h2 {{ font-size: 20px; margin: 32px 0 8px; }}
  a {{ color: #B24F43; }}
  p, li {{ color: rgba(42, 32, 27, 0.86); }}
  ul {{ padding-left: 22px; }}
  li {{ margin: 6px 0; }}
</style>
</head>
<body><main>
{content}
</main></body>
</html>
"""

policy = (LEGAL / "privacy-policy.uk.md").read_text(encoding="utf-8")
(ROOT / "pryvatnist").mkdir(exist_ok=True)
(ROOT / "pryvatnist/index.html").write_text(page("Політика конфіденційності — Нейро Шлімак", body(policy), "../"), encoding="utf-8")
(ROOT / "index.html").write_text(page("Нейро Шлімак", body(
    "# Нейро Шлімак\n\nЩодня одна коротка думка, яка налаштовує мислення.\n\n")
    + '\n<p><a href="pryvatnist/">Політика конфіденційності</a></p>'), encoding="utf-8")
(ROOT / ".nojekyll").write_text("")

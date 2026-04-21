from pathlib import Path

CRITSO = Path(__file__).resolve().parents[1] / "09_ Simulacao web" / "fluxus"
OLD = 'src="images/logo/logo.svg" data-light="images/logo/logo.svg" data-dark="images/logo/logo-dark.svg"'
NEW = 'src="images/fluxus-cover.png" data-light="images/fluxus-cover.png" data-dark="images/fluxus-cover.png"'

for f in CRITSO.glob("*.html"):
    t = f.read_text(encoding="utf-8")
    if OLD in t:
        f.write_text(t.replace(OLD, NEW, 1), encoding="utf-8")
        print("logo", f.name)

"""Copy checked-in Amicus CSS/JS into the installable companion plugin."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "assets"
target = ROOT / "wp-plugin" / "assets"
for group in ("css", "js"):
    (target / group).mkdir(parents=True, exist_ok=True)
    for path in (source / group).iterdir():
        if path.is_file():
            shutil.copy2(path, target / group / path.name)
print("Packaged", len(list(target.rglob("*.css"))), "CSS files and", len(list(target.rglob("*.js"))), "JS files")

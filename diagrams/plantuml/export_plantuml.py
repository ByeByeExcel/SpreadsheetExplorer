import subprocess
from pathlib import Path

# === CONFIGURATION ===
source_dir = Path("")
output_dir = Path("../exported")

# === CLEANUP ===
for file in output_dir.glob("*"):
    if file.is_file():
        file.unlink()

# === GENERATE EPS FILES ===
for puml_file in source_dir.rglob("*.puml"):
    output_file = output_dir / (puml_file.stem + ".eps")
    subprocess.run([
        "plantuml", "-teps", "-pipe"
    ], input=puml_file.read_bytes(), stdout=output_file.open("wb"))


import os, sys, json, yaml, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

OK = True
def warn(msg):
    print(f"::warning::{msg}")

def err(msg):
    global OK
    OK = False
    print(f"::error::{msg}")

def check_exists(rel):
    p = ROOT / rel
    if not p.exists():
        err(f"Missing required file: {rel}")
        return None
    print(f"✅ found: {rel}")
    return p

# 1) NDS_BOOTSTRAP.yaml
p_boot = check_exists("NDS_BOOTSTRAP.yaml")
owner_repo = None
spec_current = None
if p_boot:
    try:
        import yaml as _yaml
        data = _yaml.safe_load(p_boot.read_text(encoding="utf-8"))
        owner_repo = (data or {}).get("owner_repo")
        spec_current = (data or {}).get("spec", {}).get("current")
        if not owner_repo or "/" not in owner_repo:
            warn("owner_repo is blank or malformed (expected 'owner/repo').")
        else:
            print(f"owner_repo: {owner_repo}")
        if not spec_current:
            err("spec.current is missing in NDS_BOOTSTRAP.yaml")
        else:
            print(f"spec.current: {spec_current}")
    except Exception as e:
        err(f"Failed to parse NDS_BOOTSTRAP.yaml: {e}")

# 2) Required spec/docs
required_files = [
    "spec/NDS_EVIDENCE_MAP_v0.1.md",
    "spec/IMAGES_INDEX.md",
    "spec/VIDEOS_INDEX.md",
    "outs/PDF_CATALOG.md",
    "outs/READING_QUEUE.md",
    "outs/SPEC_DELTA_v0.3.1.md",
    "reports/pdf_quickscan.json",
]
for rel in required_files:
    check_exists(rel)

# 3) spec.current must exist
if spec_current:
    if not (ROOT / spec_current).exists():
        err(f"spec.current path not found: {spec_current}")

# 4) Validate JSON
qpath = ROOT / "reports" / "pdf_quickscan.json"
if qpath.exists():
    try:
        _ = json.loads(qpath.read_text(encoding="utf-8"))
        print("✅ reports/pdf_quickscan.json is valid JSON")
    except Exception as e:
        err(f"Invalid JSON in reports/pdf_quickscan.json: {e}")

# 5) Produce a small summary
summ = ROOT / "reports" / "qa_summary.txt"
summ.parent.mkdir(parents=True, exist_ok=True)
summ.write_text("QA completed. Errors = %s\n" % (not OK), encoding="utf-8")
print(f"📝 wrote {summ}")

# Exit: fail only if STRICT=true
STRICT = os.getenv("STRICT", "false").lower() == "true"
if STRICT and not OK:
    sys.exit(1)
else:
    sys.exit(0)

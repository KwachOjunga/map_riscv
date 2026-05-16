import json
import re
import subprocess
from pathlib import Path

# config
ISA_REPO_URL = "https://github.com/riscv/riscv-isa-manual.git"
ISA_REPO_DIR = "riscv-isa-manual"
JSON_FILE = "instr_dict.json"
ISA_SRC_DIR = ISA_REPO_DIR + "/src"

# check to clone riscv-isa-manual if not present
if not Path(ISA_REPO_DIR).exists():
    print("RISC-V ISA manual repository not found.")
    print("Cloning repository...")

    subprocess.run(["git", "clone", ISA_REPO_URL], check=True)

    print("Clone completed.\n")


def normalize_extension(ext):
    """
    Normalize extension names for comparison.

    Examples:
        rv_zicsr -> zicsr
        Zba      -> zba
        RV64M    -> m
    """
    ext = ext.lower()

    # remove rv/rv32/rv64 prefixes
    ext = re.sub(r"^rv(32|64)?", "", ext)

    # remove underscores and hyphens
    ext = ext.replace("_", "").replace("-", "")

    return ext.strip()


def extract_extensions_from_json(json_path):
    """
    Extract extension names from instr_dict.json.
    Assumes each instruction has an 'extension' field.
    """

    with open(json_path, "r") as f:
        data = json.load(f)

    extensions = set()

    # Flexible parsing
    if isinstance(data, dict):
        iterable = data.values()
    else:
        iterable = data

    for item in iterable:
        if not isinstance(item, dict):
            continue

        ext = item.get("extension")

        if not ext:
            continue

        # Handle list or string
        if isinstance(ext, list):
            for e in ext:
                extensions.add(normalize_extension(e))
        else:
            extensions.add(normalize_extension(ext))

    return extensions


def extract_extensions_from_manual(src_dir):
    """
    Scan all .adoc files for extension names.

    Matches:
        Zba
        Zicsr
        M
        F
        Zvbb
        etc.
    """

    extension_pattern = re.compile(r"\b(?:Z[a-zA-Z0-9]+|[MFADCVHBPKQJTSUN])\b")

    extensions = set()

    for adoc_file in Path(src_dir).rglob("*.adoc"):
        try:
            text = adoc_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        matches = extension_pattern.findall(text)

        for match in matches:
            extensions.add(normalize_extension(match))

    return extensions


json_extensions = extract_extensions_from_json(JSON_FILE)
manual_extensions = extract_extensions_from_manual(ISA_SRC_DIR)

matched = json_extensions & manual_extensions
json_only = json_extensions - manual_extensions
manual_only = manual_extensions - json_extensions

#
#   Print Report
#

print("=" * 60)
print("RISC-V Extension Cross-Reference Report")
print("=" * 60)

print(f"\nMatched Extensions ({len(matched)}):")
print(sorted(matched))

print(f"\nExtensions only in instr_dict.json ({len(json_only)}):")
print(sorted(json_only))

print(f"\nExtensions only in ISA manual ({len(manual_only)}):")
print(sorted(manual_only))

print("\nSummary")
print("-" * 60)
print(
    f"{len(matched)} matched, "
    f"{len(json_only)} in JSON only, "
    f"{len(manual_only)} in manual only"
)

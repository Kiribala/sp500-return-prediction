"""
run_all.py — Single-command orchestrator for the dissertation analysis.

Usage:
    python run_all.py

Runs both pipeline scripts in the correct order and reports total elapsed time.
"""

import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

STEPS = [
    ("Step 1/2 — Build master dataset", SCRIPT_DIR / "Build_Master_Dataset_final.py"),
    ("Step 2/2 — Run empirical analysis", SCRIPT_DIR / "Analysis_Pipeline_final.py"),
]


def run_step(label: str, script: Path) -> None:
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  Script: {script.name}")
    print(f"{'='*60}")
    t0 = time.time()
    result = subprocess.run([sys.executable, str(script)], check=False)
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"\n❌  {label} FAILED (exit code {result.returncode})")
        sys.exit(result.returncode)
    print(f"\n✅  {label} completed in {elapsed:.1f}s")


def main():
    total_start = time.time()
    print("\n" + "="*60)
    print("  MSc Dissertation — Full Analysis Pipeline")
    print("  'Does the Inclusion of Additional Financial Information")
    print("   Improve Stock Return Prediction Accuracy?'")
    print("="*60)

    for label, script in STEPS:
        if not script.exists():
            print(f"❌  Cannot find {script}. Aborting.")
            sys.exit(1)
        run_step(label, script)

    total = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"  ALL STEPS COMPLETE  |  Total time: {total/60:.1f} min")
    print(f"  Outputs written to: {SCRIPT_DIR / 'outputs'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

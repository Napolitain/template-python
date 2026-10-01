"""Run mutmut and fail if any mutant survives (``mutmut run`` always exits 0)."""

import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    subprocess.run(["mutmut", "run"], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["mutmut", "export-cicd-stats"], check=True, stdout=subprocess.DEVNULL)
    stats = json.loads(Path("mutants/mutmut-cicd-stats.json").read_text())

    bad = {k: stats[k] for k in ("survived", "no_tests", "suspicious", "timeout") if stats[k]}
    print(f"mutants: {stats['killed']}/{stats['total']} killed")
    if bad:
        subprocess.run(["mutmut", "results"], check=True)
        print(f"not killed: {bad}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

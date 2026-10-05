#!/usr/bin/env python
"""Beniget def-use chains over the domain, the taint fixture and language/.

One of exactly two PyPI tools in the roster whose latest release actually runs
on Python 3.6 -- and, unlike lizard and pydriller, its declared >=3.6 is true.

On THIS family the runner does one extra thing. It analyses language/ (PEP 695
syntax, which the byte-identical domain cannot contain) and counts the unbound
identifiers beniget reports there. beniget 0.5.0 has no visitor for the
type-parameter nodes gast produces, so it never binds a type parameter and
reports every USE of one as a free variable. gast parses the syntax correctly;
this is a wrong answer, not a parse failure, and the tool exits 0 either way.

The count is written into the report as `pep695_unbound_false_positives` so the
degradation is a measured number on every branch rather than a note in a
document. dataset.json records the expected value.
"""
from __future__ import print_function

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, *"packages/domain/src".split("/"))
PKG = "orderlab"

try:
    import gast
    import beniget
except ImportError as exc:
    print("STATUS: SKIPPED")
    print("  tool        : beniget")
    print("  import error: %s" % exc)
    sys.exit(3)

TARGETS = [
    "services/pricing_rules.py",
    "services/order_service.py",
    "analysis/taint_fixture.py",
    "analysis/call_graph_sample.py",
]

# Outside the domain, and outside the byte-identical invariant. See
# language/README.md.
LANGUAGE_TARGET = os.path.join(ROOT, "language", "version_features.py")


def analyse(rel):
    path = os.path.join(SRC, PKG, *rel.split("/"))
    with open(path) as handle:
        source = handle.read()
    tree = gast.parse(source)
    chains = beniget.DefUseChains()
    chains.visit(tree)
    beniget.UseDefChains(chains)

    defs = []
    for node, definition in chains.chains.items():
        name = getattr(definition, "name", lambda: None)()
        if not name:
            continue
        defs.append({
            "name": name,
            "line": getattr(node, "lineno", None),
            "uses": len(definition.users()),
        })
    unused = [d for d in defs if d["uses"] == 0 and d["line"]]
    return {
        "file": "%s/%s" % (PKG, rel),
        "definitions": len(defs),
        "unused_definitions": len(unused),
        "sample_unused": sorted(unused, key=lambda d: d["line"])[:6],
    }


def count_unbound(path):
    """Count the 'unbound identifier' warnings beniget prints for one file.

    beniget writes these to STDOUT and still exits 0, so they are captured
    rather than detected by return code -- which is the whole point of the
    measurement.
    """
    import io
    import contextlib

    with open(path) as handle:
        tree = gast.parse(handle.read())
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        chains = beniget.DefUseChains()
        chains.visit(tree)
    lines = [ln for ln in buffer.getvalue().splitlines() if "unbound identifier" in ln]
    names = sorted(set(ln.split("'")[1] for ln in lines if "'" in ln))
    return len(lines), names


def main():
    rows = [analyse(rel) for rel in TARGETS]
    report = {
        "tool": "Beniget",
        "interpreter": "%d.%d.%d" % sys.version_info[:3],
        "beniget": getattr(beniget, "__version__", "unknown"),
        "files": rows,
        "total_definitions": sum(r["definitions"] for r in rows),
    }

    if os.path.exists(LANGUAGE_TARGET):
        count, names = count_unbound(LANGUAGE_TARGET)
        report["pep695_unbound_false_positives"] = count
        report["pep695_unbound_names"] = names
        print("  %-42s %3d spurious unbound identifiers %s"
              % ("language/version_features.py", count, names))
        if count:
            print("  NOTE: beniget 0.5.0 does not bind PEP 695 type parameters.")
            print("        It exits 0 and the finding is wrong, not missing.")
            print("        See language/README.md and dataset.json.")
    outdir = os.path.join(ROOT, "reports")
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    with open(os.path.join(outdir, "beniget.json"), "w") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
    for row in rows:
        print("  %-42s %3d definitions, %2d unused"
              % (row["file"], row["definitions"], row["unused_definitions"]))
    if report["total_definitions"] == 0:
        print("WARNING: zero definitions found -- beniget did not parse the sources.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

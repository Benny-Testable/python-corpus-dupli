#!/usr/bin/env python
"""cognitive-ast -- cognitive complexity from the stdlib `ast` module.

There is no PyPI distribution called `cognitive-ast`; the name resolves to
nothing under any spelling. It is implemented here directly, which is also why
it is one of the few primary tools that runs on Python 3.6 at all.

Scoring follows Campbell's white paper (SonarSource, version 1.7, 2023):
+1 plus nesting for each if, ternary, for, while, catch and match; a flat +1 for
elif, else, each sequence of like boolean operators and direct recursion;
nothing for try/finally, methods or early returns; lambdas and nested functions
raise the nesting level.

Written 3.6-clean: no dataclasses, no walrus, no f-string `=` specifier.
"""
from __future__ import print_function

import ast
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, *"packages/domain/src".split("/"))
PKG = "orderlab"
THRESHOLD = 15

_MATCH = getattr(ast, "Match", None)       # Python 3.10+; absent on older interpreters


def _bool_runs(node):
    """Number of sequences of like boolean operators in an and/or expression, plus its operands.

    ``a or b and c or d`` is three sequences (or, and, or); a ``not`` around a
    boolean group starts a new sequence (Campbell, p.7-8).
    """
    ops, atoms = [], []

    def go(n):
        if isinstance(n, ast.BoolOp):
            for i, value in enumerate(n.values):
                if i:
                    ops.append(type(n.op).__name__)
                go(value)
        elif (isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not)
              and isinstance(n.operand, (ast.BoolOp, ast.UnaryOp))):
            ops.append("sep")
            go(n.operand)
            ops.append("sep")
        else:
            atoms.append(n)

    go(node)
    runs, prev = 0, None
    for op in ops:
        if op == "sep":
            prev = None
        elif op != prev:
            runs += 1
            prev = op
    return runs, atoms


def score_function(fn):
    """Cognitive Complexity of one function per Campbell, white paper v1.7 (Appendix B).

    Structural +1 plus nesting for if, ternary, for, while, catch and match;
    hybrid flat +1 for elif and else; flat +1 per boolean-operator sequence and
    for direct recursion. try/finally add nothing; lambdas and nested functions
    raise the nesting level.
    """
    state = {"score": 0, "recursive": False}

    def add(points):
        state["score"] += points

    def expr(n, nest):
        if isinstance(n, ast.BoolOp) or (
                isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not)
                and isinstance(n.operand, ast.BoolOp)):
            runs, atoms = _bool_runs(n)
            add(runs)
            for atom in atoms:
                expr(atom, nest)
        elif isinstance(n, ast.IfExp):
            add(1 + nest)
            for child in (n.test, n.body, n.orelse):
                expr(child, nest + 1)
        elif isinstance(n, ast.Lambda):
            expr(n.body, nest + 1)
        else:
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                    and n.func.id == fn.name):
                state["recursive"] = True
            for child in ast.iter_child_nodes(n):
                visit(child, nest)

    def block(stmts, nest):
        for stmt in stmts:
            visit(stmt, nest)

    def if_chain(n, nest, is_elif):
        add(1 if is_elif else 1 + nest)
        expr(n.test, nest)
        block(n.body, nest + 1)
        if len(n.orelse) == 1 and isinstance(n.orelse[0], ast.If):
            if_chain(n.orelse[0], nest, True)
        elif n.orelse:
            add(1)
            block(n.orelse, nest + 1)

    def visit(n, nest):
        if isinstance(n, ast.If):
            if_chain(n, nest, False)
        elif isinstance(n, (ast.For, ast.While)) or (
                hasattr(ast, "AsyncFor") and isinstance(n, ast.AsyncFor)):
            add(1 + nest)
            for child in ast.iter_child_nodes(n):
                if child in n.body or child in n.orelse:
                    visit(child, nest + 1)
                else:
                    expr(child, nest)
        elif isinstance(n, ast.ExceptHandler):
            add(1 + nest)
            if n.type is not None:
                expr(n.type, nest)
            block(n.body, nest + 1)
        elif _MATCH is not None and isinstance(n, _MATCH):
            add(1 + nest)
            expr(n.subject, nest)
            for case in n.cases:
                block(case.body, nest + 1)
        elif isinstance(n, ast.FunctionDef) or (
                hasattr(ast, "AsyncFunctionDef") and isinstance(n, ast.AsyncFunctionDef)):
            block(n.body, nest + 1)
        elif isinstance(n, ast.ClassDef):
            block(n.body, nest)
        elif isinstance(n, ast.expr):
            expr(n, nest)
        else:
            for child in ast.iter_child_nodes(n):
                visit(child, nest)

    block(fn.body, 0)
    return state["score"] + (1 if state["recursive"] else 0)


def _functions(body):
    """Top-level functions and class methods; nested functions are scored inside their parent."""
    for node in body:
        if isinstance(node, ast.FunctionDef) or (
                hasattr(ast, "AsyncFunctionDef") and isinstance(node, ast.AsyncFunctionDef)):
            yield node
        elif isinstance(node, ast.ClassDef):
            for inner in _functions(node.body):
                yield inner



def walk(path):
    with open(path, "r") as handle:
        source = handle.read()
    try:
        tree = ast.parse(source, path)
    except SyntaxError as exc:
        return [{"file": path, "function": "<unparseable>", "line": exc.lineno,
                 "score": None, "error": str(exc)}]
    rows = []
    for node in _functions(tree.body):
        rows.append({
            "file": os.path.relpath(path, ROOT).replace(os.sep, "/"),
            "function": node.name,
            "line": node.lineno,
            "score": score_function(node),
        })
    return rows


def main():
    target = os.path.join(SRC, PKG)
    if not os.path.isdir(target):
        print("STATUS: SKIPPED")
        print("  tool   : cognitive-ast")
        print("  reason : source root %s not found" % target)
        return 3
    rows = []
    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in sorted(filenames):
            if name.endswith(".py"):
                rows.extend(walk(os.path.join(dirpath, name)))
    rows.sort(key=lambda r: (-(r["score"] or 0), r["file"], r["function"]))
    over = [r for r in rows if (r["score"] or 0) > THRESHOLD]
    report = {
        "tool": "cognitive-ast",
        "threshold": THRESHOLD,
        "interpreter": "%d.%d.%d" % sys.version_info[:3],
        "functions": len(rows),
        "over_threshold": len(over),
        "worst": rows[:5],
        "rows": rows,
    }
    outdir = os.path.join(ROOT, "reports")
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    with open(os.path.join(outdir, "cognitive-ast.json"), "w") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
    print("cognitive-ast: %d functions, %d over threshold %d"
          % (len(rows), len(over), THRESHOLD))
    for row in rows[:5]:
        print("  %-28s %-30s %s" % (row["file"], row["function"], row["score"]))
    if not over:
        print("WARNING: nothing exceeded the threshold. The planted fixture "
              "classify_shipment should. Check that %s was actually scanned." % target)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

# language/ -- syntax introduced by this interpreter

**This directory is deliberately NOT byte-identical across families.** Every
other analysable file in this branch is. See the note at the top of
`dataset.json` (`languageFixture`).

`src/` is written to the Python 3.6 language subset so that the same domain
code can be held constant across every family in the corpus. That is what makes
a difference in tool output attributable to the branch variables. The cost is
that the domain can never exercise syntax newer than 3.6, and from this family
onward that stopped being free.

`version_features.py` contains **PEP 695** type-parameter syntax, **PEP 698**
`@override` and **PEP 701** f-strings, all new in 3.12. It is a target for the
parser-based tools, and it is the only place in the branch where they meet
syntax the domain cannot contain.

## What it measured

**`beniget` 0.5.0 is degraded on this family, and only on this family.**

It has 69 visitor methods and none of them handles the `TypeVar` /
`ParamSpec` / `TypeVarTuple` nodes that `gast` 0.7.0 produces for PEP 695 type
parameters. gast parses the syntax correctly -- this is not a parse failure --
but beniget never creates the binding, so every *use* of a type parameter is
reported as a free variable:

```
$ python -m beniget language/version_features.py
W: unbound identifier 'T' at <unknown>:11:29
W: unbound identifier 'T' at <unknown>:14:21
W: unbound identifier 'T' at <unknown>:18:21
W: unbound identifier 'T' at <unknown>:20:21
W: unbound identifier 'T' at <unknown>:24:29
W: unbound identifier 'T' at <unknown>:24:36
```

Six spurious findings in a 37-line file. The same file with the generics
removed produces none.

It writes them to **stdout**, exits **0**, and reports no error. beniget is the
primary tool for the Data Flow metrics, so this is a wrong answer rather than a
missing one -- the failure mode that no status check can see, and the reason
`dataset.json` gives this tool `status: "active-degraded"` rather than
`"active"`.

Every other parser-based tool in the roster handles PEP 695 correctly:
astroid resolves all nine top-level names, pylint scores the file 10.00/10,
ruff, radon, lizard, vulture, bandit, semgrep, complexipy and pyan3 all read it
without incident.

## Running the tools against it

```
bash tools/beniget/run_beniget.sh      # includes this directory
python tools/tool_integration.py --run
```

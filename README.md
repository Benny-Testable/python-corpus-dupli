# orderlab -- PY_V312_POETRY_CONDA_MICRO

Order-pricing domain used as a white-box tool-evaluation fixture. One branch of
the Python 3.12 family: 24 branches across 3 build backends, 4 package managers
and 2 architectures. The domain layer is byte-identical on every branch, so any
difference in tool output is attributable to the branch variables alone.

## Branch variables

| Variable | This branch |
|---|---|
| Branch | `PY_V312_POETRY_CONDA_MICRO` |
| Python | 3.12.11 |
| Build backend | poetry-core 2.4.1 |
| Backend metadata | pyproject [project] |
| Package manager | conda (solver-resolved) |
| Architecture | Microservices |
| Scenario | 2 - Microservices |
| Source root | `packages/domain/src` |
| Branch usable | yes |

> **Build backend.** poetry-core 2.4.1 -- the current latest release. Being on the 2.x line, it emits PEP 621 [project] rather than [tool.poetry], which is what makes the poetry-core + uv pairing resolvable; the 1.x releases the older families were held to could not express that table and left two branches of the grid unlockable.

> **Package manager.** conda can create a python=3.9.23 environment from conda-forge, but conda.anaconda.org and repo.anaconda.com are 403 at this build host's egress proxy, so no solved lock could be produced here. environment.yml is complete and solves on the operator's machine.

## Supported tools

29 tools are wired on this branch: 15 primary and 14 alternative, covering the
103-metric white-box framework. **29 of them can run on Python 3.12;
0 cannot.**

That is the measurement, not a defect. Every tool is pinned at its current
latest release, identically on all 24 branches, and the pins that this
interpreter excludes are guarded with an environment marker so they drop out of
resolution instead of failing it. A tool that cannot run exits **3**, not 0 --
a skip that looks like a pass is the failure mode this corpus exists to expose.

### Running here

| Tool | Role | Pin | Why |
|---|---|---|---|
| `CrossHair` | primary | `crosshair-tool==0.0.110` | crosshair-tool 0.0.110 declares >=3.8 but its real floor is 3.9. |
| `Coverage.py` | primary | `coverage==7.16.0` | Coverage.py 7.16.0 declares >=3.10. |
| `Pymcdc` | primary | `pymcdc==0.2.6` | pymcdc 0.2.6 declares >=3.10. |
| `Radon` | primary | `radon==6.0.1` | radon 6.0.1 declares no Requires-Python and imports cleanly on 3.8.. |
| `Lizard` | primary | `lizard==1.24.0` | lizard 1.24.0 -- a silent import crash on the 3.6 family, working from 3.7 onward. |
| `testmon` | primary | `pytest-testmon==2.2.0` | pytest-testmon 2.2.0 declares >=3.10. |
| `cognitive-ast` | primary | _binary / stdlib_ | Not a PyPI package -- no distribution of that name exists. |
| `jscpd` | primary | `jscpd@5.1.1` | jscpd 5.1.1 is an npm package that runs on Node, not on the project interpreter, so the Python version is irrelevant to it. |
| `pylint` | primary | `pylint==4.0.8` | pylint 4.0.8 declares >=3.10. |
| `Semgrep OSS` | primary | `semgrep==1.176.0` | semgrep 1.176.0 declares >=3.10, and bandit 1.9.4 with it. |
| `Bandit` | primary | `bandit==1.9.4` | bandit 1.9.4 declares >=3.10. |
| `pip-audit` | primary | `pip-audit==2.10.1` | pip-audit 2.10.1 declares >=3.10. |
| `cosmic-ray` | primary | `cosmic-ray==8.7.0` | cosmic-ray 8.7.0 declares >=3.9. |
| `Beniget` | primary | `beniget==0.5.0` | beniget 0.5.0 declares >=3.6 and means it. |
| `PyDriller` | primary | `pydriller==2.10` | pydriller 2.10 works. |
| `Ruff` | alternative | `ruff==0.16.6` | ruff 0.16.6 -- alternative for 19 of the 103 metrics. |
| `complexipy` | alternative | `complexipy==8.0.0` | complexipy 8.0.0 declares >=3.8. |
| `symilar (pylint)` | alternative | `pylint==4.0.8` | symilar ships inside pylint 4.0.8, so it arrives with it. |
| `Opengrep` | alternative | _binary / stdlib_ | Standalone binary with its own parser. |
| `Opengrep (taint mode)` | alternative | _binary / stdlib_ | Same binary, taint mode. |
| `Trivy` | alternative | _binary / stdlib_ | Standalone binary; scans manifests and lockfiles, never the interpreter. |
| `SlipCover` | alternative | `slipcover==1.1.0` | slipcover 1.1.0 declares >=3.9,<3.15. |
| `mutmut` | alternative | `mutmut==3.7.0` | mutmut 3.7.0 declares >=3.10. |
| `diff-cover` | alternative | `diff-cover==10.5.1` | diff-cover 10.5.1 declares >=3.10. |
| `astroid` | alternative | `astroid==4.0.4` | astroid 4.0.4, NOT the latest 4.3.1 -- and this is the one place in the corpus where the latest-everywhere policy had to yield. |
| `pyan3 + astroid` | alternative | `pyan3==2.8.1` | pyan3 2.8.1 declares >=3.10,<3.16. |
| `pylint + vulture` | alternative | `vulture==2.16` | vulture 2.16 declares >=3.9. |
| `dulwich` | alternative | `dulwich==1.2.14` | dulwich 1.2.14 declares >=3.10. |
| `sys.settrace driver (stdlib)` | alternative | _binary / stdlib_ | stdlib sys.settrace driver, written 3.6-compatible.. |

### Dark here

_(none)_

**No tool on this branch lies about its own support -- but one
lies about its results.** `beniget` 0.5.0 installs, imports, runs, exits 0 and
produces a report in which every use of a PEP 695 type parameter appears as an
unbound identifier. Declared support, importability and exit status are all
clean; the output is wrong. `dataset.json` records it as `active-degraded`,
a status this corpus did not need before this family.

### What moved since the earlier families

| | 3.6 | 3.7 | 3.8 | 3.9 | 3.10 | 3.11 | 3.12 |
|---|---|---|---|---|---|---|---|
| Tools running | 5 | 7 | 12 | 16 | 29 | 29 | **29** |
| Silent liars | 2 | 1 | 1 | 0 | 0 | 0 | **0** |
| Degraded (runs, wrong) | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
| Branches that build | 12/24 | 12/24 | 22/24 | 24/24 | 24/24 | 24/24 | **24/24** |
| PEP 621 `[project]` | 0 | 8 | 16 | 24 | 24 | 24 | **24** |
| Infra pins at latest | none | none | uv | uv, wheel | all 7 | all 7 | **all 7** |

- **Two tool pins moved, and they are the first to move for a
  reason that is not the interpreter.** `ruff` 0.16.5 to 0.16.6 and
  `complexipy` 7.0.1 to **8.0.0** -- both simply released between the 3.11
  build and this one. The policy is to re-resolve every pin live, never carry
  one forward, so 3.12 is not a third member of the 3.10/3.11 matched pair.
- **complexipy 8.0.0 dropped the `-mx` short flag.** The 3.11 family's
  invocation exits 2 here with `tip: to pass '-m' as a value, use '-- -m'`.
  Second consecutive complexipy release to break this corpus's command line;
  7.0.1 dropped `-o`. The runner now uses `--max-complexity-allowed`.
- **`language/` is new**, and it is not part of the byte-identical invariant.
  The domain is held to the 3.6 language subset so it can be identical across
  every family; `language/version_features.py` carries PEP 695, PEP 698 and
  PEP 701 so the parser-based tools have something newer than 3.6 to read.
- **beniget is degraded, and only here.** No visitor for the type-parameter
  nodes gast produces, so every use of a type parameter is reported as an
  unbound identifier -- exit 0, wrong output. Every other parser-based tool in
  the roster handles PEP 695 correctly.
- **Nothing else moved.** The infrastructure is at latest for the third family
  running, all 24 branches build, and the roster is unchanged at 29.

## Build

```
make setup        # conda env create -f environment.yml
make install      # conda env update -f environment.yml
```

> `environment.yml` is complete but no solved lock ships with it: conda.anaconda.org and repo.anaconda.com are both 403 at the egress proxy of the host this corpus was built on. Run `conda list --explicit > conda-lock.txt` on a machine with access to close the gap.

## Run

```
python -m orderlab
```

Each service is importable on its own:

```
python -c "from gateway_service import health; print(health())"
python -c "from pricing_service import quote; print(quote('gold', 600, 'retail', 'US', 100.0))"
```


## Test

```
make test         # pytest 9.1.1
make check        # Tool Triggering (Synthetic Data)/full_check.py -- cross-file consistency audit
```

pytest is pinned at 9.1.1, which is its current latest
release -- on this family the infrastructure pins cost nothing. It is
infrastructure, not one of the 29 roster tools, and so is exempt from the
latest-only policy either way: a branch whose tests cannot run is not a
branch.

## Workspace layout

```
python-corpus/  (PY_V312_POETRY_CONDA_MICRO)
|-- .github/  (1 files)
|-- language/  (2 files)
|-- packages/  (23 files)
|-- services/  (6 files)
|-- tests/  (7 files)
|-- Tool Triggering (Synthetic Data)/  (76 files)
|-- .editorconfig
|-- .gitignore
|-- .python-version
|-- Makefile
|-- dataset.json
|-- environment.yml
|-- pyproject.toml
|-- pytest.ini
|-- requirements-dev.txt
|-- requirements-runtime.txt
|-- requirements.lock
|-- setup.cfg
```

### Microservices

Five workspace members. `packages/domain` holds the same byte-identical domain
as the monolith branches; `packages/contracts` holds the wire schema with no
third-party dependency at all, so a service whose own dependencies failed to
install still fails for its own reason. Three services consume both.

`services/gateway_service` is where untrusted input enters. That makes the
microservices branches the mirror image of the monolith ones for taint
analysis: the same domain code, reached through a request envelope rather than
through argv and environment. A tool that scores the two architectures
differently is telling you about its source model, not about the code.



## Tool test-data folders

Three sibling folders sit at the repo root, alongside this branch's own
`Tool Triggering (Synthetic Data)/` (above).

### `Tool Triggering (Tool Github Test data)/`
Each of the 28 tool subfolders is that tool's own real upstream test suite,
pulled as-is from its actual GitHub project -- not generated. `Radon/` is
radon's own pytest suite; `pydriller/` is pydriller's own test suite;
`Opengrep/` is the real opengrep/semgrep test corpus (1,000+ files of rules,
parsing fixtures and snapshots). A correct run finds whatever that upstream
project's own tests genuinely contain.

### `Tool Clean (Synthetic Data)/`
25 of the 28 tools each carry 5 generated fixture packages, one per Python
interpreter (3.6, 3.7, 3.11, 3.13, 3.14), each a self-contained package
(`pyproject.toml`, `src/<module>/`, `tests/`) under its own invented domain
name -- engineered to be clean, so the tool should report zero findings:
the **Tool Clean (100% pass)** condition. The remaining 3 tools
(`diff-cover`, `dulwich`, `pydriller`) operate on git history rather than
interpreter syntax, so each carries one real git repository's worth of
history instead of 5 per-version copies -- restored from `_git-bundles/`
via `restore-invalid-git.ps1` rather than kept as a live `.git` folder, so a
plain file copy never silently drops their content. `_generator/` holds the
scripts that built every fixture.

### `Tool Invalid (Synthetic Data)/`
Same shape as Clean -- 25 tools x 5 Python-version fixtures, plus the same
3 git-history tools -- but every fixture is engineered to make the tool
flag or fail rather than pass: the **Tool Invalid** condition. `_git-bundles/`
backs up each git-history tool's real history, with `restore-invalid-git.ps1`
to rebuild it; `live_results.json` and this folder's own README/archive
travel with it.

## Tool entry points

Every tool directory carries a `trigger.yaml` recording its pin, its declared
floor, its measured status on this interpreter and what a working run should
find. Run one tool directly, or all of them:

```
bash "Tool Triggering (Synthetic Data)/radon/run_radon.sh"
python "Tool Triggering (Synthetic Data)/tool_integration.py" --run
python "Tool Triggering (Synthetic Data)/tool_integration.py" --verify
```

`--run` distinguishes three outcomes: a tool that ran, a tool that skipped for
a reason `dataset.json` already records, and a tool that skipped for a reason
it does not. Only the third is a finding.

## Planted fixtures

Every tool is pointed at something it should find. Without these, a tool that
ran and reported nothing is indistinguishable from a tool that silently
no-opped.

| Fixture | File | Planted for |
|---|---|---|
| Duplication | [`packages/domain/src/orderlab/services/retail_order_processor.py`](packages/domain/src/orderlab/services/retail_order_processor.py) + [`wholesale_order_processor.py`](packages/domain/src/orderlab/services/wholesale_order_processor.py) | jscpd, symilar |
| Complexity | [`packages/domain/src/orderlab/analysis/complexity_sample.py`](packages/domain/src/orderlab/analysis/complexity_sample.py) | Radon, Lizard, complexipy, cognitive-ast |
| Lint | [`packages/domain/src/orderlab/analysis/lint_violations.py`](packages/domain/src/orderlab/analysis/lint_violations.py) | pylint, Ruff |
| SAST | [`packages/domain/src/orderlab/analysis/sast_fixture.py`](packages/domain/src/orderlab/analysis/sast_fixture.py) | Semgrep + Bandit, Opengrep |
| Taint | [`packages/domain/src/orderlab/analysis/taint_fixture.py`](packages/domain/src/orderlab/analysis/taint_fixture.py) | Opengrep taint mode |
| Dead code | [`packages/domain/src/orderlab/analysis/dead_code.py`](packages/domain/src/orderlab/analysis/dead_code.py) | vulture, pylint |
| Call graph | [`packages/domain/src/orderlab/analysis/call_graph_sample.py`](packages/domain/src/orderlab/analysis/call_graph_sample.py) | pyan3 + astroid, Beniget |
| Vulnerable pins | [`requirements-runtime.txt`](requirements-runtime.txt) | pip-audit, Trivy |

The duplicate pair also co-changes three times in the git history, so a
change-coupling tool and a duplication tool should agree on it.

The five planted pins carry 45 live advisories between them,
confirmed against the PyPI JSON API on 3 September 2026. The planted set is unchanged from 3.10 and 3.11 -- `urllib3`
2.2.2 and `paramiko` 2.10.1, both moved at 3.10 for reasons unrelated to the
interpreter -- so the SCA metrics are directly comparable across those three
families.

`six` sits beside them in a clearly separated support section — paramiko
2.10.1 imports it without declaring it, and cryptography 42 no
longer supplies it by accident. Every one is genuinely imported by
[`packages/domain/src/orderlab/platform/integrations.py`](packages/domain/src/orderlab/platform/integrations.py) --
a pin nothing imports produces a manifest-versus-source disagreement that looks
like a tool defect and is not.

## History

Roughly 45 synthetic commits, authored as Prajith Kumaravel with three
co-authors carried in `Co-authored-by:` trailers. Measured on this family:
14-20% of commits each, three distinct names. A history tool
that reads only the author field reports one contributor at 100% and is wrong.
The processor pair co-changes three times; the tool runners co-change as a
cluster.

## Machine-readable

[`dataset.json`](dataset.json) carries every branch variable, the full tool
status breakdown with the verbatim reason for each dark tool, and the planted
fixture inventory. It is the answer key: a run is correct when what the tool
platform reports matches what `dataset.json` says should happen, **including
the tools that are supposed to be dark**.

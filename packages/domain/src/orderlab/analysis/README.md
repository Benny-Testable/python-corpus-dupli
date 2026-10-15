# Planted fixtures

Each file here exists so that one class of tool has a known, non-empty answer.
If a tool reports nothing against this directory, the tool did not run --
whatever its exit code said.

| File | Planted for | What a working tool should report |
|---|---|---|
| `complexity_sample.py` | Radon, Lizard, complexipy, cognitive-ast | `classify_shipment` scores well above the limit of 10 |
| `lint_violations.py` | pylint, Ruff | unused import, unused variable, bad naming, bare except, mutable default |
| `sast_fixture.py` | Semgrep OSS + Bandit, Opengrep | shell injection, `eval`, MD5, `yaml.load`, pickle, hardcoded secret, disabled TLS verify |
| `taint_fixture.py` | Opengrep taint mode, Semgrep | four flows from untrusted input to a dangerous sink |
| `dead_code.py` | vulture, pylint | three unreachable definitions and one unused constant |
| `call_graph_sample.py` | pyan3 + astroid, Beniget | a five-deep call chain and one recursive cycle |
| `nested_paths_sample.py` | coverage.py nested-condition-path measure | decisions nested four and five deep, only some of them taken by `tests/check_nested_paths_sample.py` |
| `access_control_fixture.py` | Opengrep / Semgrep (`orderlab-missing-authorization`) | four sensitive operations; two call `authorize` first, two are planted CWE-862 |
| `sensitive_flow_fixture.py` | Opengrep taint mode, Semgrep (`orderlab-taint-secret-to-output`) | three secrets from the environment reach a log, stdout or a file (CWE-200); one is redacted first and must not be reported |
| `entry_points_fixture.py` | Opengrep taint mode, Semgrep (`orderlab-taint-request-to-sql`) | three GET routes: one request parameter reaches SQL (CWE-89), one is cast and parameterised, one is authorised |

The duplication fixture is not here: it is the
`retail_order_processor.py` / `wholesale_order_processor.py` pair in
`../services/`, which also co-changes three times in the git history.

Nothing in this directory is imported by the package's public surface, and
nothing here executes at import time, except that `entry_points_fixture.py`
registers its three routes in a dict (no I/O).

# Security policy

This repository is a measurement corpus. The files under
`packages/domain/src/orderlab/analysis/`, the pins in
`requirements-runtime.txt` and the IaC under `infra/` are vulnerable on
purpose, so scanners have a known answer to find. They are listed in
`dataset.json` under `plantedFixtures`.

Reporting a problem that is not planted, such as a flaw in a tool runner under
`tools/` or in a CI workflow: open an issue on this repository. Do not put
exploit detail in the issue text. A report is acknowledged by whoever
maintains the branch; no response time is promised.

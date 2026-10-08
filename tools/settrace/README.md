# sys.settrace driver

A stdlib-only line tracer. It is the alternative tool for "Reporting Validation
/ Audit Trail Verification", and on this branch it carries more weight than
that: it is the one coverage-shaped measurement in the roster that depends on
nothing but the standard library, so it is the control against which
Coverage.py and SlipCover are read on the families where those two run.

It is not a substitute for either. It measures executed lines against an
`ast`-derived statement set, with no branch or arc analysis, and it exercises a
fixed scenario rather than the test suite.

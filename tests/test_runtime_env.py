"""The Python 3.12 runtime lock.

Fails on 3.11 AND on 3.13+, so a branch built or run against the wrong
interpreter says so immediately instead of producing plausible numbers.

The floor half is what separates this family from 3.11, and this is the first
time since 3.10 that the separation is a LANGUAGE change rather than a library
one: PEP 695 gives type parameters their own syntax, PEP 698 adds @override,
and PEP 701 lifts the restrictions on quotes inside f-strings. itertools.batched,
pathlib.Path.walk, sys.monitoring and calendar.Month arrive with them.

PEP 695 is not just a lock here. It is the reason `language/` exists on this
family: it is syntax the analysis tools have to model, and beniget does not.
See language/README.md.
"""
import sys


def test_interpreter_is_python_312():
    assert sys.version_info[:2] == (3, 12)


# ---- floor: everything below fails on 3.11 ------------------------------------

def test_pep695_type_alias_compiles():
    # PEP 695 `type X = ...`, new in 3.12. The 3.11 family asserts the OPPOSITE.
    namespace = {}
    exec("type Money = float", namespace)
    assert "Money" in namespace


def test_pep695_generic_function_compiles():
    # PEP 695 `def f[T]()`, new in 3.12.
    namespace = {}
    exec("def first[T](items: list[T]) -> T:\n    return items[0]", namespace)
    assert namespace["first"]([7, 8]) == 7


def test_pep695_generic_class_binds_its_type_parameter():
    # `class Box[T]` binds T for the whole class body. This is exactly the
    # binding beniget 0.5.0 fails to create -- see language/README.md.
    namespace = {}
    exec("class Box[T]:\n"
         "    def __init__(self, item: T) -> None:\n"
         "        self.item = item\n", namespace)
    box = namespace["Box"](3)
    assert box.item == 3
    assert namespace["Box"].__type_params__[0].__name__ == "T"


def test_type_params_are_visible_to_the_ast():
    # The stdlib ast models PEP 695 type parameters. A tool that does not is
    # not failing to parse -- it is parsing and then ignoring them.
    import ast
    tree = ast.parse("def first[T](x: T) -> T:\n    return x")
    assert [p.name for p in tree.body[0].type_params] == ["T"]


def test_typing_override_exists():
    # PEP 698, new in 3.12.
    import typing
    assert hasattr(typing, "override")


def test_itertools_batched_exists():
    # itertools.batched, new in 3.12.
    from itertools import batched
    assert list(batched([1, 2, 3, 4, 5], 2)) == [(1, 2), (3, 4), (5,)]


def test_path_walk_exists():
    # pathlib.Path.walk, new in 3.12.
    import pathlib
    assert hasattr(pathlib.Path, "walk")


def test_sys_monitoring_exists():
    # PEP 669, new in 3.12. tools/settrace/ deliberately does NOT use this --
    # it uses sys.settrace, because it must run on every family including 3.6.
    assert hasattr(sys, "monitoring")


def test_pep701_allows_the_same_quote_inside_an_fstring():
    # PEP 701, new in 3.12: reusing the outer quote character inside an
    # f-string expression is a SyntaxError on 3.11 and legal here.
    # NB: no nested dict literal here. build.py's sub() collapses "}" to "}",
    # so `{"tier": {"gold": 0.2}` emits as unbalanced source. dict() sidesteps
    # the template rather than fighting it.
    namespace = {"tier": dict(gold=0.2)}
    exec('rate = f"{tier["gold"]}"', namespace)
    assert namespace["rate"] == "0.2"


def test_calendar_month_enum_exists():
    # calendar.Month, new in 3.12.
    import calendar
    assert calendar.Month.JANUARY == 1


# ---- ceiling: everything below fails on 3.13+ ---------------------------------

def test_pep696_type_param_defaults_do_not_compile():
    # PEP 696 (`type Alias[T = int] = ...`) landed in 3.13.
    try:
        compile("type Listing[T = int] = list[T]", "<lock>", "exec")
    except SyntaxError:
        return
    raise AssertionError("PEP 696 defaults compiled -- this is not Python 3.12")


def test_typing_typeis_is_not_available():
    # PEP 742 typing.TypeIs landed in 3.13.
    import typing
    assert not hasattr(typing, "TypeIs")


def test_copy_replace_is_not_available():
    # copy.replace landed in 3.13.
    import copy
    assert not hasattr(copy, "replace")


def test_warnings_deprecated_is_not_available():
    # PEP 702 @warnings.deprecated landed in 3.13.
    import warnings
    assert not hasattr(warnings, "deprecated")


def test_os_process_cpu_count_is_not_available():
    # os.process_cpu_count landed in 3.13.
    #
    # This slot originally asserted random.binomialvariate was absent, on the
    # belief that it was a 3.13 addition. It is 3.12, and the test failed on
    # the very interpreter it was written for. Fourth time in this corpus that
    # a written claim and the executed behaviour have disagreed by exactly one
    # minor version -- after lizard's missing floor, crosshair's >=3.8, and the
    # 3.9 family's parenthesized context managers. Assume it; do not discover
    # it.
    import os
    assert not hasattr(os, "process_cpu_count")



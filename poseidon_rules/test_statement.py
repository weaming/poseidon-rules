from .utils import g
from .statement import ConditionalStatement
from .validator import is_date_format


def test_dict_as_statement_list_item():
    rule_dict = {
        "name": "example one",
        "if": [
            {"relation": "and", "statements": [True, True]},
            {"relation": "or", "statements": [False, True]},
        ],
        "must": [
            {"relation": "and", "statements": [True, True]},
            {"relation": "or", "statements": [False, True]},
        ],
    }
    rule = ConditionalStatement.from_dict(rule_dict)
    print(rule)


def test_else_must1():
    rule_dict = {
        "name": "example two 1",
        "if": False,
        "must": True,
        "else_name": "example two 1 (else)",
        "else_must": False,
    }
    rule = ConditionalStatement.from_dict(rule_dict)
    print(rule)
    assert bool(rule) is False


def test_else_must2():
    rule_dict = {
        "name": "example two 2",
        "if": True,
        "must": True,
        "else_name": "example two 2 (else)",
        "else_must": False,
    }
    rule = ConditionalStatement.from_dict(rule_dict)
    print(rule)
    assert bool(rule) is True


def test_boolean_as_statement_list_item():
    data = {"a": {"b": {"c": 4}}, "b": {"b": {"c": 3}}}
    x = g(data, "a.b.c")
    y = g(data, "b.b.c")
    rule_dict = {
        "name": "example two",
        "if": [x + y == 7],
        "must": [
            x == 4,
            y == 3,
            is_date_format("2019-06-01"),
            not is_date_format("20190101"),
        ],
    }
    rule = ConditionalStatement.from_dict(rule_dict)
    print(rule)
    assert bool(rule) is True

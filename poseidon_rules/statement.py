"""
* stands for required
- stands for optional

Statement (abstract):
    DeepStatement or boolean

DeepStatement (variant 1) (type dict):
    * relation (type str)
    * statements (type List[Statement])

DeepStatement (variant 2) (type List[Statement])

Rule:
    * name (type str)
    - if (type DeepStatement, default True)
    * must (type DeepStatement, default True)
    - desc (type str)
    - else_name (type str)
    - else_must (type DeepStatement, default True)
"""
from functools import reduce
from .errors import RuleFail


class Logic:
    def __and__(self, other):
        return self and other

    def __or__(self, other):
        return self or other


class Boolean:
    def __init__(self, v, boolean):
        self.v = v
        self.boolean = boolean

    def __bool__(self):
        return bool(self.boolean)

    def __repr__(self):
        return repr(self.v)


class StatementList(Logic):
    def __init__(self, statements, relation="and"):
        """
        :param statements: list
        :param relation: "and" or "or"
        """
        assert relation in ['and', 'or']
        self.relation = relation
        self.statements = statements

    def __bool__(self):
        return bool(self.evaluate())

    def evaluate(self, debug=False):
        if not debug:
            if self.relation == "and":
                return reduce(
                    lambda x, y: DeepStatement(x) and DeepStatement(y),
                    self.statements,
                    True,
                )
            elif self.relation == "or":
                return reduce(
                    lambda x, y: DeepStatement(x) or DeepStatement(y),
                    self.statements,
                    False,
                )
            else:
                raise Exception("unknown statements relation")
        else:
            if self.relation == "and":
                for _, x in enumerate(self.statements):
                    v = DeepStatement(x)
                    if not v:
                        return v
            else:
                return Boolean((self.relation, self.statements), False)
        return None

    def __repr__(self):
        return "<StatementList: {}({})>".format(self.relation, self.statements)

    def reason(self):
        return self.evaluate(debug=True)


class DeepStatement(Logic):
    def __init__(self, definition):
        """
        :param definition: dict, list or primitive types
            examples:
                {
                    "relation": "and"
                    "statements": [true, false, true]
                }

            or:
                [true, false, true]

            or:
                true

            or:
                none
        """
        self.definition = definition

    def __bool__(self):
        return bool(self.evaluate())

    def __repr__(self):
        return "<DeepStatement: {}>".format(self.definition)

    def evaluate(self):
        if isinstance(self.definition, dict):
            # ConditionalStatement
            if "must" in self.definition:
                return ConditionalStatement.from_dict(self.definition)
            # StatementList
            else:
                return StatementList(
                    self.definition["statements"], self.definition["relation"]
                )
        # List
        elif isinstance(self.definition, list):
            # print(self.definition)
            return StatementList(self.definition)
        # Boolean
        else:
            # "if" not provided
            if self.definition is None:
                return True
            return self.definition

    def reason(self):
        return self.evaluate()


class ConditionalStatement(Logic):
    def __init__(
        self,
        name,  # type: str
        if_,  # type: DeepStatement
        must,  # type: DeepStatement
        else_name=None,  # type: str
        else_must=None,  # type: DeepStatement
        desc=None,  # type: str
    ):
        """
        :param name:
        :param if_: list of
        :param must:
        :param desc:
        """
        assert (else_name is None) is (
            else_must is None
        ), 'should provide else_name and else_must, got "{}" "{}"'.format(
            else_name, else_must
        )
        self.name = name
        self.desc = desc or str(id)
        self.if_ = if_
        self.else_name = else_name
        self.must = must
        self.else_must = else_must

    def __repr__(self):
        return '<ConditionalStatement "{}": {}, {}, {} => {}>'.format(
            self.real_name(),
            self.is_satisfied(),
            self.is_must_valid(),
            self.is_else_must_valid(),
            bool(self),
        )

    def real_name(self):
        name = self.name
        if self.else_name is not None:
            if not self.is_satisfied():
                name = self.else_name
        return name

    def is_satisfied(self):
        return bool(self.if_)

    def is_must_valid(self):
        return bool(self.must)

    def is_else_must_valid(self):
        if self.else_must is not None:
            return bool(self.else_must)
        return True

    def __bool__(self):
        if self.is_satisfied():
            return self.is_must_valid()
        else:
            if self.else_must is not None:
                return self.is_else_must_valid()
        return True

    @classmethod
    def from_dict(cls, data):
        """
        :param data: dict
        """
        return cls(
            data["name"],
            DeepStatement(data.get("if")),
            DeepStatement(data["must"]),
            else_name=data.get("else_name"),
            else_must=DeepStatement(data["else_must"])
            if data.get('else_must') is not None
            else None,
            desc=data.get('desc'),
        )

    def reason(self):
        if self.is_satisfied():
            return self.must
        else:
            return self.else_must


def get_reason_stack(x, last_name=None, stack=None, prt=False):
    stack = stack or []
    if hasattr(x, 'reason'):
        reason = x.reason()
        assert bool(reason) is False
        if prt:
            print(reason)
        stack.append(reason)
        return get_reason_stack(
            reason,
            last_name=reason.real_name() if hasattr(reason, 'real_name') else last_name,
            stack=stack,
            prt=prt,
        )
    else:
        if prt:
            print(x)
        stack.append(x)
        return last_name, stack


def validate_rule_dict(rule_dict):
    rule = ConditionalStatement.from_dict(rule_dict)
    if not rule:
        last_name, _ = get_reason_stack(rule)
        raise RuleFail(last_name)


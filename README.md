# Poseidon Rules

Validate complex json data against rules you defined.

## Philosophy of this library

Business code has complex logic, and they can be wrapped deeply, so we need a DSL to define these rules in one place.

Every logic can have two basci relation, `and` or `or`, but the `not` logic is left to the rule evaluation written by developer.

Once one rule is not satisfied, the whole logic rule will be falsy, call the help function `get_reason_stack` will find the deepest name of rule, aka the exception message wrapped in the `RuleFail`.

Rules is defined in dict format, which is bad compared to the Haskell lazy evaluation. So you can pass a closure function to the "must" or "else_must", which will be called when "if" is evaluated to true ("must") or false ("else_must") at runtime, instead of define-time. This feature make you free from caring about the exception in some situations.

## Usage

See [test](poseidon_rules/test_statement.py)

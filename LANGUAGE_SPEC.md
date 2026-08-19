# Tamba Language Specification v0.1

## Core values

Tamba currently supports integers, floating-point numbers, strings, and booleans. Boolean literals are `dyame` (true) and `notdyame` (false).

## Output

`toree(...)` is the built-in output function.

## Variables

`let name = expression` creates a variable. Assignment uses `name = expression`.

## Control flow

Blocks use `{}`. Supported forms are `if`/`else`, `while`, functions, and `return`.

## Operators

Arithmetic: `+ - * / %`

Comparison: `== != < > <= >=`

Logic: `and or not`.

## Diagnostics

Lexer and parser diagnostics preserve filename, line, and column. Runtime diagnostics are designed to grow into full source-aware stack traces.

# Tamba 🐘

Tamba is a general-purpose programming language designed for performance, systems programming, AI/data, games, web development, applications, IoT, and security tooling.

## Status

Early development — **Tamba 0.1.1-dev**.

The current milestone is a real, tested tree-walk interpreter with the JUSU CLI. No mock implementations are used.

## Example

```tamba
let name = "Francis"
let ready = dyame

toree("Hello, " + name)
toree(ready)
```

Tamba uses `dyame` and `notdyame` for booleans, and `toree(...)` for output.

## JUSU CLI

```bash
jusu run hello.tmb
jusu repl
jusu version
```

## Current 0.1.1 work

- Lexer with filename, line, and column tracking
- Parser and AST with source locations
- Tree-walk interpreter
- `toree`, `dyame`, and `notdyame`
- Variables, assignment, expressions, conditions, loops, functions and returns
- Short-circuit `and` / `or`
- Source-aware runtime and parser diagnostics
- Regression tests and GitHub Actions CI

## Roadmap

- Collections and modules
- Complete call-stack diagnostics
- Bytecode VM and profiling
- Native compiler/JIT
- Native FFI and hardware capabilities
- Concurrency
- AI/data, game, web, mobile, desktop and IoT libraries
- JUSU package manager and registry

See `LANGUAGE_SPEC.md` and `ROADMAP.md` for the design.

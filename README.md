# Tamba 🐘

Tamba is a general-purpose programming language designed for performance, systems programming, AI/data, games, web development, applications, IoT, and security tooling.

## Status

Early development — **Tamba 0.1.0-dev**.

The first milestone is a real, tested tree-walk interpreter with the JUSU CLI. No mock implementations are used.

## Example

```tamba
let name = "Francis"
let ready = dyame

toree("Hello, " + name)
toree(ready)
```

## JUSU CLI

```bash
jusu run hello.tmb
jusu repl
jusu test
jusu version
```

## Roadmap

- Lexer and precise source locations
- Parser and AST
- Interpreter and REPL
- Rich diagnostics and stack traces
- Functions, collections, modules and concurrency
- Bytecode VM and native compiler
- Native/FFI and hardware capabilities
- AI/data, game, web, mobile, desktop and IoT libraries
- JUSU package manager and registry

See `LANGUAGE_SPEC.md` and `ROADMAP.md` for the design.

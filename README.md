# collatz-bench

Projeto poliglota **Python + C**: uma CLI em Python que explora a
[conjectura de Collatz](https://pt.wikipedia.org/wiki/Conjectura_de_Collatz) e
compara duas implementações do mesmo algoritmo:

- **Python puro** (`collatz_bench/core.py`);
- **C** (`csrc/collatz.c`), compilado como biblioteca compartilhada e chamado via `ctypes`.

Se a biblioteca C não estiver compilada, o projeto continua funcionando com o backend Python.

## Uso

```bash
make                                   # compila a lib em C
python -m collatz_bench steps 27       # 27 -> 111 passos
python -m collatz_bench longest 100000 # maior sequência até 100000
python -m collatz_bench longest 100000 --backend python
python -m collatz_bench bench 200000   # compara Python vs C
make test                              # roda os testes (pytest)
```

Requisitos: Python 3.9+, um compilador C (`gcc`/`clang`) e `pytest` para os testes.

## Estrutura

```
csrc/                 código em C (collatz.c / collatz.h)
collatz_bench/        pacote Python (core, cli)
tests/                testes com pytest
.github/workflows/    CI no GitHub Actions
```

## Limitações

O backend C usa inteiros de 64 bits; se a sequência estourar, é lançado `OverflowError`
(o backend Python não tem esse limite).

## Licença

MIT. Lembre de trocar `SEU NOME` no arquivo `LICENSE`.

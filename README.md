# template-python

Minimal Python template: [uv](https://docs.astral.sh/uv/), [ruff](https://docs.astral.sh/ruff/), [ty](https://docs.astral.sh/ty/), [pytest](https://pytest.org), hooks via [prek](https://prek.j178.dev).

```sh
uv sync                              # create .venv with dev tools
prek install                         # install pre-commit + pre-push hooks
uv run pytest                        # run tests with coverage (terminal + coverage.xml)
prek run -a                          # pre-commit hooks
prek run -a --hook-stage pre-push    # pre-push hooks
```

- pre-commit: `ruff format`, `ruff check --fix` (unsafe fixes on, review the diff), `ty check --fix`
- pre-push: `ty check`, `pytest` with coverage gate

## Optional Nix shell

Installing the tools directly on NixOS (or another OS) remains supported. The
optional shell supports x86_64/aarch64 Linux and Apple Silicon macOS. With Nix
flakes enabled:

```sh
nix develop --command "$SHELL"       # keep your shell, aliases and prompt
# Or: nix develop                   # use Nix's default Bash shell
```

Then run the normal development commands in this README. Each template has its own
`flake.nix` and `flake.lock`, using `github:NixOS/nixpkgs/nixpkgs-unstable`.
To refresh to the latest unstable packages, run `nix flake update nixpkgs`,
then leave and re-enter the shell. Commit the updated lock file with your project.

The shell supplies Python 3.14 and uv, and disables uv's Python downloads so
`uv sync` uses the Nix interpreter. Project dependencies and checks remain in uv.

## Complexity

Ruff's `C901` check enforces a maximum McCabe cyclomatic complexity of 10 per
function, including tests and tools, in the existing pre-commit hook and CI.
Configure it in `[tool.ruff.lint.mccabe]` in `pyproject.toml`. Refactoring is manual.
Ruff does not provide a cognitive-complexity rule.

## Coverage

pytest-cov (branch coverage) runs with every `pytest`, and fails below 80% (`fail_under` in `[tool.coverage.report]`).

## Property-based testing

[Hypothesis](https://hypothesis.readthedocs.io) generates inputs and shrinks failures to a minimal case; see `tests/test_template.py`. It runs with `pytest`.

```python
@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs: list[int]) -> None:
    assert sorted(sorted(xs)) == sorted(xs)
```

## Mutation testing

[mutmut](https://mutmut.readthedocs.io), on demand and weekly in CI (`.github/workflows/mutation.yml`); `tools/mutation.py` fails if any mutant survives (`mutmut run` itself always exits 0):

```sh
prek run --hook-stage manual mutmut --all-files
uv run mutmut browse    # inspect survivors
```

mutmut skips decorated functions (your code, not tests: `@given` tests are fine).

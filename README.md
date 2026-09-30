# template-python

Minimal Python template: [uv](https://docs.astral.sh/uv/), [ruff](https://docs.astral.sh/ruff/), [ty](https://docs.astral.sh/ty/), [pytest](https://pytest.org), hooks via [prek](https://prek.j178.dev).

```sh
uv sync            # create .venv with dev tools
prek install       # install git hooks
uv run pytest      # run tests with coverage (terminal + coverage.xml)
prek run -a        # run all hooks on all files
```

Pre-commit hooks: `ruff format`, `ruff check --fix` (unsafe fixes on, review the diff), `ty check --fix`.

Mutation testing ([mutmut](https://mutmut.readthedocs.io)), on demand and weekly in CI; fails if any mutant survives:

```sh
prek run --hook-stage manual mutmut --all-files
uv run mutmut browse    # inspect survivors
```

mutmut skips decorated functions.

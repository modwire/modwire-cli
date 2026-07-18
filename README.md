# modwire-cli

The command-line interface for the Modwire ecosystem.

## Install

```sh
pip install modwire-cli
```

## Usage

```sh
modwire --language python
```

By default, Modwire reads its configuration from `.modwire/architecture.yaml`
and analyses the current directory. Override either path when needed:

```sh
modwire --language typescript --dot-dir path/to/.modwire --architecture-root path/to/source
```

Use `--summary` for a compact module → layer map that omits individual source files:

```sh
modwire --language python --summary
```

To check this repository's architecture:

```sh
uv run modwire --language python
```

## Development

```sh
uv sync --all-groups
uv run pytest
uv run ruff check .
uv build
```

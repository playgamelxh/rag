# Copilot instructions for playgamelxh/AI

Purpose: short, focused guidance so Copilot sessions understand this repository structure, how to run things, and repository-specific conventions.

---

Build, test, and lint commands

- Python (per-subproject): many subfolders have their own requirements.txt. Typical workflow:
  - python -m venv .venv && source .venv/bin/activate
  - pip install -r airllm/requirements.txt
  - pip install -r RAG/python/video/requirements.txt
  - To run a script: python <path/to/script.py> (examples: python airllm/main.py, python MLP/mlp/train.py)
  - No repository-wide pytest, tox, or lint (flake8/black/mypy) configuration found; search each subfolder for its own tooling.

- Go (RAG/go): uses Go modules
  - Run all tests: cd RAG/go && go test ./...
  - Run a single test: go test ./... -run TestName (or cd into the package and run go test -run TestName)
  - Run example/main: go run ./main.go or go run ./path/to/package

Notes: there is no top-level build system or CI configuration discovered. Treat each subproject (airllm, RAG, MLP, CNN, Framework/PyTorch) independently for installing and running.

---

High-level architecture (big picture)

- airllm/: inference/optimization library for running very large LLMs with low memory (packaged Python project; entrypoint main.py; has requirements.txt).

- RAG/: retrieval-augmented generation examples and tooling. Contains:
  - python/: chunking, chunk vectorisation, vector store integrations (Chroma, Milvus), video example, and utility scripts. Some example data and a small Chroma DB are checked in under chroma_data/.
  - go/: helper tools and tests for chunking and keyword extraction; includes go.mod and unit tests.
  - docs/: architecture diagrams and notes on LoRA and transformers.

- MLP/ and CNN/: educational implementations (pure-Python) of small networks and helper scripts. Checkpoints (.pth) and example scripts live here (train.py, evaluation utils).

- Framework/PyTorch/: small reusable PyTorch utilities (resnet, torch_base) with an install note in its README.

Data and artifacts: several trained model checkpoints (.pth) and binary Chroma DB files are stored in the repo (MLP/, CNN/, RAG/python/chroma_data/). These are large, persistent data assets — do not edit them directly in code changes.

---

Key conventions and repo-specific patterns

- Per-subproject dependency files: expect requirements.txt inside subfolders. There is no single requirements.txt at repo root.

- Binary/data assets are checked-in: .pth model files and chroma.sqlite3 + binary shards. Copilot should avoid suggesting edits that modify these files; treat them as data.

- Tests: Go tests live under RAG/go and follow standard _test.go conventions. Python test-like scripts exist (e.g., chonkie_test.py) but no standardized pytest suite; run them as scripts unless a pytest config appears.

- Entrypoints are simple scripts: many modules expose top-level scripts (main.py, train.py). Use relative paths under the repository root when running them.

- Local environment hints: some subprojects assume GPU or larger disk (AirLLM, model training). Running full examples may require substantial disk space and GPU memory.

- Documentation-first: many subfolders include README.md with project-specific usage and parameters. Prefer reading the subfolder README before making behavioral changes.

---

Files and tooling to check before making changes

- airllm/requirements.txt, RAG/python/video/requirements.txt, any README inside a subproject for run examples and environment notes.
- RAG/python/chroma_data/ and MLP/CNN .pth files (large binaries) — avoid accidental diffs.

---

How Copilot should behave when editing or generating code

- Scope changes to a single subproject unless the user requests cross-cutting changes.
- Avoid generating or editing large binary/data files; treat them as external assets.
- When adding tests or CI, prefer adding per-subproject configuration (requirements, pytest.ini) rather than a monolithic root change.
- For Go packages under RAG/go, use the module-aware commands (go test, go vet) and follow existing test patterns.

---

If you'd like, the next step can be adding repository-level CI or recommended linting (black/flake8/ruff) and a single top-level README section describing how to run each subproject. If desirable, Copilot can also add .gitignore entries to avoid committing new large artifacts.


High-signal notes for automated agents (OpenCode / bots)

Only include repository-specific facts an agent would otherwise miss.

- Python: this project requires Python 3.13+. Do not attempt to run with older interpreters.

- Environment: copy .env.template -> .env and set DATABASE_URL and DATABASE_AUTH_TOKEN before running the app.

- Dependency managers (important):
  - Local development documented for humans uses Poetry (README). Use: `pip install poetry` then `poetry install`.
  - The Docker image and CI use the `uv` tool and the checked-in `uv.lock`. The Dockerfile runs `uv sync --no-dev` and docker-compose.test.yml runs `uv sync --group test`.
  - Do not mix workflows carelessly: if you run `uv sync` you are using the uv lockfile; if you use Poetry you are using pyproject. Mixing can produce mismatched environments.

- Start / entrypoint facts (authoritative):
  - Application ASGI app: `src.main:app` (use this module path). The repo contains a start script at `scripts/start.sh` which runs migrations then starts `uvicorn src.main:app --host 0.0.0.0 --port 3000`.
  - README contains an outdated uvicorn example (`uvicorn main:app`). Prefer `src.main:app` (the code and start script are authoritative).
  - Always run migrations before starting the server (the start script and docker compose do this): `alembic upgrade head` (run from the repo root so alembic.ini's prepend_sys_path = . works).

- Docker / compose
  - Build+run dev container: `docker-compose build` then `docker-compose up`. docker-compose.yml overrides the service command to run migrations and then `fastapi dev src/main.py --reload` inside the container.
  - Run tests in container (recommended for parity): `docker-compose -f docker-compose.test.yml up --build` (this uses `uv sync --group test` then runs pytest inside the container).

- Tests (local and single-test examples)
  - pytest.ini sets environment vars for the test run (ENVIRONMENT=testing, DATABASE_URL=sqlite:///:memory:, DATABASE_AUTH_TOKEN=test_token). Running pytest picks those up automatically.
  - To run the full suite locally (using Poetry's dependency-groups):
    - `poetry install --with test` (or include `dev` if you want tooling) then `pytest`
    - If you don't want to manage test deps locally, use the docker-compose.test.yml flow above.
  - Run a single test example: `pytest tests/v1/test_trm_api.py::test_get_trm_data`

- Alembic / migrations
  - Migration scripts live under `src/db` / `src/db/migrations` (alembic.ini script_location points there).
  - Always run `alembic upgrade head` from the repository root (the env.py expects repo layout / sys.path as configured by alembic.ini).

- Important assertions / brittle tests to watch for
  - Several tests assert the package version (health endpoint) equals the version in pyproject (0.1.0). Changing pyproject.toml version will break tests unless tests are updated.

- Formatting / linting
  - Black, isort and flake8 are in the `dev` dependency-group in pyproject. Run them after installing dev deps (e.g. `poetry install --with dev`) or via docker if you prefer.

- Files to check first when you start working
  - README.md (local quickstart), scripts/start.sh (authoritative start), docker-compose*.yml, Dockerfile, pyproject.toml, uv.lock, alembic.ini, pytest.ini.

- Minimal checklist an agent should follow before running or editing runtime behavior
  1. Ensure Python 3.13+ is used.
 2. Copy `.env.template` -> `.env` (or provide DATABASE_URL/DATABASE_AUTH_TOKEN via env) before starting the server.
 3. Install dependencies consistently (Poetry for local dev, uv inside container).
 4. Run migrations: `alembic upgrade head` from repo root.
 5. Start server with: `uvicorn src.main:app --host 0.0.0.0 --port 3000` (or use scripts/start.sh / docker-compose to get the migration step included).

If something is ambiguous (team conventions, release branching, or which tool to standardize on), ask a short question instead of guessing.

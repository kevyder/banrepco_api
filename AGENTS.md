High-signal notes for automated agents (OpenCode / bots)

Only include repository-specific facts an agent would otherwise miss.

- Python: this project requires Python 3.13+. Do not attempt to run with older interpreters.

- Environment: copy .env.template -> .env and set DATABASE_URL, DATABASE_AUTH_TOKEN, and BANREP_WEB_SERVICE_URL before running the app or scheduler.

- Dependency managers (important):
  - All local, CI, and container workflows use **uv** and the checked-in `uv.lock`. The Dockerfile runs `uv sync --no-dev` and docker-compose.test.yml runs `uv sync --group test`.
  - Do not use Poetry; mixing Poetry and uv will break environments.

- Application entrypoint (authoritative):
  - ASGI app: `src.main:app` (use this module path). The start script at `scripts/start.sh` runs migrations then starts `uvicorn src.main:app --host 0.0.0.0 --port 3000`.
  - Always run migrations before starting the server: `alembic upgrade head` (run from repo root so alembic.ini's prepend_sys_path = . works).

- Scheduled jobs (src/jobs/):
  - The scheduler runs as a separate sidecar process (banrepco-scheduler container) alongside the API.
  - Singleton behavior: file-based lock at `/tmp/banrepco_scheduler.lock`. If another instance is running, the scheduler exits immediately.
  - Job definition: `src/jobs/tasks/get_daily_trm.py` — `get_daily_trm()` fetches TRM from BanRep SDMX API, `insert_trm_into_db()` stores it via `TRMUseCase`, `get_daily_trm_job()` orchestrates both.
  - Scheduler entrypoint: `scripts/start_scheduler.sh` → `python -m src.jobs.scheduler`.
  - Runs daily at 00:00. Schedule is defined in `src/jobs/scheduler.py` via `schedule.every().day.at("00:00")`.
  - WAF note: BanRep's service (`totoro.banrep.gov.co`) has a WAF that blocks requests without browser-like headers or JavaScript execution. See `src/jobs/tasks/get_daily_trm.py` for current header configuration.

- Docker / compose
  - Build+run dev container: `docker compose build` then `docker compose up`. Runs migrations then `fastapi dev src/main.py --reload` inside the container.
  - Run tests in container (recommended for parity): `docker compose -f docker-compose.test.yml up --build`.
  - Scheduler container: `docker compose up -d --build banrepco-scheduler`.

- Tests (local and single-test examples)
  - pytest.ini sets environment vars for the test run (ENVIRONMENT=testing, DATABASE_URL=sqlite:///:memory:, DATABASE_AUTH_TOKEN=test_token). Running pytest picks those up automatically.
  - To run the full suite locally: `uv sync --group test` then `pytest`.
  - If you do not want to manage test deps locally, use the docker-compose.test.yml flow.
  - Run a single test example: `pytest tests/v1/test_trm_api.py::test_get_trm_data`

- Alembic / migrations
  - Migration scripts live under `src/db` / `src/db/migrations`.
  - Always run `alembic upgrade head` from the repository root.

- Important assertions / brittle tests to watch for
  - Several tests assert the package version (health endpoint) equals the version in pyproject (0.1.0). Changing pyproject.toml version will break tests unless tests are updated.

- Formatting / linting
  - Black, isort and flake8 are in the `dev` dependency-group in pyproject. Run after installing dev deps (`uv sync --group dev`) or via docker.

- Files to check first when you start working
  - README.md (local quickstart), scripts/start.sh (app entrypoint), scripts/start_scheduler.sh (scheduler entrypoint), docker-compose*.yml, Dockerfile, pyproject.toml, uv.lock, alembic.ini, pytest.ini.

- Minimal checklist an agent should follow before running or editing runtime behavior
  1. Ensure Python 3.13+ is used.
  2. Copy `.env.template` -> `.env` and set DATABASE_URL, DATABASE_AUTH_TOKEN, and BANREP_WEB_SERVICE_URL.
  3. Install dependencies: `uv sync`.
  4. Run migrations: `alembic upgrade head` from repo root.
  5. Start API server: `uvicorn src.main:app --host 0.0.0.0 --port 3000` (or use scripts/start.sh / docker compose).
  6. Start scheduler (if needed): `docker compose up -d --build banrepco-scheduler`.

If something is ambiguous (team conventions, release branching, or which tool to standardize on), ask a short question instead of guessing.

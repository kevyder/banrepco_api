# BanRepCo API

A FastAPI-based API enabling access to Bank of the Republic of Colombia (BanRep) data, such as inflation rates.

---

## Quickstart: Local and Container Usage

### Requirements

- Python **3.13+** (required for local development)
- Docker (optional, for container-based dev/test)

### 1. Environment Variables
Copy and update your environment file:
```bash
cp .env.template .env
# Edit the .env and set at least DATABASE_URL and DATABASE_AUTH_TOKEN
```
**Note:** The service will not start without valid values for these variables. See `.env.template` for required fields.

- `BANREP_WEB_SERVICE_URL`: The root URL of the BanRep TRM SDMX web service (required for scheduled daily TRM jobs).

### 2. Dependency Installation

**Canonical local (bare metal) install:**
```bash
# Ensure uv is installed (see https://github.com/astral-sh/uv)
pip install uv
# Install runtime and dev dependencies as specified in uv.lock
uv sync --all
```
**IMPORTANT:**
- Do **not** use Poetry for dependency management (even if present in some files/instructions). All official tooling, CI, and containers rely on **uv** and the checked-in `uv.lock`.
- Mixing Poetry and uv commands or files will break environments.

### 3. Database Migrations
Run migrations (always before starting the app):
```bash
alembic upgrade head
```

### 4. Starting the Server
- **Preferred local command:**
  ```bash
  uvicorn src.main:app --host 0.0.0.0 --port 3000
  # or use scripts/start.sh (runs migrations then starts app):
  ./scripts/start.sh
  ```
- App will be available at http://localhost:3000

### 5. Developing/Testing with Containers
**Development:**
```bash
docker-compose build
docker-compose up
```
- This runs migrations before starting FastAPI autoreload in `src/main.py` in dev mode inside the container.

**Testing/CI:**
```bash
docker-compose -f docker-compose.test.yml up --build
```
- This installs test dependencies with `uv sync --group test` and runs pytest inside the container.

### 6. Local Testing (Advanced)
If you want to run tests locally:
```bash
uv sync --group test
pytest
```
- `pytest.ini` will automatically set test db URL/token. To run a specific test:
  ```bash
  pytest tests/v1/test_trm_api.py::test_get_trm_data
  ```

### 7. Alembic Migrations (Repeat After Changes)
```bash
alembic upgrade head
# Always run from the repo root.
```

### 8. Formatting and Linting
Ruff is used for both formatting and linting (replaced black, isort, flake8).
```bash
uv sync --group dev
ruff check .        # lint
ruff format .       # format
```
Pre-commit hooks run ruff automatically — see `.pre-commit-config.yaml`.

### 9. Scheduled Jobs (TRM Daily Sync)
The scheduler runs as a separate sidecar container alongside the API. It fetches the daily TRM from BanRep's SDMX API and stores it in the database via `TRMUseCase`.
```bash
docker compose up -d --build banrepco-scheduler
```
- Runs daily at **00:00** (midnight).
- Singleton: file-based lock prevents multiple instances from running simultaneously.
- Job logic lives in `src/jobs/tasks/get_daily_trm.py`.
- Scheduler entrypoint: `scripts/start_scheduler.sh`.

---

## API Documentation

- Swagger/OpenAPI: http://localhost:3000/docs
- ReDoc: http://localhost:3000/redoc

---

## Quick Reference (Common Commands)

| Task                        | Command                                                      |
|-----------------------------|--------------------------------------------------------------|
| Install deps (local)        | `uv sync`                                                    |
| Install dev deps            | `uv sync --group dev`                                        |
| Run linting                 | `ruff check .`                                              |
| Run formatting             | `ruff format .`                                              |
| Run migrations             | `alembic upgrade head`                                       |
| Start server (local)        | `uvicorn src.main:app --host 0.0.0.0 --port 3000`           |
| Start with script           | `./scripts/start.sh`                                         |
| Build Dev container         | `docker compose build`                                       |
| Run Dev container           | `docker compose up`                                          |
| Run tests (container)        | `docker compose -f docker-compose.test.yml up --build`       |
| Run tests (local)           | `pytest`                                                     |
| Start scheduler (container) | `docker compose up -d --build banrepco-scheduler`           |

---

## Important Gotchas / Notes

- **Python version:** 3.13+ is strictly required.
- **Dependency management:** Use only uv+uv.lock for installation. Do not use Poetry, even if it's mentioned elsewhere.
- **Mixing tools:** Never mix uv and Poetry commands or environments; you will break the local/CI contract.
- **.env file:** The app will not start without proper environment variables set in `.env`.
- **Migration command:** Always run `alembic upgrade head` from the repo root, before starting the app.
- **Entrypoint:** The canonical ASGI app path is `src.main:app`, not `main:app`.
- **Brittle test:** Some tests assert the version set in `pyproject.toml`. If you update the version, you **must** update the tests accordingly.

---

## Need More Details?
- See `AGENTS.md` for high-signal internal agent/developer tips and advanced workflow specifics.

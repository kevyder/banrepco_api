# BanRepCo API

A FastAPI-based API that provides access to Bank of the Republic of Colombia (BanRep) data, starting with inflation rates.

## Requirements

- Python 3.13+
- Docker (optional)

## Local Development Setup

1. Set up environment variables
```bash
cp .env.template .env
# Edit .env with your configuration
```

2. Install dependencies
```bash
pip install uv
uv pip install -r pyproject.toml
```

3. Run migrations
```bash
alembic upgrade head
```

4. Start the server
```bash
uvicorn main:app --port 3000
```

The API will be available at http://localhost:3000

## Docker Setup

1. Build the image
```bash
docker build -t banrepco-api .
```

2. Run the container
```bash
# Using .env file
docker run -p 3000:3000 --env-file .env banrepco-api
```

## API Documentation

Once the server is running, you can access:
- API documentation: http://localhost:3000/docs
- Alternative documentation: http://localhost:3000/redoc

## Environment Variables

Required environment variables are listed in `.env.template`. Copy this file to `.env` and update the values accordingly.

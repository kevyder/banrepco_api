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
pip install poetry
poetry install
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

## Run with Docker compose

1. Build the image
```bash
docker-compose build
```

2. Run the container
```bash
# Using .env file
docker-compose up
```

## Run Tests
```bash
docker-compose -f docker-compose.test.yml up --build
```

## API Documentation

Once the server is running, you can access:
- API documentation: http://localhost:3000/docs
- Alternative documentation: http://localhost:3000/redoc

## Environment Variables

Required environment variables are listed in `.env.template`. Copy this file to `.env` and update the values accordingly.

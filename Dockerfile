FROM python:3.13.9-slim

ENV UV_VERSION=0.10.6
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Set working directory
WORKDIR /api

# Install UV
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv==$UV_VERSION

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --no-dev

# Copy application code
COPY . /api/

# Make the startup script executable
RUN chmod +x /api/scripts/start.sh

# Expose port
EXPOSE 3000

# Command to run migrations and start the application
CMD ["/api/scripts/start.sh"]

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Create and activate virtual environment, install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv==0.8.17 && \
    uv pip install --system --no-cache-dir -r pyproject.toml

# Copy application code
COPY . /app/

# Make the startup script executable
RUN chmod +x /app/scripts/start.sh

# Change ownership of the app directory to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 3000

# Command to run migrations and start the application
CMD ["/app/scripts/start.sh"]
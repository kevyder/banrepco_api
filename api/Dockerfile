FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Install Poetry
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry==2.2.0

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

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
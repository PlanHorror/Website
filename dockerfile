# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=website.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gettext \
        gcc \
        python3-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirement.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy project
COPY . .

# Create directories for static and media files with proper permissions
RUN mkdir -p /app/staticfiles /app/media

# Copy existing media files to the container (if they exist)
RUN if [ -d "media" ]; then cp -r media/* /app/media/ 2>/dev/null || true; fi

# Set temporary environment variables for collectstatic
ENV DATABASE_URL=sqlite:///tmp/temp.db
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost

# Collect static files as root before switching user
RUN python manage.py collectstatic --noinput

# Create non-root user for security
RUN groupadd -r django && useradd -r -g django django

# Change ownership of the app directory to django user
RUN chown -R django:django /app

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/', timeout=10)" || exit 1

# Run the application
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 website.wsgi:application"]
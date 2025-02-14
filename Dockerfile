# Stage 1: Build dependencies
FROM python:3.10-alpine as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    libffi-dev \
    gcc \
    g++ \
    make \
    python3-dev \
    rust \
    cargo \
    pcre

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final image with only required files
FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Install runtime dependencies only
RUN apk add --no-cache \
    libffi \
    pcre

# Copy only necessary files from builder stage
COPY --from=builder /install /usr/local

# Copy application files
COPY app.py . 
COPY static/ static/

# Create and switch to non-root user
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--access-logfile", "-", "--error-logfile", "-", "app:app"]

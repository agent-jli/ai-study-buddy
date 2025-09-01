# AI Study Buddy Dockerfile
# Multi-stage build for production deployment

# Use the official uv image for faster builds
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Work directory inside the docker container
WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv lock for reproducible builds
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

# Create logs directory
RUN mkdir -p logs results

# Expose port for Streamlit
EXPOSE 8501

# Health check for container monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the app using uv
CMD ["uv", "run", "streamlit", "run", "application.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]
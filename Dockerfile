FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PuLP's CBC solver
RUN apt-get update && apt-get install -y \
    coinor-cbc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY main.py ./
COPY lp_optimizer/ ./lp_optimizer/

# Install Python dependencies using UV
# The --system flag installs to the system Python instead of a virtual environment
RUN uv pip install --system .

# Expose port
EXPOSE 8050

# Run the application
CMD ["python", "main.py"]
# Use an official Python base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Set working directory
WORKDIR /app

# Copy necessary files for the project
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry config virtualenvs.create false && \
  poetry install --no-dev

# Copy your source files
COPY src/ ./src/

# Expose the port your app will run on
EXPOSE 80

# Start your application
CMD ["uvicorn", "src.main.main:app", "--host", "0.0.0.0", "--port", "80"]

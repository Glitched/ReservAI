# First, build the frontend

# Install dependencies only when needed
FROM node:16-alpine AS deps
RUN apk add --no-cache libc6-compat
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install --frozen-lockfile

# Rebuild the source code only when needed
FROM node:16-alpine AS builder
WORKDIR frontend/
COPY --from=deps /node_modules ./node_modules
COPY frontend/. .

# Disable telemetry
ENV NEXT_TELEMETRY_DISABLED 1
RUN yarn build

# Use an official Python base image
FROM python:3.11-slim as runner

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

# Copy frontend
COPY --from=builder /frontend/dist/ ./static/

# Expose the port your app will run on
EXPOSE 8080

# Start your application
CMD ["uvicorn", "src.main.main:app", "--host", "0.0.0.0", "--port", "8080"]

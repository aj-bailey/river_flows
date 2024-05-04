FROM python:3.11 AS base

WORKDIR /app

# Set the PATH to include the poetry bin
ENV PATH="${PATH}:/root/.local/bin"

# Install system dependencies required for Python, Rust, and general build processes
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
curl \
libpq-dev \
&& rm -rf /var/lib/apt/lists/*

# Install Rust using rustup
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Add cargo's bin directory to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Install poetry
RUN pip install poetry==1.7.1
RUN poetry config virtualenvs.create false
COPY . /app
RUN poetry install

# Expose port 8000
EXPOSE 8000
#!/bin/bash
# Render build script - install only necessary dependencies

set -e  # Exit on error

echo "📦 Installing core dependencies..."

# Install only the core packages needed for the web service
pip install --no-cache-dir \
    fastapi==0.115.6 \
    uvicorn[standard]==0.34.0 \
    pydantic==2.10.5 \
    python-dotenv==1.0.1 \
    google-generativeai==0.8.4 \
    anthropic==0.46.0 \
    openai==1.59.8 \
    httpx==0.28.1 \
    aiohttp==3.11.11 \
    requests==2.32.3 \
    sqlalchemy==2.0.36 \
    alembic==1.14.0 \
    pytelegrambotapi==4.24.0 \
    pycryptodome==3.21.0 \
    llama-stack-client==0.1.0 \
    fastmcp==2.12.0

echo "✅ Dependencies installed successfully!"

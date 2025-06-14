# Smart Summarizer API

A RESTful API that accepts text input and returns a summarized version using AI models.

## Features

- Text summarization using Hugging Face Transformers
- FastAPI with Pydantic validation
- Comprehensive error handling
- Detailed logging system
- Basic rate limiting
- Simple web interface
- Dockerized deployment
- Unit tests with 'pytest'

## Requirements

- Python 3.8+
- FastAPI
- Hugging Face Transformers
- PyTorch
- Docker (optional)

## Installation

### Option 1: Local Installation

```bash
git clone https://github.com/AbduazizovaNozima/Smart-Summarizer-API.git
cd smart-summarizer-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
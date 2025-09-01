# AI Study Buddy

An AI-powered quiz generator that creates multiple choice and fill-in-the-blank questions using Groq's LLM API.

## Features

- Generate MCQ and fill-in-the-blank questions
- Interactive Streamlit interface
- Results tracking with CSV export
- Multiple difficulty levels

## Quick Start

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup
```bash
# Install uv (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <repository-url>
cd ai-study-buddy
./setup_dev.sh

# Set your Groq API key
echo "GROQ_API_KEY=your_api_key_here" > .env

# Run the application
uv run streamlit run application.py
```

Visit `http://localhost:8501` to use the app.

## Docker

```bash
docker build -t ai-study-buddy .
docker run -p 8501:8501 --env-file .env ai-study-buddy
```

## Jenkins for CI


## ArgoCD for CD


## Project Structure

```
src/
├── generator/     # Question generation logic
├── llm/          # Groq API client
├── models/       # Pydantic schemas
├── prompts/      # LLM prompt templates
└── utils/        # Helper functions
```

## Development

```bash
# Add dependencies
uv add package-name

# Add dev dependencies
uv add --dev package-name

# Run tests
pytest
```

## API Setup

1. Get a [Groq API key](https://console.groq.com/)
2. Add it to your `.env` file: `GROQ_API_KEY=your_key_here`

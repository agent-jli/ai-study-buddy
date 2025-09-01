# AI Study Buddy

An AI-powered study buddy application that generates quiz questions using Groq's LLM API.

## Features

- Generate Multiple Choice Questions (MCQ)
- Generate Fill-in-the-blank questions
- Interactive quiz interface with Streamlit
- Results tracking and CSV export
- Support for different difficulty levels

## Setup

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup the project**:
   ```bash
   git clone <repository-url>
   cd ai-study-buddy
   
   # Run the setup script
   ./setup_dev.sh
   ```

3. **Manual setup** (alternative):
   ```bash
   # Create virtual environment
   uv venv
   
   # Activate virtual environment
   source .venv/bin/activate
   
   # Install dependencies
   uv pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the project root with:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Running the Application

```bash
# Run the Streamlit application using uv
uv run streamlit run application.py
```

Or if you prefer to activate the virtual environment:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the Streamlit application
streamlit run application.py
```

The application will be available at `http://localhost:8501`

## Docker

Build and run with Docker:

```bash
# Build the image
docker build -t ai-study-buddy .

# Run the container
docker run -p 8501:8501 --env-file .env ai-study-buddy
```

## Project Structure

```
ai-study-buddy/
├── application.py              # Main Streamlit application
├── pyproject.toml             # Project configuration for uv
├── requirements.txt           # Python dependencies
├── setup_dev.sh              # Development setup script
├── .python-version           # Python version specification
├── src/
│   ├── common/               # Common utilities
│   ├── config/               # Configuration settings
│   ├── generator/            # Question generation logic
│   ├── llm/                  # LLM client (Groq)
│   ├── models/               # Pydantic models
│   ├── prompts/              # Prompt templates
│   └── utils/                # Helper utilities
└── manifests/                # Kubernetes manifests
```

## Changes from Previous Version

- **Switched from pip to uv**: Faster dependency management and virtual environment handling
- **Removed LangChain**: Direct integration with Groq API for better control and reduced dependencies
- **Removed setup.py**: Using modern `pyproject.toml` configuration
- **Updated Docker**: Now uses uv for dependency installation

## Development

### Adding Dependencies

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name
```

### Running Tests

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests (when available)
pytest
```

## API

The application uses Groq's API for LLM inference. Make sure to:

1. Sign up for a Groq account
2. Get your API key
3. Set it in your `.env` file

## License

[Add your license information here]

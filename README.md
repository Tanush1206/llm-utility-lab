# 🚀 LLM Utility Lab

> A production-oriented LLM utility API for text summarization and context-aware question answering.

[![CI](https://github.com/Tanush1206/llm-utility-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/Tanush1206/llm-utility-lab/actions/workflows/ci.yml)
[![Live API](https://img.shields.io/badge/Live%20API-Render-46E3B7)](https://llm-utility-lab.onrender.com)
[![Swagger Docs](https://img.shields.io/badge/Swagger-API%20Docs-85EA2D)](https://llm-utility-lab.onrender.com/docs)

**Live API:** https://llm-utility-lab.onrender.com  
**API Documentation:** https://llm-utility-lab.onrender.com/docs

LLM Utility Lab is a Python-based project that provides reusable LLM utilities for **text summarization** and **context-aware question answering**.

The project uses the **Groq API through its OpenAI-compatible interface** and follows a modular architecture with separate components for API communication, configuration, prompt management, application logic, token tracking, evaluation, logging, testing, and HTTP API exposure.

---

## ✨ Features

### Text Summarization

- Summarize arbitrary text using an LLM
- Configurable maximum sentence limit
- Input validation
- Token usage tracking
- CLI and HTTP API support

### Context-Aware Q&A

- Ask questions against user-provided context
- Support for multi-line context input
- Answers are restricted to the provided context
- Reduces unsupported answers when information is unavailable
- Token usage tracking
- CLI and HTTP API support

### LLM Infrastructure

- Centralized LLM client
- Groq Responses API integration
- OpenAI-compatible Python SDK
- Configurable model
- Configurable temperature
- Configurable request timeout
- API error handling
- Connection error handling
- Structured response and token usage models
- Request duration logging
- Token usage logging
- Safe logging without exposing prompts, API keys, context, or generated responses

## 🐳 Docker

The project ships with a Dockerfile (Python 3.12 slim, non-root user, health check on `/health`).

```bash
docker build -t llm-utility-lab .
docker run -p 8000:8000 --env-file .env llm-utility-lab
```

The API is then available at http://localhost:8000 and the Swagger docs at http://localhost:8000/docs. The live deployment on Render runs from this same Dockerfile.

### REST API

- FastAPI-based HTTP API
- Health check endpoint
- Text summarization endpoint
- Context-aware Q&A endpoint
- Request validation using Pydantic
- Structured API responses
- Centralized runtime error handling
- Unexpected error handling
- Interactive Swagger documentation
- Request examples in OpenAPI documentation

### Evaluation

- Evaluation case abstraction
- Case-insensitive response matching
- Unicode text normalization
- Evaluation runner
- Live Q&A evaluation against the LLM
- Aggregate evaluation score
- Total token tracking
- Historical evaluation reports
- Evaluation run comparison
- Case-level regression detection

### Testing

- Automated tests with `pytest`
- Client error handling tests
- Configuration validation tests
- Prompt construction tests
- API endpoint tests
- API validation tests
- API exception handling tests
- Evaluation framework tests
- Evaluation runner tests
- Regression detection tests

---

## 🏗️ Architecture

### Application Architecture

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
       ┌──────────────┐              ┌──────────────┐
       │   main.py    │              │    api.py    │
       │     CLI      │              │   FastAPI    │
       └──────┬───────┘              └──────┬───────┘
              │                             │
              │                  ┌──────────┴──────────┐
              │                  │                     │
              ▼                  ▼                     ▼
       ┌──────────────┐   ┌──────────────┐     ┌──────────────┐
       │ summarizer.py│   │    qa.py     │     │  API Models  │
       └──────┬───────┘   └──────┬───────┘     └──────────────┘
              │                  │
              └─────────┬────────┘
                        ▼
                 ┌──────────────┐
                 │  prompts.py  │
                 │    Prompt    │
                 │ Construction │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  client.py   │
                 │  LLM Client  │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   Groq API   │
                 │ Responses API│
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ LLMResponse  │
                 │ Text + Usage │
                 └──────────────┘
```

The evaluation pipeline is separated from the main application flow:

```text
qa_cases.json
      │
      ▼
evaluate_qa.py
      │
      ▼
Evaluation Framework
      │
      ├── Run evaluation
      ├── Calculate score
      ├── Track tokens
      ├── Compare previous run
      └── Detect regressions
      │
      ▼
Evaluation Reports
```

Generated evaluation reports are intentionally excluded from version control.

---

## 📁 Project Structure

```text
LLM Utility Lab/
│
├── src/
│   ├── __init__.py
│   ├── client.py
│   ├── config.py
│   ├── evaluation.py
│   ├── logging_config.py
│   ├── models.py
│   ├── prompts.py
│   ├── qa.py
│   └── summarizer.py
│
├── tests/
│   ├── test_api.py
│   ├── test_client.py
│   ├── test_config.py
│   ├── test_evaluation.py
│   ├── test_logging_config.py
│   └── test_prompts.py
│
├── examples/
│   └── sample_inputs.txt
│
├── evaluation/
│   └── qa_cases.json
│
├── api.py
├── evaluate_qa.py
├── main.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **Groq API**
- **OpenAI Python SDK**
- **Pydantic**
- **python-dotenv**
- **pytest**
- **JSON-based evaluation datasets**
- **Git & GitHub**

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Tanush1206/llm-utility-lab.git
cd llm-utility-lab
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
GROQ_TEMPERATURE=0.1
GROQ_TIMEOUT=60
```

The `.env` file is intentionally excluded from version control.

### Configuration

The application supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API authentication key | Required |
| `GROQ_MODEL` | LLM model used by the application | `openai/gpt-oss-20b` |
| `GROQ_TEMPERATURE` | LLM temperature | `0.1` |
| `GROQ_TIMEOUT` | API request timeout in seconds | `60` |

---

## ▶️ Running the Application

### CLI Application

Run the CLI application:

```bash
python main.py
```

The application provides options for:

- Text summarization
- Context-aware question answering

The CLI also supports multi-line input for longer context and text.

---

## 🚀 REST API

LLM Utility Lab also provides a FastAPI-based HTTP API for interacting with the LLM utilities.

### Start the API

Run:

```bash
uvicorn api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Interactive API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The API documentation provides interactive request and response schemas along with example request payloads.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Check API health |
| `POST` | `/summarize` | Summarize text |
| `POST` | `/ask` | Answer a question using provided context |

### Health Check

**Request**

```http
GET /health
```

**Response**

```json
{
  "status": "ok"
}
```

### Text Summarization

**Request**

```http
POST /summarize
```

```json
{
  "text": "The company was founded in 2018 and develops cloud-based accounting software.",
  "max_sentences": 1
}
```

**Response**

```json
{
  "summary": "Founded in 2018, the company develops cloud-based accounting software.",
  "usage": {
    "input_tokens": 194,
    "output_tokens": 81,
    "total_tokens": 275
  }
}
```

Token usage values can vary between requests.

### Context-Aware Q&A

**Request**

```http
POST /ask
```

```json
{
  "context": "The company was founded in 2018.",
  "question": "When was the company founded?"
}
```

**Response**

```json
{
  "answer": "2018",
  "usage": {
    "input_tokens": 199,
    "output_tokens": 51,
    "total_tokens": 250
  }
}
```

Token usage values can vary between requests.

---

## 🛡️ API Validation & Error Handling

The API validates incoming requests before making LLM calls.

Examples of invalid requests include:

- Empty text
- Empty context
- Empty questions
- Invalid `max_sentences` values

Validation failures are returned using FastAPI's standard validation response format.

The API also provides centralized exception handling.

### LLM Runtime Errors

LLM-related runtime errors return:

```text
502 Bad Gateway
```

Example:

```json
{
  "detail": "Groq server error. Please try again later."
}
```

### Unexpected Errors

Unexpected application errors return:

```text
500 Internal Server Error
```

Example:

```json
{
  "detail": "Internal server error."
}
```

Internal error details are not exposed to API clients.

Unexpected errors are logged server-side for debugging and observability.

---

## 🧪 Running Tests

Run the complete test suite:

```bash
python -m pytest -q
```

Current test suite:

```text
58 passed
```

The tests cover:

- API health checks
- Summarization endpoint
- Q&A endpoint
- API request validation
- API runtime error handling
- Unexpected API error handling
- LLM client behavior
- LLM API error handling
- Configuration validation
- Prompt construction
- Input validation
- Evaluation logic
- Text normalization
- Evaluation summaries
- Evaluation comparison
- Regression detection
- Evaluation report generation
- Evaluation history handling
- Logging configuration

---

## 📊 Evaluation Framework

The project includes a dedicated evaluation framework for measuring the reliability of the Q&A system.

Evaluation cases are stored in:

```text
evaluation/qa_cases.json
```

Each evaluation case contains:

```json
{
  "name": "Direct factual answer",
  "context": "The company was founded in 2018.",
  "question": "When was the company founded?",
  "expected": "2018"
}
```

The evaluation runner sends each case to the LLM and checks whether the expected information appears in the response.

Run the evaluation with:

```bash
python evaluate_qa.py
```

Example output:

```text
=== Q&A Evaluation ===

✓ Direct factual answer
✓ Context-grounded answer
✓ Missing information

Passed: 3/3
Score: 100%
Total tokens: 759
```

---

## 📈 Evaluation Run Comparison

The evaluation runner compares the current evaluation run with the previous historical run and reports:

- Score change
- Token usage change
- Passed case change
- Failed case change

Example:

```text
=== Evaluation Comparison ===
Score change: +0.00%
Token change: +3
Passed cases change: +0
Failed cases change: +0
```

This makes it easier to identify whether changes to prompts, models, or application logic affected evaluation performance.

---

## 🔍 Regression Detection

The evaluation framework detects **case-level regressions** where an evaluation case previously passed but fails in the current run.

A regression is represented as:

```text
Previous run: PASS
Current run: FAIL
```

When a regression is detected, the evaluation runner reports:

- Evaluation case name
- Expected result
- Previous response
- Current response

This allows individual evaluation cases to be identified when a change causes previously successful behavior to fail.

---

## 📂 Evaluation Reports

Every evaluation run produces a report containing:

- Evaluation summary
- Total token usage
- Model name
- Temperature
- Run timestamp
- Prompt version
- Individual case results

Generated evaluation reports are excluded from Git version control.

The generated files use:

```text
evaluation/latest_report.json
evaluation/history/
```

This provides a lightweight history of model evaluation performance over time without committing generated artifacts to the repository.

---

## 🧠 Evaluation Design

The evaluation system separates the following responsibilities:

```text
Evaluation Case
      │
      ▼
Model Response
      │
      ▼
Response Normalization
      │
      ▼
Expected Text Matching
      │
      ▼
Evaluation Result
      │
      ▼
Aggregate Metrics
      │
      ├── Score
      ├── Passed Cases
      ├── Failed Cases
      └── Token Usage
```

The framework also supports comparing two complete evaluation runs:

```text
Previous Run
     │
     ├── Score
     ├── Tokens
     ├── Passed Cases
     └── Failed Cases
          │
          ▼
     Comparison
          ▲
          │
     Current Run
```

---

## 📝 Logging & Observability

The project includes centralized application logging.

LLM requests log operational information such as:

- Model used
- Request duration
- Input token count
- Output token count
- Total token count
- Error type
- API status code

Sensitive information is intentionally excluded from logs.

The application does not log:

- API keys
- User prompts
- User context
- System instructions
- Generated LLM responses

Unexpected API errors are logged with server-side tracebacks while exposing only a generic error message to API clients.

---

## 🎯 Design Principles

The project follows several engineering principles:

### Separation of Concerns

LLM communication, configuration, prompt construction, application logic, API routing, evaluation, logging, and data models are implemented as separate modules.

### Configuration Through Environment Variables

Model configuration, temperature, timeout, and API credentials are controlled through environment variables rather than hardcoded values.

### Structured Responses

LLM responses and token usage are represented using dedicated data models.

### Input Validation

Invalid or empty inputs are rejected before making unnecessary API requests.

### Centralized Error Handling

API errors are handled centrally to provide consistent responses across endpoints.

### Safe Error Exposure

Internal implementation details and unexpected exceptions are not exposed to API clients.

### Observability

Operational LLM request information is logged without exposing sensitive application data.

### Evaluation-Driven Development

The project includes automated evaluation cases and regression detection so that changes to the LLM system can be measured instead of judged only manually.

### Test-Driven Engineering

Application components and API behavior are protected by automated tests to reduce regressions as the project evolves.

---

## 🔮 Future Improvements

Potential future improvements include:

- Semantic evaluation using embeddings
- LLM-as-a-judge evaluation
- More comprehensive evaluation datasets
- Retrieval-Augmented Generation (RAG)
- Persistent experiment tracking
- Evaluation dashboards
- Additional LLM providers
- Streaming responses
- Authentication and API authorization
- Rate limiting
- Improved CLI experience
- Automated CI evaluation runs
- Production hardening: retries with backoff, caching and monitoring

---

## 👨‍💻 Author

**Tanush Thakran**

Computer Science Student
Interested in AI/ML Engineering, LLM Applications, and Data Science.

GitHub:

https://github.com/Tanush1206

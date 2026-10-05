# 🚀 LLM Utility Lab

> A modular LLM-powered utility application for text summarization and context-aware question answering.

LLM Utility Lab is a Python-based project that provides reusable LLM utilities for **text summarization** and **context-aware question answering**.

The project uses the **Groq API through its OpenAI-compatible interface** and follows a modular architecture with separate components for API communication, prompt management, application logic, token tracking, evaluation, and testing.

---

## ✨ Features

### Text Summarization

- Summarize arbitrary text using an LLM
- Configurable maximum sentence limit
- Input validation
- Token usage tracking

### Context-Aware Q&A

- Ask questions against user-provided context
- Support for multi-line context input
- Answers are restricted to the provided context
- Reduces unsupported answers when information is unavailable
- Token usage tracking

### LLM Infrastructure

- Centralized LLM client
- Groq Responses API integration
- OpenAI-compatible Python SDK
- Configurable model
- Configurable temperature
- API error handling
- Structured response and token usage models

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

- Automated unit tests with `pytest`
- Input validation tests
- Prompt construction tests
- Evaluation framework tests
- Evaluation runner tests

---

## 🏗️ Architecture

```
User
  │
  ▼
main.py
CLI Interface
  │
  ├───────────────┐
  ▼               ▼
Summarizer      Q&A
summarizer.py   qa.py
  │               │
  └───────┬───────┘
          ▼
      prompts.py
  Prompt Construction Layer
          │
          ▼
      client.py
       LLM Client
          │
          ▼
       Groq API
     Responses API
          │
          ▼
      LLMResponse
      Text + Usage
```

The evaluation pipeline is separated from the main application flow:

```
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
evaluation/
├── latest_report.json
└── history/
    └── report_*.json
```

---

## 📁 Project Structure

```text
LLM Utility Lab/
│
├── src/
│   ├── __init__.py
│   ├── client.py
│   ├── evaluation.py
│   ├── models.py
│   ├── prompts.py
│   ├── qa.py
│   └── summarizer.py
│
├── tests/
│   ├── test_evaluation.py
│   └── test_prompts.py
│
├── examples/
│   └── sample_inputs.txt
│
├── evaluation/
│   ├── qa_cases.json
│   ├── latest_report.json
│   └── history/
│       └── report_*.json
│
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
- **Groq API**
- **OpenAI Python SDK**
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
```

The `.env` file is intentionally excluded from version control.

---

## ▶️ Running the Application

Run the CLI application:

```bash
python main.py
```

The application provides options for:

- Text summarization
- Context-aware question answering

The CLI also supports multi-line input for longer context and text.

---

## 🧪 Running Tests

Run the complete test suite:

```bash
python -m pytest -q
```

Current test suite:

```text
22 passed
```

The tests cover:

- Prompt construction
- Input validation
- Evaluation logic
- Text normalization
- Evaluation summaries
- Evaluation comparison
- Regression detection
- Evaluation report generation
- Evaluation history handling

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

--------------------------
Passed: 3/3
Score: 100%
Total tokens: 758
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
Token change: -2
Passed cases change: +0
Failed cases change: +0
```

This makes it easier to identify whether changes to prompts, models, or application logic affected evaluation performance.

---

## 🔍 Regression Detection

The evaluation framework detects **case-level regressions** where an evaluation case previously passed but fails in the current run.

Example:

```text
Previous run: PASS
Current run: FAIL
```

A regression is therefore treated differently from a general score change.

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

The latest evaluation report is stored at:

```text
evaluation/latest_report.json
```

Historical evaluation reports are stored in:

```text
evaluation/history/
```

Example:

```text
evaluation/
├── qa_cases.json
├── latest_report.json
└── history/
    ├── report_2026-09-21T123639.506421+0000.json
    └── report_2026-09-21T133411.928910+0000.json
```

This provides a lightweight history of model evaluation performance over time.

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

## 🎯 Design Principles

The project follows several engineering principles:

### Separation of Concerns

LLM communication, prompt construction, application logic, evaluation, and data models are implemented as separate modules.

### Configuration Through Environment Variables

Model configuration and temperature are controlled through environment variables rather than hardcoded values.

### Structured Responses

LLM responses and token usage are represented using dedicated data models.

### Input Validation

Invalid or empty inputs are rejected before making unnecessary API requests.

### Error Handling

Common API failures such as authentication errors, rate limits, server errors, and connection failures are converted into clear application-level errors.

### Evaluation-Driven Development

The project includes automated evaluation cases and regression detection so that changes to the LLM system can be measured instead of judged only manually.

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
- Improved CLI experience
- Automated CI evaluation runs

---

## 👨‍💻 Author

**Tanush Thakran**

Computer Science Student
Interested in AI/ML Engineering, LLM Applications, and Data Science.

GitHub:

https://github.com/Tanush1206

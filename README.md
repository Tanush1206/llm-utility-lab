# LLM Utility Lab

> A modular LLM-powered utility application for text summarization and context-aware question answering.

LLM Utility Lab is a Python-based project that provides reusable LLM utilities for **text summarization** and **context-aware question answering**.

The project uses the **Groq API through its OpenAI-compatible interface** and follows a modular architecture with separate components for API communication, prompt management, application logic, token tracking, evaluation, and testing.

---

## 🚀 Features

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
- Total token usage tracking

### Testing

- Automated unit tests with pytest
- Input validation tests
- Evaluation framework tests
- Evaluation runner tests

---

## 🏗️ Architecture

```text
                        ┌─────────────────┐
                        │      User       │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    main.py      │
                        │   CLI Interface │
                        └────────┬────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
             ┌──────────────┐         ┌──────────────┐
             │  Summarizer  │         │      Q&A     │
             │ summarizer.py│         │    qa.py     │
             └──────┬───────┘         └──────┬───────┘
                    │                         │
                    ▼                         ▼
             ┌────────────────────────────────────┐
             │            prompts.py              │
             │     Prompt Construction Layer      │
             └────────────────┬───────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    client.py    │
                     │   LLM Client    │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    Groq API     │
                     │  Responses API  │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │   LLMResponse   │
                     │   Text + Usage  │
                     └─────────────────┘
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
├── evaluate_qa.py
├── main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Groq API | LLM inference |
| OpenAI Python SDK | API client |
| python-dotenv | Environment variable management |
| pytest | Automated testing |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Tanush1206/llm-utility-lab.git
cd llm-utility-lab
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

You can use `.env.example` as a template.

> **Security:** Never commit your real API key to GitHub.

The `.gitignore` file is configured to exclude `.env`.

---

# ▶️ Running the Application

Start the CLI application:

```bash
python main.py
```

The application provides three options:

```text
=== LLM Utility Lab ===

1. Summarize text
2. Ask a question
3. Exit
```

---

## 📝 Text Summarization

Select option `1`:

```text
Choose an option: 1
```

You can provide multi-line text:

```text
Enter text to summarize:

Artificial intelligence is transforming many industries.
It is being used in healthcare, finance, education, and software development.
Organizations must also consider privacy, security, and responsible deployment.

(Press Enter on an empty line to finish.)
```

The application sends the provided text to the LLM and returns the generated summary.

Example:

```text
--- Summary ---

Artificial intelligence is transforming multiple industries,
while organizations must consider responsible deployment,
privacy, security, and other governance concerns.

--- Usage ---

Input tokens: 551
Output tokens: 155
Total tokens: 706
```

---

## 💬 Context-Aware Q&A

Select option `2`:

```text
Choose an option: 2
```

Provide your context:

```text
Enter context:

Python was created by Guido van Rossum.
It was first released in 1991.
Python is widely used for software development and data science.

(Press Enter on an empty line to finish.)
```

Then provide your question:

```text
Enter your question:

Who created Python?
```

Example response:

```text
--- Answer ---

Guido van Rossum.

--- Usage ---

Input tokens: 211
Output tokens: 52
Total tokens: 263
```

The Q&A system is instructed to answer using only the supplied context.

If the required information is not available in the context, the system can respond:

```text
The answer cannot be determined from the provided context.
```

---

## 🧪 Testing

The project includes automated tests using `pytest`.

Run the complete test suite:

```bash
python -m pytest -q
```

The test suite covers:

- Evaluation logic
- Expected text matching
- Case-insensitive evaluation
- Unicode text normalization
- Evaluation runner behavior
- Empty evaluation cases
- Summarizer input validation
- Q&A input validation

All tests should pass before changes are committed.

---

## 📊 LLM Evaluation

The project includes a separate live evaluation runner:

```bash
python evaluate_qa.py
```

This script sends predefined Q&A cases to the actual LLM and evaluates the generated responses.

Example:

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

### Evaluation Cases

The current evaluation covers:

1. Direct factual question
2. Context-grounded question
3. Question where the required information is missing

The evaluation runner is separate from the automated test suite because it makes real LLM API calls.

---

## 🧩 Design Principles

### Separation of Concerns

Different responsibilities are isolated into separate modules:

```text
client.py       → LLM/API communication
models.py       → Response and token data models
prompts.py      → Prompt construction
summarizer.py   → Summarization logic
qa.py           → Q&A logic
evaluation.py   → Evaluation logic
main.py         → CLI interaction
```

This makes individual components easier to test, modify, and extend.

---

### Grounded Question Answering

The Q&A system uses explicit instructions to restrict responses to the provided context.

This helps reduce unsupported or fabricated answers when the required information is not available.

---

### Token Usage Tracking

Each LLM response contains usage information:

```text
Input tokens
Output tokens
Total tokens
```

This provides visibility into the size and usage of individual LLM requests.

---

### Evaluation-Driven Development

The project separates two types of validation.

#### Automated Tests

Used to verify that the Python application logic works correctly.

```bash
python -m pytest -q
```

#### Live LLM Evaluation

Used to observe the behavior of the actual model.

```bash
python evaluate_qa.py
```

This distinction is important because **code correctness and LLM response quality are different things**.

---

## 🔮 Future Improvements

The following features are planned but are **not currently implemented**:

- Web-based user interface
- REST API
- Structured LLM outputs
- Larger evaluation datasets
- Additional evaluation metrics
- Persistent evaluation reports
- Model comparison
- Retrieval-Augmented Generation (RAG)
- Conversation history
- Docker deployment
- Production deployment
- Logging and observability
- Configuration management

---

## 🎯 Learning Goals

This project is being developed to explore practical LLM application engineering concepts, including:

- LLM API integration
- Prompt engineering
- Context-aware generation
- Input validation
- Error handling
- Token usage tracking
- LLM evaluation
- Automated testing
- Modular Python architecture

---

## 📌 Project Status

**Current Status:** Active Development

### Implemented

- ✅ Groq LLM integration
- ✅ Text summarization
- ✅ Context-aware Q&A
- ✅ Dynamic multi-line CLI input
- ✅ Prompt architecture
- ✅ Token usage tracking
- ✅ Error handling
- ✅ Evaluation framework
- ✅ Live Q&A evaluation
- ✅ Automated tests

---

## 👨‍💻 Author

**Tanush Thakran**

GitHub:
https://github.com/Tanush1206

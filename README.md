# ⚡ Forge — Local AI Coding Agent

> A terminal-based AI agent that reads, writes, and manages your codebase through natural language. Built from scratch with LangChain and OpenAI — a working clone of how Claude Code works under the hood.

---

## What It Does

Talk to your filesystem in plain English. Forge figures out what to do.

```
You:   "Create a Python script that fetches Bitcoin price"
Forge: ✓ Created crypto_price.py

You:   "Read my main.py and add error handling"
Forge: ✓ Read main.py → Updated with try/except blocks

You:   "Create a folder called utils and move helpers there"
Forge: ✓ Created utils/ → Moved helpers.py
```

---

## How It Works

Forge runs an **LangChain agent loop** — the same pattern behind Claude Code and Cursor:

```
User input
    ↓
GPT-4o-mini decides which tool to use
    ↓
Tool executes (read / write / list / create)
    ↓
Result fed back to agent
    ↓
Agent reasons over result → responds or calls next tool
    ↓
Final answer streamed to terminal
```

The agent streams its thinking in real time — you can watch it decide which tool to call and why.

---

## Tools

| Tool | What it does |
|------|-------------|
| `list_directory(path)` | Lists all files and folders at a given path |
| `read_file(filename)` | Reads and returns file contents |
| `write_file(filename, content)` | Creates or overwrites a file |
| `create_directory(path)` | Creates a new directory (nested paths supported) |

---

## Stack

```
LangChain    Agent loop · Tool binding · Streaming
OpenAI       GPT-4o-mini for reasoning
Python       os · file I/O · standard library
Rich         Terminal UI · Markdown rendering · Panels
```

---

## Run Locally

```bash
git clone https://github.com/agenticmohit/forge
cd forge
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
python forge.py
```

---

## Why I Built This

I wanted to understand how AI coding assistants work under the hood — not just use them. Forge is the result: a working agent that can navigate, read, and modify a codebase using nothing but natural language and four Python functions.

The core insight: Claude Code and Cursor aren't magic. They're an LLM with filesystem tools and a good system prompt. This project proves that.

---

## What's Next

- [ ] Add `run_python(code)` tool — execute code and return output
- [ ] Add `search_in_files(query)` — semantic search across codebase
- [ ] Web UI with FastAPI + streaming response

---

*Built as the capstone project of AI Engineer Bootcamp by Ardit Sulce · LangChain · OpenAI*
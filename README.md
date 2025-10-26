# Patriot 

Patriot is an autonomous cybersecurity agent that thinks, plans, and learns as it works. It performs analysis using task planning, self-reflection, and real-time security data. It's built specifically to help with CyberPatriot

USAGE INSTRUCTIONS BELOW

# Screenshots
<img width="979" height="651" alt="Screenshot 2025-10-14 at 6 12 35 PM" src="https://github.com/adhyaay-karnwal/patriot-agent/blob/main/Screenshot%202025-10-26%20160252.png" />
<br>
<img width="879" height="651" alt="Screenshot 2025-10-14 at 6 12 35 PM" src="https://github.com/adhyaay-karnwal/patriot-agent/blob/main/Screenshot%202025-10-26%20161035.png" />
<br>
<img width="979" height="651" alt="Screenshot 2025-10-14 at 6 12 35 PM" src="https://github.com/adhyaay-karnwal/patriot-agent/blob/main/Screenshot%202025-10-26%20163134.png" />

## Overview

Patriot takes complex cybersecurity questions and turns them into clear, step-by-step research plans. It runs those tasks using live security data, checks its own work, and refines the results until it has a confident, data-backed answer.

It’s not just a chatbot.  It’s an agent that plans ahead, verifies its progress, and keeps iterating until the job is done.

**Key Capabilities:**
- **Intelligent Task Planning**: Automatically decomposes complex queries into structured research steps
- **Autonomous Execution**: Selects and executes the right tools to gather security data
- **Self-Validation**: Checks its own work and iterates until tasks are complete
- **Real-Time Security Data**: Access to vulnerability databases, threat intelligence feeds, and more.
- **Safety Features**: Built-in loop detection and step limits to prevent runaway execution


### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key (get [here](https://platform.openai.com/api-keys)) <br>
  OR <br>
- Gemini API key (get [here](https://aistudio.google.com/app/apikey)) (FREE TIER - RECOMMENDED)

### Installation

Install UV if not already:
```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```
```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

1. Clone the repository:
```bash
git clone https://github.com/adhyaay-karnwal/patriot-agent.git
cd patriot-agent
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Set up your environment variables(whichever you set, thats the provider patriot will use):
```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=your-openai-api-key
# GEMINI_API_KEY=your-gemini-api-key
```

### Usage

Run Patriot in interactive mode:
```bash
uv run patriot-agent
```

Press CTRL+C to exit or type "exit"

### Example Queries

Try asking Patriot questions like:
- "How do I harden a Windows 10 image?"
- "What are the common vulnerabilities in a Cisco router?"
- "How do I analyze a pcap file for forensic evidence?"
- "What are the best practices for securing a Linux server?"

Patriot will automatically:
1. Break down your question into research tasks
2. Fetch the necessary security data
3. Perform analysis
4. Provide a comprehensive, data-rich answer

## Architecture

Patriot uses a multi-agent architecture with specialized components:

- **Planning Agent**: Analyzes queries and creates structured task lists
- **Action Agent**: Selects appropriate tools and executes research steps
- **Validation Agent**: Verifies task completion and data sufficiency
- **Answer Agent**: Synthesizes findings into comprehensive responses

## Project Structure

```
patriot/
├── src/
│   ├── patriot/
│   │   ├── agent.py      # Main agent orchestration logic
│   │   ├── model.py      # LLM interface
│   │   ├── tools.py      # Cybersecurity tools
│   │   ├── prompts.py    # System prompts for each component
│   │   ├── schemas.py    # Pydantic models
│   │   ├── utils/        # Utility functions
│   │   └── cli.py        # CLI entry point
├── pyproject.toml
└── uv.lock
```

## Configuration

Patriot supports configuration via the `Agent` class initialization:

```python
from patriot.agent import Agent

agent = Agent(
    max_steps=20,              # Global safety limit
    max_steps_per_task=5       # Per-task iteration limit
)
```

## Roadmap

1. Add line breaks to AI answer
2. Better tool use - terminal actions + file reading
3. Better OS and systems context
4. Enhance system prompt + add make it better for windows and linux


## License
Apache-2.0-license
Officially opensource
Built by Adhyaay Karnwal for CyberPatriot.


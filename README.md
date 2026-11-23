# Personal chat with an Actor, a Critic and a revision loop

Assignment 1 - AI Systems (Dr. Paul Avrahami).

A Hebrew Gradio chat that represents a person based on a LinkedIn profile and a personal summary.
For every question:
1. The **Actor** writes a candidate answer.
2. The **Critic** checks it and returns a Pydantic-validated `Evaluation` (`is_acceptable`, `feedback`).
3. A rejected answer goes back to the Actor with the feedback, for up to **3 attempts** per question.

Every attempt is saved in a separate review log.

> The profile in `personal_chat/data/` is a **sample profile of a fictional person** (Noa Levi), created for this assignment.

## Requirements

- **Python 3.12** (tested with 3.12.12)
- [**uv**](https://docs.astral.sh/uv/getting-started/installation/) package manager
- An **Anthropic API key** with credit ([Claude Console → API keys](https://platform.claude.com/settings/keys))
- VS Code or Cursor with the Python and Jupyter extensions, or any Jupyter environment

## Setup

### 1. Install the dependencies

From the repository root:

```bash
uv sync --python 3.12
```

This creates `.venv/` with the exact versions from `uv.lock`:

| Package | Version |
|---|---|
| openai | 3.57.0 |
| gradio | 6.32.0 |
| pydantic | 2.14.4 |
| python-dotenv | 1.2.4 |
| ipykernel | 7.4.0 |

### 2. Set the environment

Copy `.env.example` to `.env` in the repository root, then add your key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

`.env` is listed in `.gitignore` and is never committed. `.env.example` contains only the variable name.

### 3. Open the notebook

1. Open `personal_chat/personal_chat.ipynb`.
2. Select the kernel **`.venv` (Python 3.12)**.
3. Run the cells from top to bottom.

The notebook must run with `personal_chat/` as its working folder, because it reads `data/` and writes `logs/` relative to it. VS Code and Cursor do this by default.

Without VS Code: `cd personal_chat` then `uv run --with jupyter jupyter lab`.

## Running the chat

1. Run all cells up to and including **Part C → "The chat with the Critic and the revision loop"**.
2. The chat opens in the browser, at a local Gradio address such as `http://127.0.0.1:7860`.
3. Every question goes through the full Actor → Critic → revision loop.
4. The chat shows only the questions and the final answers. Drafts, Critic decisions and feedback go to `personal_chat/logs/run_log.json`.
5. Run the `demo.close()` cell below the chat before launching another chat.

The Part A chat, earlier in the notebook, is the Actor alone, without the Critic.

## Running the tests (Part D)

Run the **Part D** cells in order:

| Scenario | How it runs | Expected |
|---|---|---|
| 1 - Existing information | In the Part D Gradio chat, with scenario "1" selected | Approved answer. `show_source_lines()` prints the supporting line from the sources. |
| 2 - Follow-up question | Same chat, scenario "2": two questions, the second leans on the first answer | The context is kept |
| 3 - Missing information | Same chat, scenario "3" | The answer says the information is not available, without inventing facts |
| 4 - Rejection and improvement | Cell: a faulty test draft is injected as attempt 1 (`run_controlled_test(..., first_draft=...)`) | The Critic rejects it with reasons, and the revised answer is approved |
| 5 - Attempts exhausted | Cell: a mock Critic that always rejects (`mock_critic=always_reject`) | 3 attempts, then the "no approved answer" notice |

- **Clearing the chat:** clear it (🗑) before each new scenario, so that one scenario's history does not leak into the next.
- **Mock results:** scenario 5 is a **control-flow check with a mock Critic**, not a model result. Its log entry says so under `controlled_test` and `critic_model`.
- **Results summary:** the final cell prints a table of results against expectations, with each scenario marked LLM or mock Critic. It saves all scenario entries to `personal_chat/logs/part_d_results.json`.

## Models and settings

| Setting | Value |
|---|---|
| Actor model | `claude-opus-5-5` |
| Critic model | `claude-opus-5-5` (same model, separate calls and separate prompts) |
| API access | OpenAI Python SDK (`chat.completions`) with `base_url="https://api.anthropic.com/v1/"` (Anthropic's OpenAI-compatible endpoint) and the Anthropic API key |
| Critic output | `chat.completions.parse(response_format=Evaluation)`: a strict JSON schema, validated with Pydantic |
| `max_tokens` | 16000 per call |
| Max attempts per question | 3, including the first |
| Temperature, thinking | Model defaults. Claude Opus 5.5 thinks adaptively by default, and the thinking is not returned. `reasoning_effort` is not set, because the compatible endpoint ignores it. |
| Scenario 5 Critic | `always_reject`, a mock function (no model call) |

On any of these technical errors, the question stops with a Hebrew error notice and the reason is logged. It is never treated as an approval:
- a failed API call;
- an empty or cut-off answer;
- Critic output that cannot be parsed or validated.

## Project structure

```
.
├── README.md
├── pyproject.toml, uv.lock          # dependencies (uv)
├── .env.example                     # variable names only - copy to .env
├── personal_chat/
│   ├── personal_chat.ipynb          # the whole implementation, Parts A-D
│   ├── data/
│   │   ├── linkedin.txt             # professional background (sample profile)
│   │   └── summary.txt              # personal summary, about half a page (sample profile)
│   ├── logs/
│   │   ├── run_log.json             # review log: every question, attempt, decision and feedback
│   │   └── part_d_results.json      # the Part D scenario entries
│   └── report/
│       ├── architecture.png         # architecture diagram
│       ├── draw_architecture.py     # regenerates the diagram
│       └── hand_checked_asnwers     # manual check of approved answers against the sources
└── references/                      # course material (lectures, labs, assignment instructions)
```

The architecture diagram can be regenerated from `personal_chat/` with:

```bash
uv run --no-project --with matplotlib python report/draw_architecture.py report/architecture.png
```

### Log format (`run_log.json`)

Each question is one entry with:
- `scenario_id`, `question`, `actor_model`, `critic_model`;
- `final_status`: `approved` / `max_attempts_reached` / `technical_error`;
- `shown_to_user`;
- an `attempts` list.

Each attempt records:
- `attempt`, `candidate_answer`, `evaluation_completed`, `is_acceptable`, `feedback`;
- on a technical error, `evaluation_completed: false` and `error`, with no content decision recorded.

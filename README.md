# Echoes: Ghost in the Machine 👻

An offline-first ghost-story studio for Hacktoberfest 2026 Week 4. Echoes uses a locally running open-weight language model through [Ollama](https://ollama.com/) to create spooky stories from a theme, mood, setting, and optional seed detail.

## Features

- Local model inference through Ollama; no hosted AI API key required.
- Choose from six themes and five moods.
- Generate flash, short, or longer stories.
- Download the generated story as Markdown.
- Swap the model by changing the model tag in the sidebar.
- Clear error messages for a missing Ollama server or unavailable model.

## Requirements

- Python 3.10 or newer
- Ollama installed and running
- Enough RAM for your selected model (the default `gemma3:1b` is a small model, but performance depends on your computer)

## Setup

### 1. Install Ollama

Install Ollama from https://ollama.com/download for your operating system, then start the Ollama app/service.

### 2. Download an open-weight model

Open Terminal / PowerShell and run:

```bash
ollama pull gemma3:1b
```

This downloads the model once. The model files take disk space; the first download requires internet. After the model is downloaded, generation can run locally.

If you already have another Ollama model, enter its exact tag in the app's **Model settings** sidebar.

### 3. Set up Python

From this project folder:

**Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, use Command Prompt:
```bat
py -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
streamlit run app.py
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Streamlit opens the app in your browser, usually at http://localhost:8501.

## Troubleshooting

- **“Can't reach Ollama”**: Start the Ollama application/service and retry. On most installations its local API is available at `http://localhost:11434`.
- **Model not found**: Run `ollama pull gemma3:1b`, or enter the exact tag of a model already installed.
- **Slow generation**: Choose Flash length or use a smaller model supported by your machine.
- **No internet after setup**: Ollama model downloads and Python package installation need internet initially. Once everything is installed and the model is downloaded, story generation can work offline.

## How it works

1. The Streamlit UI collects story choices.
2. `app.py` turns those choices into a prompt.
3. The app sends the prompt to the Ollama local API at `localhost:11434`.
4. Ollama runs the selected model and returns the story.
5. The UI displays the result and offers a Markdown download.

## Open innovation

The core generation runs on an open-weight model that users can run on their own hardware. That makes model swapping possible, reduces dependence on a proprietary hosted API, and keeps prompts on the user's machine under the default setup. The model is downloaded from its provider, so check the model's license and terms for your intended use.

## Project structure

```text
ghost_in_the_machine/
├── app.py
├── requirements.txt
├── README.md
├── SAMPLE_OUTPUT.md
├── DEV_SUBMISSION_DRAFT.md
└── LICENSE
```

## Challenge submission checklist

- Run the app and generate your own story.
- Capture a screenshot of the working app and generated result.
- Publish a DEV post using the official submission template/tags required by the challenge.
- Link your code repository and demo/screenshots.
- Be accurate about what you tested; do not claim offline operation until you have tested after downloading the model and dependencies.

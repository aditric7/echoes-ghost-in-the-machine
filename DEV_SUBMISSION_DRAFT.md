# Echoes: Ghost in the Machine — a local AI that writes ghost stories

**Tags:** #devchallenge #hf26challenge

For Hacktoberfest's “Ghost in the Machine” theme, I built **Echoes**, a small ghost-story studio powered by a locally running open-weight language model.

## What I built

Echoes is a Streamlit app where a user chooses a haunting theme, mood, setting, and optional detail. The app sends those choices to Ollama running on the same computer, displays the generated story, and lets the user download it as Markdown.

## Why open AI matters here

A spooky writing tool does not need to send personal prompts to a hosted AI service. With Echoes, the model runs locally after setup. Users can inspect the code, switch to another Ollama-supported model, and keep their prompts on their own machine under the default configuration. This also avoids needing a paid hosted-model API key.

The trade-off is that users must install Ollama, download a model, and have hardware capable of running it. The first model download requires internet access; the app can work offline after setup if all dependencies and model files are already present.

## How it works

1. Streamlit collects the story settings.
2. Python creates a structured prompt.
3. The app calls Ollama's local generation API.
4. The chosen local model returns a story.
5. The user can save the result as Markdown.

## Run it

```bash
ollama pull gemma3:1b
pip install -r requirements.txt
streamlit run app.py
```

See the README for full Windows, macOS, and Linux setup steps.

## What I learned

This project explores a practical benefit of open-weight AI: the ability to run inference locally and replace the model without redesigning the whole interface. It also makes the limitations visible—local inference depends on the user's hardware, and model output can vary.

## Demo

Add a screenshot or short screen recording of your own running app here.

## Repository

Add your public repository URL here.

---

**Before publishing:** Run the app yourself, generate a fresh story, replace the sample demo section with a real screenshot, and verify the challenge's current submission rules and tags on DEV.

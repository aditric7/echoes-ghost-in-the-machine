import os

import requests
import streamlit as st

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_MODEL = os.getenv("HF_MODEL", "google/gemma-2-2b-it").strip()

st.set_page_config(
    page_title="Echoes | Ghost in the Machine",
    page_icon="👻",
    layout="centered",
)

st.title("👻 Echoes: Ghost in the Machine")

if HF_TOKEN:
    st.caption("A ghost-story studio powered by an open-weight Gemma model through Hugging Face Inference Providers.")
    st.markdown(
        "Create a small haunting from a memory, a place, or a strange machine log. "
        "In this deployed version, your prompt is sent to the configured inference provider "
        "to generate a story. Do not enter private or sensitive information."
    )
    model = HF_MODEL
    mode = "cloud"
else:
    st.caption("An offline-first ghost-story studio powered by a local open-weight language model.")
    st.markdown(
        "Create a small haunting from a memory, a place, or a strange machine log. "
        "Your prompt is sent to the Ollama server running on your own computer—not to a hosted AI API."
    )
    mode = "local"
    with st.sidebar:
        st.header("Local model settings")
        model = st.text_input(
            "Ollama model tag",
            value="gemma3:1b",
            help="Use a model you have downloaded with `ollama pull`.",
        )
        st.caption("Default: Gemma 3 1B. A different locally installed Ollama model can be entered here.")
        st.divider()
        st.markdown("**Privacy note**")
        st.write(
            "In local mode, prompts stay on this computer as long as Ollama is running locally "
            "and you do not add external integrations."
        )

col1, col2 = st.columns(2)
with col1:
    theme = st.selectbox(
        "Theme",
        [
            "Haunted machine",
            "Forgotten memory",
            "Abandoned website",
            "Midnight train",
            "Old family house",
            "Lost programming language",
        ],
    )
    mood = st.selectbox(
        "Mood",
        [
            "Quietly unsettling",
            "Gothic and dramatic",
            "Folklore-inspired",
            "Melancholic",
            "Creepy but not gory",
        ],
    )
with col2:
    setting = st.text_input("Setting", value="a computer lab after midnight")
    length = st.select_slider(
        "Story length",
        options=["Flash (150 words)", "Short (300 words)", "Long (500 words)"],
        value="Short (300 words)",
    )

seed = st.text_area(
    "A detail to weave into the story (optional)",
    placeholder="Example: every night, one terminal displays a username that no longer exists.",
    height=100,
)

generate = st.button("Generate the haunting", type="primary", use_container_width=True)

if generate:
    word_target = length.split(" (")[1].rstrip(")")
    prompt = f"""Write an original, polished ghost story for the theme 'Ghost in the Machine'.
Theme: {theme}
Mood: {mood}
Setting: {setting or 'an unnamed place after midnight'}
Approximate length: {word_target}
User-provided detail: {seed or 'Invent one subtle, eerie detail.'}
Requirements:
- Give it a title.
- Build atmosphere and a clear narrative arc.
- Keep it suitable for a general audience; no graphic violence.
- Do not claim the story is based on real events.
- Return only the title and story, with no preamble.
"""

    with st.spinner(f"Consulting {'hosted' if mode == 'cloud' else 'local'} model {model}…"):
        try:
            if mode == "cloud":
                response = requests.post(
                    HF_API_URL,
                    headers={"Authorization": f"Bearer {HF_TOKEN}"},
                    json={
                        "model": model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a creative fiction writer specializing in atmospheric, original ghost stories.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "max_tokens": 1100 if word_target == "500 words" else 700,
                        "temperature": 0.8,
                    },
                    timeout=180,
                )
                response.raise_for_status()
                data = response.json()
                story = (
                    data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                    .strip()
                )
            else:
                response = requests.post(
                    OLLAMA_URL,
                    json={"model": model, "prompt": prompt, "stream": False},
                    timeout=240,
                )
                response.raise_for_status()
                story = response.json().get("response", "").strip()

            if not story:
                st.error("The model returned an empty response. Please try again.")
            else:
                st.subheader("The machine remembers…")
                st.markdown(story)
                st.download_button(
                    "Download story as Markdown",
                    data=story,
                    file_name="echoes_story.md",
                    mime="text/markdown",
                )
                if mode == "cloud":
                    st.caption(f"Generated with `{model}` through Hugging Face Inference Providers.")
                else:
                    st.caption(f"Generated locally with `{model}` via Ollama.")

        except requests.exceptions.Timeout:
            st.error("The model took too long to respond. Try a shorter story and try again.")
        except requests.exceptions.HTTPError as exc:
            status = response.status_code
            if status in (401, 403):
                st.error(
                    "The inference provider rejected the Hugging Face token or model access. "
                    "Check that HF_TOKEN is valid and has inference permissions."
                )
            elif status == 402:
                st.error(
                    "The inference provider reports that credits or billing are required. "
                    "Check your Hugging Face Inference Providers account and available credits."
                )
            elif mode == "local":
                st.error(
                    "Ollama returned an error. Confirm Ollama is running and the selected model is installed. "
                    f"Details: {exc}"
                )
            else:
                st.error(
                    f"The hosted model request failed (HTTP {status}). "
                    "Check the model/provider availability and your Hugging Face account settings."
                )
        except requests.exceptions.ConnectionError:
            if mode == "local":
                st.error(
                    "Can't reach Ollama. Start Ollama and run `ollama pull gemma3:1b` in your terminal."
                )
            else:
                st.error(
                    "Could not reach the hosted inference endpoint. Check the deployment logs and try again."
                )
        except Exception as exc:
            st.error(f"Something went wrong: {exc}")

st.divider()
if mode == "cloud":
    st.markdown(
        "**Why open AI?** The deployed app uses an open-weight Gemma model through a hosted inference provider. "
        "The hosted version sends prompts to that provider; use local mode with Ollama when you want prompts "
        "to stay on your own computer."
    )
else:
    st.markdown(
        "**Why open AI?** This local version uses a locally running open-weight model. "
        "You can inspect the code, swap models, and create stories without sending prompts to a third-party hosted AI service."
    )

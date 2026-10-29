import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/generate"

st.set_page_config(page_title="Echoes | Ghost in the Machine", page_icon="👻", layout="centered")

st.title("👻 Echoes: Ghost in the Machine")
st.caption("An offline-first ghost-story studio powered by a local open-weight language model.")
st.markdown(
    "Create a small haunting from a memory, a place, or a strange machine log. "
    "Your prompt is sent to the Ollama server running on your own computer—not to a hosted AI API."
)

with st.sidebar:
    st.header("Model settings")
    model = st.text_input("Ollama model tag", value="gemma3:1b", help="Use a model you have downloaded with `ollama pull`.")
    st.caption("Default: Gemma 3 1B. A different locally installed Ollama model can be entered here.")
    st.divider()
    st.markdown("**Privacy note**")
    st.write("Story prompts stay local as long as Ollama is running on this computer and you do not add external integrations.")

col1, col2 = st.columns(2)
with col1:
    theme = st.selectbox("Theme", ["Haunted machine", "Forgotten memory", "Abandoned website", "Midnight train", "Old family house", "Lost programming language"])
    mood = st.selectbox("Mood", ["Quietly unsettling", "Gothic and dramatic", "Folklore-inspired", "Melancholic", "Creepy but not gory"])
with col2:
    setting = st.text_input("Setting", value="a computer lab after midnight")
    length = st.select_slider("Story length", options=["Flash (150 words)", "Short (300 words)", "Long (500 words)"], value="Short (300 words)")

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
    with st.spinner(f"Consulting local model {model}…"):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=240,
            )
            response.raise_for_status()
            story = response.json().get("response", "").strip()
            if not story:
                st.error("The model returned an empty response. Try again or select another installed model.")
            else:
                st.subheader("The machine remembers…")
                st.markdown(story)
                st.download_button("Download story as Markdown", data=story, file_name="echoes_story.md", mime="text/markdown")
                st.caption(f"Generated locally with `{model}` via Ollama.")
        except requests.exceptions.ConnectionError:
            st.error("Can't reach Ollama. Install and start Ollama, then run `ollama pull gemma3:1b` in your terminal.")
        except requests.exceptions.Timeout:
            st.error("The model took too long to respond. Try a shorter story or a smaller local model.")
        except requests.exceptions.HTTPError as exc:
            details = ""
            try:
                details = response.text
            except Exception:
                pass
            st.error(f"Ollama returned an error: {exc}. {details}")
        except Exception as exc:
            st.error(f"Something went wrong: {exc}")

st.divider()
st.markdown("**Why open AI?** This demo uses a locally running open-weight model. You can inspect the code, swap models, and create stories without sending prompts to a third-party hosted AI service.")

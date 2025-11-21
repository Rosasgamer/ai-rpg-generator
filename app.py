# app.py
import streamlit as st
from huggingface_hub import InferenceClient

# --- Streamlit UI ---
st.set_page_config(page_title="AI Game Master", layout="centered")
st.title("🧙 AI Game Master Assistant")
st.write("Generate creative content for your TTRPG campaign!")

# === SIDEBAR ===
with st.sidebar:
    st.header("⚙️ Generator Settings")
    temperature = st.slider("Creativity Level", 0.1, 1.0, 0.7, 0.1, 
                           help="Lower = more predictable, Higher = more creative")
    max_tokens = st.slider("Response Length", 100, 400, 250, 50,
                          help="Maximum length of generated content")
    st.markdown("---")
    st.markdown("### Model Info")
    st.markdown("**Zephyr-7B**: NPCs, Dialogue, Stories")
    st.markdown("**Mistral-7B**: Quests, Magic Items")
    st.markdown("---")
    st.markdown("Built with 🧙♂️ for GMs")

if "HF_API_TOKEN" not in st.secrets:
    st.error("❌ HF_API_TOKEN not found in secrets")
    st.stop()

HF_API_TOKEN = st.secrets["HF_API_TOKEN"]
client = InferenceClient(token=HF_API_TOKEN)

# Model assignments based on content type
MODEL_MAPPING = {
    "NPC": "HuggingFaceH4/zephyr-7b-beta",           
    "NPC History": "HuggingFaceH4/zephyr-7b-beta",   
    "Village": "HuggingFaceH4/zephyr-7b-beta",       
    "Area": "HuggingFaceH4/zephyr-7b-beta",
    "Dialogue": "HuggingFaceH4/zephyr-7b-beta",      
    "Quest": "mistralai/Mistral-7B-Instruct-v0.2",   
    "Magic Item": "mistralai/Mistral-7B-Instruct-v0.2",  
}

# Expanded content types
content_type = st.selectbox(
    "What do you want to generate?",
    ("NPC", "NPC History", "Village", "Area", "Dialogue", "Quest", "Magic Item")
)

user_input = st.text_input(
    "Give me a theme, race, or keyword:",
    placeholder="e.g., Elf, Betrayal, Fiery Sword, Ancient Ruins"
)


if st.button("Generate!"):
    if user_input:
        with st.spinner(f"Creating {content_type}..."):
            # Select the appropriate model
            model = MODEL_MAPPING[content_type]
            
            # Custom prompts for each content type
            prompts = {
                "NPC": f"Create a compelling NPC with personality, appearance, and motivation. Theme: {user_input}. Write exactly 3-4 sentences. Be concise..",
                "NPC History": f"Write a rich backstory for an NPC. Include origins, key events, and secrets. Theme: {user_input}. Write exactly 4 sentences maximum..",
                "Village": f"Describe a fantasy village or settlement. Include location, inhabitants, and unique features. Theme: {user_input}. Write exactly 3 to 5 sentences maximum.", 
                "Area": f"Describe a area with details and interest points. Theme: {user_input}. 3-5 sentences. Keep it brief.",
                "Dialogue": f"Write an engaging dialogue snippet between characters. Theme: {user_input}. Keep it to 3-4 lines.",
                "Quest": f"Create a structured quest with objective, challenges, and reward. Theme: {user_input}. Write exactly 4 sentences.",
                "Magic Item": f"Design a balanced magic item with description, abilities, and lore. Theme: {user_input}. Write exactly 3 sentences."
            }
            
            prompt = prompts[content_type]
            
            try:
                messages = [{"role": "user", "content": prompt}]
                response = client.chat_completion(
                    messages, 
                    model=model, 
                    max_tokens=max_tokens,      # ← Use sidebar value
                    temperature=temperature     # ← Use sidebar value
                )
                st.success(f"**{content_type}:**")
                st.write(generated_text)
                st.caption(f"🤖 Generated with {model.split('/')[-1]}")
                
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
    else:
        st.warning("Please enter a theme or keyword.")
import streamlit as st
from config import MODEL

def display_model_info():
    """Display model information banner with dark theme"""
    if "wen:14b" in MODEL or "wen:7b" in MODEL:
        st.markdown(f"""
        <div class="model-info-banner">
            <p>🚀 Using <strong>{MODEL}</strong> - ByteDance's Wen model is ready to generate detailed to-do lists</p>
        </div>
        """, unsafe_allow_html=True)
    elif "llama3" in MODEL:
        st.markdown(f"""
        <div class="model-info-banner">
            <p>🦙 Using <strong>{MODEL}</strong> - Meta's latest LLaMA model is optimized for task planning</p>
        </div>
        """, unsafe_allow_html=True)
    elif MODEL == "deepseek-r1":
        st.markdown(f"""
        <div class="model-info-banner">
            <p>🧠 Using <strong>deepseek-r1</strong> - Known for detailed and well-structured outputs</p>
        </div>
        """, unsafe_allow_html=True)
    elif "mistral" in MODEL:
        st.markdown(f"""
        <div class="model-info-banner">
            <p>🔮 Using <strong>{MODEL}</strong> - Efficient open-source model with good overall quality</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="model-info-banner">
            <p>🤖 Using <strong>{MODEL}</strong> - AI-powered to-do list generation</p>
        </div>
        """, unsafe_allow_html=True)
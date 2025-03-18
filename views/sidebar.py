import streamlit as st
from helpers.api_helpers import get_model_payload
from config import AVAILABLE_MODELS, MODEL_DESCRIPTIONS

def render_sidebar():
    """Render the sidebar with styling matching the reference images exactly"""
    with st.sidebar:
        # App name/logo styled to match reference
        st.markdown('<div class="sidebar-title">Todo<span class="highlight">AI</span></div>', unsafe_allow_html=True)
        st.markdown("<p style='opacity: 0.6; margin-top: 0; font-size: 0.9rem;'>Powered by local AI models</p>", unsafe_allow_html=True)

        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

        # Model configuration section
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <span style="background: rgba(60, 60, 60, 0.5); width: 28px; height: 28px; 
                  display: inline-flex; align-items: center; justify-content: center;
                  border-radius: 8px; margin-right: 10px;">
                🤖
            </span>
            <h3 style="margin: 0; font-size: 1.1rem;">Model Configuration</h3>
        </div>
        """, unsafe_allow_html=True)

        # Label for model selection
        st.markdown('<p style="margin: 0 0 5px 0; font-size: 0.9rem; opacity: 0.7;">Select AI Model</p>', unsafe_allow_html=True)

        # Model selection with simplified styling
        selected_model = st.selectbox(
            "",  # Empty label since we're using custom label above
            options=AVAILABLE_MODELS,
            index=0
        )

        # Update the global MODEL variable
        global MODEL
        import config
        config.MODEL = selected_model

        # Model information display in card matching reference
        if selected_model in MODEL_DESCRIPTIONS:
            st.markdown(f"""
            <div class="model-info">
                <p class="title">{selected_model}</p>
                <p class="description">{MODEL_DESCRIPTIONS[selected_model]}</p>
            </div>
            """, unsafe_allow_html=True)

        # Advanced model settings
        with st.expander("Advanced Settings"):
            model_temp = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1,
                                   help="Higher values make output more random, lower values more deterministic")
            model_top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.05,
                                    help="Controls diversity via nucleus sampling")
            max_tokens = st.slider("Max Tokens", min_value=100, max_value=4000, value=2000, step=100,
                                   help="Maximum length of the generated response")

        # Store the model settings in session state
        if 'model_settings' not in st.session_state:
            st.session_state.model_settings = {
                'temperature': model_temp,
                'top_p': model_top_p,
                'max_tokens': max_tokens
            }
        else:
            st.session_state.model_settings = {
                'temperature': model_temp,
                'top_p': model_top_p,
                'max_tokens': max_tokens
            }

        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

        # Saved lists section
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <span style="background: rgba(60, 60, 60, 0.5); width: 28px; height: 28px; 
                  display: inline-flex; align-items: center; justify-content: center;
                  border-radius: 8px; margin-right: 10px;">
                💾
            </span>
            <h3 style="margin: 0; font-size: 1.1rem;">Saved Lists</h3>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.to_do_lists:
            st.markdown('<p style="margin: 0 0 5px 0; font-size: 0.9rem; opacity: 0.7;">Select a list to load</p>', unsafe_allow_html=True)
            selected_list = st.selectbox(
                "",  # Empty label since we're using custom label above
                options=[list_data["name"] for list_data in st.session_state.to_do_lists],
                index=0,
                key="saved_list_selector"
            )

            # Add some space
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📂 Load", use_container_width=True):
                    selected_list_data = next((item for item in st.session_state.to_do_lists if item["name"] == selected_list), None)
                    if selected_list_data:
                        st.session_state.current_list = selected_list_data["content"]
                        st.session_state.list_name = selected_list_data["name"]
                        # Clear the deleted tasks list when loading a new list
                        st.session_state.deleted_tasks = []
                        st.rerun()

            with col2:
                if st.button("🗑️ Delete", use_container_width=True):
                    from helpers.todo_helpers import delete_todo_list
                    delete_todo_list(selected_list)
        else:
            st.markdown("""
            <div style="background: #2a2a2a; padding: 15px; border-radius: 8px;
                      text-align: center;">
                <p style="margin: 0; opacity: 0.7; font-size: 0.9rem;">No saved lists found</p>
                <p style="margin: 5px 0 0 0; font-size: 0.8rem; opacity: 0.5;">Create a list and save it to see it here</p>
            </div>
            """, unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div style="position: fixed; bottom: 20px; left: 20px; right: 20px; text-align: center; opacity: 0.5; font-size: 0.8rem;">
            <p style="margin: 0;">AI-Powered To-Do List Generator</p>
            <p style="margin: 5px 0 0 0;">v1.0.0</p>
        </div>
        """, unsafe_allow_html=True)
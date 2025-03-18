import streamlit as st

def render_help_tab():
    """Render the Help tab content with dark theme"""
    # Header with icon
    st.markdown("""
    <h2 style="font-size: 1.4rem; margin-bottom: 20px; display: flex; align-items: center;">
        <span style="background: rgba(60, 60, 60, 0.5); width: 32px; height: 32px; display: inline-flex; 
              align-items: center; justify-content: center; border-radius: 8px; margin-right: 10px;">
            ❓
        </span>
        Help & Information
    </h2>
    """, unsafe_allow_html=True)

    # Create a grid of help cards
    col1, col2 = st.columns(2)

    with col1:
        # Getting Started card
        st.markdown("""
        <div style="background: rgba(50, 50, 50, 0.3); padding: 20px; border-radius: 10px;
                  margin-bottom: 20px; border: 1px solid rgba(80, 80, 80, 0.3); height: 100%;">
            <h3 style="margin: 0 0 15px 0; display: flex; align-items: center; font-size: 1.1rem;">
                <span style="background: rgba(60, 60, 60, 0.5); width: 28px; height: 28px;
                      display: inline-flex; align-items: center; justify-content: center;
                      border-radius: 8px; margin-right: 10px;">
                    🚀
                </span>
                Getting Started
            </h3>
            <p style="margin-bottom: 15px; font-size: 0.9rem; opacity: 0.8;">
                Welcome to the AI-Powered To-Do List Generator! This application helps you create structured 
                and actionable to-do lists using AI.
            </p>
            <ol style="margin-bottom: 0; padding-left: 20px; font-size: 0.9rem; opacity: 0.8;">
                <li style="margin-bottom: 8px;"><strong>Create a new list:</strong> Go to the 'Create New' tab, describe your project or tasks, and click "Generate To-Do List"</li>
                <li style="margin-bottom: 8px;"><strong>Manage your tasks:</strong> In the 'Manage Current' tab, you can view, edit, complete, and delete tasks</li>
                <li><strong>Restore deleted tasks:</strong> In the 'Deleted Tasks' tab, you can view and restore tasks you've previously deleted</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        # Tips card
        st.markdown("""
        <div style="background: rgba(50, 50, 50, 0.3); padding: 20px; border-radius: 10px;
                  margin-bottom: 20px; border: 1px solid rgba(80, 80, 80, 0.3); height: 100%;">
            <h3 style="margin: 0 0 15px 0; display: flex; align-items: center; font-size: 1.1rem;">
                <span style="background: rgba(60, 60, 60, 0.5); width: 28px; height: 28px;
                      display: inline-flex; align-items: center; justify-content: center;
                      border-radius: 8px; margin-right: 10px;">
                    💡
                </span>
                Tips for Better Results
            </h3>
            <p style="margin-bottom: 10px; font-size: 0.9rem; opacity: 0.8;">
                To get the most out of the AI-generated to-do lists:
            </p>
            <ul style="margin-bottom: 0; padding-left: 20px; font-size: 0.9rem; opacity: 0.8;">
                <li style="margin-bottom: 8px;"><strong>Be specific</strong> in your task description - include details about your project, goals, and constraints</li>
                <li style="margin-bottom: 8px;"><strong>Use the additional instructions</strong> field to guide the AI - for example, you might specify to focus on a particular methodology or timeframe</li>
                <li style="margin-bottom: 8px;"><strong>Experiment with different models</strong> - some models may work better for certain types of tasks or projects</li>
                <li><strong>Adjust temperature</strong> in Advanced Model Settings - higher means more creative outputs, lower means more consistent outputs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Model Settings card
        st.markdown("""
        <div style="background: rgba(50, 50, 50, 0.3); padding: 20px; border-radius: 10px;
                  margin-bottom: 20px; border: 1px solid rgba(80, 80, 80, 0.3); height: 100%;">
            <h3 style="margin: 0 0 15px 0; display: flex; align-items: center; font-size: 1.1rem;">
                <span style="background: rgba(60, 60, 60, 0.5); width: 28px; height: 28px;
                      display: inline-flex; align-items: center; justify-content: center;
                      border-radius: 8px; margin-right: 10px;">
                    🔧
                </span>
                Model Settings
            </h3>
            <p style="margin-bottom: 10px; font-size: 0.9rem; opacity: 0.8;">
                You can customize the AI model behavior in the sidebar:
            </p>
            <ul style="margin-bottom: 0; padding-left: 20px; font-size: 0.9rem; opacity: 0.8;">
                <li style="margin-bottom: 8px;"><strong>Model selection:</strong> Choose from various AI models with different capabilities</li>
                <li style="margin-bottom: 8px;"><strong>Temperature:</strong> Controls randomness - higher values (0.7-1.0) produce more varied outputs, lower values (0.2-0.5) produce more focused outputs</li>
                <li style="margin-bottom: 8px;"><strong>Top P:</strong> Controls diversity via nucleus sampling - lower values produce more focused results</li>
                <li><strong>Max Tokens:</strong> Maximum length of the response - increase for longer to-do lists</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Saving & Exporting card
        st.markdown("""
        <div style="background: rgba(50, 50, 50, 0.3); padding: 20px; border-radius: 10px;
                  margin-bottom: 20px; border: 1px solid rgba(80, 80, 80, 0.3); height: 100%;">
            <h3 style="margin: 0 0 15px 0; display: flex; align-items: center; font-size: 1.1rem;">
                <span style="background: rgba(60, 60, 60, 0.5); width: 28px; height: 28px;
                      display: inline-flex; align-items: center; justify-content: center;
                      border-radius: 8px; margin-right: 10px;">
                    💾
                </span>
                Saving & Exporting
            </h3>
            <p style="margin-bottom: 10px; font-size: 0.9rem; opacity: 0.8;">
                You have multiple options for saving and exporting your to-do lists:
            </p>
            <ul style="margin-bottom: 0; padding-left: 20px; font-size: 0.9rem; opacity: 0.8;">
                <li style="margin-bottom: 8px;"><strong>Save To-Do List:</strong> Saves your list to the application so you can access it later from the sidebar</li>
                <li style="margin-bottom: 8px;"><strong>Export as Excel:</strong> Creates a formatted Excel file with priority color-coding and proper formatting</li>
                <li><strong>Export as Text:</strong> Exports a simple text file with your to-do list in Markdown format</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Troubleshooting card - full width
    st.markdown("""
    <div style="background: rgba(50, 50, 50, 0.3); padding: 20px; border-radius: 10px;
              margin: 20px 0; border: 1px solid rgba(80, 80, 80, 0.3);">
        <h3 style="margin: 0 0 15px 0; display: flex; align-items: center; font-size: 1.1rem;">
            <span style="background: rgba(60, 60, 60, 0.5); width: 28px; height: 28px;
                  display: inline-flex; align-items: center; justify-content: center;
                  border-radius: 8px; margin-right: 10px;">
                ⚠️
            </span>
            Troubleshooting
        </h3>
        <p style="margin-bottom: 10px; font-size: 0.9rem; opacity: 0.8;">
            Common issues and solutions:
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; font-size: 0.9rem; opacity: 0.8;">
            <div>
                <p style="margin: 0 0 5px 0; font-weight: 600;">Ollama Connection Error</p>
                <p style="margin: 0; opacity: 0.9;">Make sure Ollama is running on your computer at http://localhost:11434</p>
            </div>
            <div>
                <p style="margin: 0 0 5px 0; font-weight: 600;">Missing Excel Formatting</p>
                <p style="margin: 0; opacity: 0.9;">Install the xlsxwriter package with <code>pip install xlsxwriter</code></p>
            </div>
            <div>
                <p style="margin: 0 0 5px 0; font-weight: 600;">List Parsing Issues</p>
                <p style="margin: 0; opacity: 0.9;">If the list cannot be parsed into interactive format, try generating a new list with more standard formatting</p>
            </div>
            <div>
                <p style="margin: 0 0 5px 0; font-weight: 600;">Model Not Available</p>
                <p style="margin: 0; opacity: 0.9;">Make sure you have pulled the selected model in Ollama with <code>ollama pull [model_name]</code></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # About section
    st.markdown("""
    <div style="background: rgba(40, 40, 40, 0.3); padding: 20px; border-radius: 10px;
              margin: 30px 0; border: 1px solid rgba(70, 70, 70, 0.3); text-align: center;">
        <h3 style="margin-top: 0; font-size: 1.1rem;">About This Application</h3>
        <p style="opacity: 0.7; font-size: 0.9rem;">
            This AI-Powered To-Do List Generator was built with Streamlit and integrates with Ollama to provide 
            local AI-generated to-do lists. It features a responsive UI with interactive task management, 
            analytics, and multiple export options.
        </p>
        <div style="background: linear-gradient(135deg, rgba(140, 97, 255, 0.2), rgba(91, 138, 245, 0.2));
                  display: inline-block; padding: 8px 16px; margin-top: 10px;
                  border-radius: 20px; font-size: 0.8rem; opacity: 0.9;">
            v1.0.0
        </div>
    </div>
    """, unsafe_allow_html=True)
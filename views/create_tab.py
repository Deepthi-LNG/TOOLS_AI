import streamlit as st
import datetime
from helpers.todo_helpers import generate_to_do_list

def render_create_tab():
    """Render the Create New tab content with date support"""
    st.markdown("""
    <p style="margin-bottom: 15px; font-size: 0.95rem; opacity: 0.8;">
        Enter your task details below. Be specific about your project goals, requirements, and deadlines.
    </p>
    """, unsafe_allow_html=True)
    
    # User input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Task entry area with label
        st.markdown('<p style="margin-bottom: 5px; font-size: 0.9rem;">Enter your task details:</p>', unsafe_allow_html=True)
        task_description = st.text_area(
            "",
            placeholder="Describe your project or tasks in detail...",
            height=250
        )
    
    with col2:
        st.markdown("""
        <div style="background: rgba(50, 50, 50, 0.3); padding: 12px; border-radius: 8px; margin-bottom: 15px; border: 1px solid rgba(80, 80, 80, 0.3);">
            <h3 style="margin: 0 0 10px 0; font-size: 1rem;">
                ⚙️ Options
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # List name input
        st.markdown('<p style="margin-bottom: 5px; font-size: 0.9rem;">List Name:</p>', unsafe_allow_html=True)
        list_name = st.text_input("", placeholder="My Project Tasks")
        
        # Due date selector
        st.markdown('<p style="margin: 15px 0 5px 0; font-size: 0.9rem;">Due Date (Optional):</p>', unsafe_allow_html=True)
        due_date = st.date_input(
            "",
            value=None,
            min_value=datetime.date.today(),
            max_value=datetime.date.today() + datetime.timedelta(days=365),
            help="Set a target completion date for all tasks"
        )
        
        # Additional instructions input
        st.markdown('<p style="margin: 15px 0 5px 0; font-size: 0.9rem;">Additional Instructions (Optional):</p>', unsafe_allow_html=True)
        extra_instructions = st.text_area(
            "",
            placeholder="E.g., Focus on agile methodology, prioritize backend tasks...",
            height=110
        )
    
    # Add some spacing
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    # Create a container for the button with custom styling
    button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
    
    with button_col2:
        if st.button("🔮 Generate To-Do List", use_container_width=True):
            if task_description.strip():
                with st.spinner("Generating your professional to-do list..."):
                    # Pass the due date to the generation function if selected
                    due_date_value = due_date if due_date is not None else None
                    to_do_list = generate_to_do_list(task_description, extra_instructions, due_date_value)
                    st.session_state.current_list = to_do_list
                    st.session_state.list_name = list_name if list_name else "Untitled List"
                    # Clear the deleted tasks list when creating a new list
                    st.session_state.deleted_tasks = []
                    st.session_state.task_df = None  # Reset to force parsing of new list
                    st.rerun()
            else:
                st.warning("⚠️ Please enter a task description.")
    
    # Tips section with dark theme
    st.markdown("<div style='height: 25px'></div>", unsafe_allow_html=True)
    
    with st.expander("💡 Tips for better results"):
        st.markdown("""
        - **Be specific** about your project requirements and goals
        - Include **deadlines** and timeframes for better task scheduling
        - Mention any **dependencies** or **constraints**
        - Specify if you want tasks organized in a particular way
        - Include preferred **methodologies** (Agile, Waterfall, etc.)
        - Provide details about **priorities** or important milestones
        """)
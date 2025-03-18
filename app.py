import streamlit as st
import os
import datetime
from helpers.ui_helpers import add_custom_css
from helpers.todo_helpers import (
    generate_to_do_list, save_todo_list, parse_todo_to_df, 
    convert_df_to_text, load_saved_lists, delete_todo_list,
    export_as_excel
)

# Check for required packages and inform user if missing
missing_packages = []
try:
    import xlsxwriter
except ImportError:
    missing_packages.append("xlsxwriter")

# Session state initialization
if 'to_do_lists' not in st.session_state:
    st.session_state.to_do_lists = []
if 'current_list' not in st.session_state:
    st.session_state.current_list = ""
if 'list_name' not in st.session_state:
    st.session_state.list_name = ""
if 'task_df' not in st.session_state:
    st.session_state.task_df = None
if 'deleted_tasks' not in st.session_state:
    st.session_state.deleted_tasks = []

# Load saved lists when app starts
load_saved_lists()

# Streamlit UI
st.set_page_config(
    page_title="AI-Powered To-Do List Generator",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for refined styling
add_custom_css()

from views.sidebar import render_sidebar
from views.create_tab import render_create_tab
from views.manage_tab import render_manage_tab
from views.calendar_tab import render_calendar_tab
from views.deleted_tasks_tab import render_deleted_tasks_tab
from views.help_tab import render_help_tab
from views.model_info import display_model_info

# Sidebar
render_sidebar()

# Main content
st.markdown("""
<h1 style="font-size: 1.8rem; font-weight: 700; margin-bottom: 5px; display: flex; align-items: center;">
    <span style="display: inline-block; margin-right: 12px; font-size: 1.8rem;">📋</span>
    AI-Powered To-Do List Generator
</h1>
<p style="margin-top: 0; opacity: 0.6; font-size: 0.95rem; margin-bottom: 20px;">
    Generate structured and actionable to-do lists using AI
</p>
""", unsafe_allow_html=True)

# Display model info banner
display_model_info()

# Missing packages warning with refined styling
if missing_packages:
    st.markdown(f"""
    <div style="background: rgba(255, 152, 0, 0.1); padding: 15px; border-radius: 8px;
              margin: 20px 0; border: 1px solid rgba(255, 152, 0, 0.2);">
        <p style="margin: 0; display: flex; align-items: center; font-size: 0.9rem; opacity: 0.9;">
            <span style="background: rgba(255, 152, 0, 0.2); width: 24px; height: 24px;
                  display: inline-flex; align-items: center; justify-content: center;
                  border-radius: 6px; margin-right: 10px;">
                ⚠️
            </span>
            Some features may be limited. Please install the following packages for full functionality: {', '.join(missing_packages)}
        </p>
        <div style="background: rgba(30, 30, 30, 0.5); margin-top: 10px; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 0.85rem;">
            pip install {' '.join(missing_packages)}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main tabs with refined styling - Added Calendar tab
tabs = st.tabs(["Create New", "Manage Current", "Calendar", "Deleted Tasks", "Help"])

# Create New Tab
with tabs[0]:
    render_create_tab()

# Manage Current Tab
with tabs[1]:
    render_manage_tab()
    
# Calendar Tab - New!
with tabs[2]:
    render_calendar_tab()

# Deleted Tasks Tab
with tabs[3]:
    render_deleted_tasks_tab()

# Help Tab
with tabs[4]:
    render_help_tab()

# Footer
st.markdown("""
<div style="position: fixed; bottom: 20px; left: 0; right: 0; text-align: center; opacity: 0.5; font-size: 0.8rem; pointer-events: none;">
    <p style="margin: 0;">AI-Powered To-Do List Generator</p>
    <p style="margin: 5px 0 0 0;">v1.0.0</p>
</div>
""", unsafe_allow_html=True)
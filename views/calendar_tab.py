import streamlit as st
import pandas as pd
import datetime
from helpers.todo_helpers import get_tasks_for_date

def render_calendar_tab():
    """Render the Calendar tab content with date-based task filtering"""
    st.markdown("""
    <div class="section-header">
        <span class="icon">📅</span>
        <h3>Calendar View</h3>
    </div>
    <p style="margin: -5px 0 15px 0; opacity: 0.6; font-size: 0.9rem;">
        View tasks by due date and schedule new tasks
    </p>
    """, unsafe_allow_html=True)
    
    # Create a two-column layout for calendar and tasks
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Date selector
        st.markdown('<p style="margin-bottom: 5px; font-size: 0.9rem;">Select Date:</p>', unsafe_allow_html=True)
        selected_date = st.date_input("", 
                                     value=datetime.date.today(),
                                     min_value=datetime.date.today() - datetime.timedelta(days=365),
                                     max_value=datetime.date.today() + datetime.timedelta(days=365))
        
        # Option to create a new task for this date
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        st.markdown('<p style="margin-bottom: 5px; font-size: 0.9rem;">Create a task for this date:</p>', unsafe_allow_html=True)
        
        # Simple form to add a task directly to the date
        task_title = st.text_input("", placeholder="Task description")
        
        # Priority selection
        priority_options = ["High", "Medium", "Low"]
        selected_priority = st.selectbox("Priority", options=priority_options, index=1)
        
        # Category selection - if we have existing categories, offer those
        categories = ["General"]
        
        if st.session_state.task_df is not None and not st.session_state.task_df.empty:
            existing_categories = st.session_state.task_df["Category"].unique().tolist()
            categories.extend([cat for cat in existing_categories if cat != "General"])
            categories = list(set(categories))  # Remove duplicates
        
        selected_category = st.selectbox("Category", options=categories, index=0)
        
        # Add task button
        if st.button("Add Task", use_container_width=True):
            if task_title.strip():
                # Add the task to the dataframe
                if st.session_state.task_df is None:
                    # Create a new dataframe if none exists
                    st.session_state.task_df = pd.DataFrame(columns=[
                        "ID", "Category", "Task", "Priority", "Time Estimate", 
                        "Due Date", "Dependencies", "Completed", "Deleted"
                    ])
                
                # Create a new task ID
                new_task_id = f"task_{len(st.session_state.task_df)}"
                
                # Add the new task to the dataframe
                new_task = {
                    "ID": new_task_id,
                    "Category": selected_category,
                    "Task": task_title,
                    "Priority": selected_priority,
                    "Time Estimate": "",
                    "Due Date": selected_date.strftime('%Y-%m-%d'),
                    "Dependencies": "",
                    "Completed": False,
                    "Deleted": False
                }
                
                st.session_state.task_df = pd.concat([st.session_state.task_df, pd.DataFrame([new_task])], ignore_index=True)
                
                # Show success message
                st.success(f"Added task: {task_title}")
                
                # Clear the input field for next task - using rerun() is deprecated, use empty() instead
                task_title = ""
                st.rerun()  # Using st.rerun() instead of experimental_rerun()
            else:
                st.warning("Please enter a task description")
    
    with col2:
        # Display tasks for the selected date
        tasks_for_date = get_tasks_for_date(st.session_state.task_df, selected_date)
        
        # Selected date display
        date_str = selected_date.strftime('%A, %B %d, %Y')
        st.markdown(f"""
        <div style="background: rgba(50, 50, 50, 0.3); padding: 10px 15px; border-radius: 8px; margin-bottom: 15px;">
            <h3 style="margin: 0; font-size: 1.1rem;">Tasks for {date_str}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if tasks_for_date.empty:
            st.markdown("""
            <div style="background: #1e1e1e; padding: 30px; border-radius: 8px; text-align: center;">
                <p style="opacity: 0.7; margin: 0;">No tasks scheduled for this date</p>
                <p style="opacity: 0.5; font-size: 0.9rem; margin-top: 10px;">Add a task using the form on the left</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Configure the display of tasks for this date
            col_config = {
                "ID": st.column_config.TextColumn(
                    "ID",
                    help="Task identifier",
                    width="small",
                    required=True,
                    disabled=True
                ),
                "Completed": st.column_config.CheckboxColumn(
                    "Completed",
                    help="Mark tasks as completed",
                    default=False,
                ),
                "Task": st.column_config.TextColumn(
                    "Task Description",
                    help="The task to be completed",
                    width="large",
                ),
                "Priority": st.column_config.SelectboxColumn(
                    "Priority",
                    help="Task priority level",
                    width="medium",
                    options=["High", "Medium", "Low"],
                    required=True,
                ),
                "Category": st.column_config.TextColumn(
                    "Category",
                    help="Task category",
                    width="medium",
                )
            }
            
            # Show the data editor for daily tasks
            edited_df = st.data_editor(
                tasks_for_date,
                use_container_width=True,
                hide_index=True,
                column_config=col_config,
                column_order=["ID", "Completed", "Task", "Priority", "Category"],
                disabled=["ID"]
            )
            
            # Update the main dataframe with any edits made
            if st.session_state.task_df is not None:
                for _, row in edited_df.iterrows():
                    task_id = row["ID"]
                    if task_id in st.session_state.task_df["ID"].values:
                        idx = st.session_state.task_df[st.session_state.task_df["ID"] == task_id].index[0]
                        for col in edited_df.columns:
                            if col in st.session_state.task_df.columns:
                                st.session_state.task_df.at[idx, col] = row[col]
                                
    # Calendar overview - show next 7 days task count
    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <span class="icon">📊</span>
        <h3>Week Overview</h3>
    </div>
    <p style="margin: -5px 0 15px 0; opacity: 0.6; font-size: 0.9rem;">
        Task summary for the upcoming week
    </p>
    """, unsafe_allow_html=True)
    
    # Create columns for the next 7 days
    week_cols = st.columns(7)
    today = datetime.date.today()
    
    # For each day in the next week, show date and task count
    for i, col in enumerate(week_cols):
        day = today + datetime.timedelta(days=i)
        day_name = day.strftime("%a")
        day_number = day.strftime("%d")
        
        # Count tasks for this day
        day_task_count = 0
        if st.session_state.task_df is not None and not st.session_state.task_df.empty:
            day_tasks = get_tasks_for_date(st.session_state.task_df, day)
            day_task_count = len(day_tasks)
        
        # Highlight current selected day
        is_selected = day == selected_date
        bg_color = "rgba(83, 111, 237, 0.3)" if is_selected else "rgba(50, 50, 50, 0.3)"
        border = "1px solid rgba(83, 111, 237, 0.6)" if is_selected else "1px solid rgba(80, 80, 80, 0.3)"
        
        with col:
            # Day card with task count
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 10px; border-radius: 8px; 
                      text-align: center; border: {border}; cursor: pointer;"
                 onclick="document.querySelector('input[type=date]').value = '{day.strftime('%Y-%m-%d')}'; 
                          document.querySelector('input[type=date]').dispatchEvent(new Event('change'));">
                <p style="margin: 0; font-size: 0.9rem; font-weight: 600;">{day_name}</p>
                <p style="margin: 5px 0; font-size: 1.2rem; font-weight: 600;">{day_number}</p>
                <div style="background: rgba(83, 111, 237, 0.2); border-radius: 50%; width: 28px; height: 28px; 
                          margin: 5px auto 0; display: flex; align-items: center; justify-content: center;">
                    <p style="margin: 0; font-size: 0.9rem;">{day_task_count}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
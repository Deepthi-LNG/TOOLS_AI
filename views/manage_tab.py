import streamlit as st
import pandas as pd
from helpers.todo_helpers import (
    parse_todo_to_df, convert_df_to_text, 
    save_todo_list, export_as_excel
)

def render_manage_tab():
    """Render the Manage Current tab content with date support"""
    if st.session_state.current_list:
        # Display list name with styled header
        st.markdown(f"""
        <h2 style="font-size: 1.4rem; margin-bottom: 20px; display: flex; align-items: center;">
            <span style="background: rgba(60, 60, 60, 0.5); width: 32px; height: 32px; display: inline-flex; 
                  align-items: center; justify-content: center; border-radius: 8px; margin-right: 10px;">
                📝
            </span>
            {st.session_state.list_name}
        </h2>
        """, unsafe_allow_html=True)
        
        # Show the original text
        with st.expander("View Raw To-Do List", expanded=True):
            st.markdown(st.session_state.current_list)
        
        # Try to parse into a dataframe for interactive editing
        try:
            # Only parse if we don't already have a dataframe or if it's a newly loaded list
            if st.session_state.task_df is None:
                todo_df = parse_todo_to_df(st.session_state.current_list)
                st.session_state.task_df = todo_df
            else:
                todo_df = st.session_state.task_df
            
            # Interactive table header
            st.markdown("""
            <div class="section-header">
                <span class="icon">📊</span>
                <h3>Interactive Task Management</h3>
            </div>
            <p style="margin: -5px 0 15px 0; opacity: 0.6; font-size: 0.9rem;">
                Edit, complete, or delete tasks as needed
            </p>
            """, unsafe_allow_html=True)
            
            # Add delete button to each row
            todo_df_display = todo_df[~todo_df["Deleted"]].copy()  # Only show non-deleted tasks
            
            # Create columns for the data editor with Due Date added
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
                "Delete": st.column_config.CheckboxColumn(
                    "Delete",
                    help="Mark tasks for deletion",
                    default=False,
                ),
                "Priority": st.column_config.SelectboxColumn(
                    "Priority",
                    help="Task priority level",
                    width="medium",
                    options=["High", "Medium", "Low"],
                    required=True,
                ),
                "Task": st.column_config.TextColumn(
                    "Task Description",
                    help="The task to be completed",
                    width="large",
                ),
                "Category": st.column_config.TextColumn(
                    "Category",
                    help="Task category",
                    width="medium",
                ),
                "Due Date": st.column_config.DateColumn(
                    "Due Date",
                    help="Task due date",
                    min_value=None,
                    max_value=None,
                    format="YYYY-MM-DD",
                    step=1,
                ),
                "Time Estimate": st.column_config.TextColumn(
                    "Time Estimate",
                    help="Estimated time to complete",
                    width="medium",
                ),
                "Dependencies": st.column_config.TextColumn(
                    "Dependencies",
                    help="Task dependencies",
                    width="medium",
                ),
            }
            
            # If "Delete" column doesn't exist, add it
            if "Delete" not in todo_df_display.columns:
                todo_df_display["Delete"] = False
            
            # Show the data editor without the Deleted column
            edited_df = st.data_editor(
                todo_df_display,
                use_container_width=True,
                hide_index=True,
                column_config=col_config,
                column_order=["ID", "Completed", "Delete", "Task", "Priority", "Category", "Due Date", "Time Estimate", "Dependencies"],
                disabled=["ID"]
            )
            
            # Process any deleted tasks
            if "Delete" in edited_df.columns:
                tasks_to_delete = edited_df[edited_df["Delete"]]["ID"].tolist()
                if tasks_to_delete:
                    # Update the main dataframe
                    for task_id in tasks_to_delete:
                        if task_id in todo_df["ID"].values:
                            idx = todo_df[todo_df["ID"] == task_id].index[0]
                            todo_df.at[idx, "Deleted"] = True
                            st.session_state.deleted_tasks.append(todo_df.loc[idx].to_dict())
                    
                    # Update the display dataframe to reflect deletions
                    edited_df = edited_df[~edited_df["Delete"]]
                
                # Remove the Delete column from the edited dataframe
                if "Delete" in edited_df.columns:
                    edited_df = edited_df.drop("Delete", axis=1)
            
            # Update the non-deleted tasks in the main dataframe with any other edits
            for _, row in edited_df.iterrows():
                task_id = row["ID"]
                if task_id in todo_df["ID"].values:
                    idx = todo_df[todo_df["ID"] == task_id].index[0]
                    for col in edited_df.columns:
                        if col != "Delete" and col in todo_df.columns:
                            todo_df.at[idx, col] = row[col]
            
            # Update the session state
            st.session_state.task_df = todo_df
            
            # Add spacing before the analytics
            st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
            
            # Analytics section header
            st.markdown("""
            <div class="section-header">
                <span class="icon">📈</span>
                <h3>Task Analytics</h3>
            </div>
            <p style="margin: -5px 0 15px 0; opacity: 0.6; font-size: 0.9rem;">
                Summary of progress and task distribution
            </p>
            """, unsafe_allow_html=True)
            
            # Analytics cards with due date information
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                completed = edited_df["Completed"].sum()
                total = len(edited_df)
                completion_rate = completed / total * 100 if total > 0 else 0
                st.metric("Completion Rate", f"{completion_rate:.1f}%", f"{completed}/{total} tasks")
            
            with col2:
                priority_counts = edited_df["Priority"].value_counts()
                st.metric(
                    "High Priority Tasks", 
                    f"{priority_counts.get('High', 0)}", 
                    f"{priority_counts.get('High', 0)/total*100:.1f}% of total" if total > 0 else "0%"
                )
            
            with col3:
                categories = edited_df["Category"].nunique()
                st.metric("Task Categories", f"{categories}")
                
            with col4:
                # Count tasks with due dates
                tasks_with_dates = edited_df['Due Date'].notna().sum()
                st.metric(
                    "Scheduled Tasks", 
                    f"{tasks_with_dates}", 
                    f"{tasks_with_dates/total*100:.1f}% of total" if total > 0 else "0%"
                )
            
            # Add spacing before export options
            st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
            
            # Export options header to match reference image
            st.markdown("""
            <div class="section-header">
                <span class="icon">💾</span>
                <h3>Export Options</h3>
            </div>
            <p style="margin: -5px 0 15px 0; opacity: 0.6; font-size: 0.9rem;">
                Save or export your to-do list in different formats
            </p>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Plain save button - no gradient
                if st.button("💾 Save To-Do List", use_container_width=True):
                    # Update the content based on the current dataframe state
                    updated_content = convert_df_to_text(todo_df)
                    st.session_state.current_list = updated_content
                    
                    # Save with the updated content
                    success = save_todo_list(st.session_state.list_name, updated_content)
                    if success:
                        st.success(f"✅ Saved '{st.session_state.list_name}' successfully!")
            
            with col2:
                try:
                    # Add gradient class for Excel button
                    excel_data = export_as_excel(todo_df)
                    st.markdown("""
                    <style>
                    div[data-testid="column"][data-column-index="1"] > div > div > div > div > div > button {
                        background: linear-gradient(90deg, #536FED, #59C2FF) !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📊 Export as Excel",
                        data=excel_data,
                        file_name=f"{st.session_state.list_name.replace(' ', '_')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                except Exception as excel_error:
                    st.warning(f"Excel export issue: {str(excel_error)}")
                    st.info("Install xlsxwriter library for better Excel exports: pip install xlsxwriter")
            
            with col3:
                # Add gradient class for Text button
                st.markdown("""
                <style>
                div[data-testid="column"][data-column-index="2"] > div > div > div > div > div > button {
                    background: linear-gradient(90deg, #536FED, #59C2FF) !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Get updated text based on current dataframe
                updated_text = convert_df_to_text(todo_df)
                st.download_button(
                    label="📝 Export as Text",
                    data=updated_text,
                    file_name=f"{st.session_state.list_name.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
        except Exception as e:
            st.warning(f"Could not parse list into interactive format: {str(e)}")
            
            # Simple export option for plain text
            st.download_button(
                label="📥 Download To-Do List",
                data=st.session_state.current_list,
                file_name=f"{st.session_state.list_name.replace(' ', '_')}.txt",
                mime="text/plain"
            )
    else:
        # Empty state with styling
        st.markdown("""
        <div style="background: #1e1e1e; padding: 40px 30px; border-radius: 12px;
                  margin: 50px 0; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 20px; opacity: 0.7;">📋</div>
            <h3 style="margin-bottom: 15px; font-size: 1.3rem;">No To-Do List Yet</h3>
            <p style="opacity: 0.7; max-width: 600px; margin: 0 auto 20px auto; font-size: 0.95rem;">
                Generate a new to-do list in the 'Create New' tab or load a saved list from the sidebar.
            </p>
            <div style="background: #2a2a2a; display: inline-block; padding: 8px 16px;
                      border-radius: 8px; font-size: 0.9rem; opacity: 0.7;">
                Click on 'Create New' to get started
            </div>
        </div>
        """, unsafe_allow_html=True)
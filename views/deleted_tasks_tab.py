import streamlit as st
import pandas as pd

def render_deleted_tasks_tab():
    """Render the Deleted Tasks tab content with dark theme"""
    # Header with icon
    st.markdown("""
    <h2 style="font-size: 1.4rem; margin-bottom: 20px; display: flex; align-items: center;">
        <span style="background: rgba(60, 60, 60, 0.5); width: 32px; height: 32px; display: inline-flex; 
              align-items: center; justify-content: center; border-radius: 8px; margin-right: 10px;">
            🗑️
        </span>
        Deleted Tasks
    </h2>
    """, unsafe_allow_html=True)

    if st.session_state.deleted_tasks:
        # Create a dataframe from deleted tasks
        deleted_df = pd.DataFrame(st.session_state.deleted_tasks)

        # Remove unnecessary columns for display
        if "Deleted" in deleted_df.columns:
            deleted_df = deleted_df.drop("Deleted", axis=1)

        # Display header for deleted tasks section
        st.markdown("""
        <div style="background: rgba(50, 50, 50, 0.3); padding: 15px; border-radius: 10px;
                  margin: 20px 0; border: 1px solid rgba(80, 80, 80, 0.4);">
            <h3 style="margin: 0; display: flex; align-items: center; font-size: 1.1rem;">
                <span style="background: rgba(60, 60, 60, 0.5); width: 28px; height: 28px;
                      display: inline-flex; align-items: center; justify-content: center;
                      border-radius: 8px; margin-right: 10px;">
                    ♻️
                </span>
                Deleted Tasks Recovery
            </h3>
            <p style="margin: 8px 0 0 38px; opacity: 0.6; font-size: 0.9rem;">
                These tasks have been deleted from your current list
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Configure columns for the deleted tasks view
        col_config = {
            "ID": st.column_config.TextColumn(
                "ID",
                help="Task identifier",
                width="small",
                disabled=True
            ),
            "Restore": st.column_config.CheckboxColumn(
                "Restore",
                help="Restore task to the active list",
                default=False,
            ),
            "Task": st.column_config.TextColumn(
                "Task Description",
                help="The deleted task",
                width="large",
            ),
            "Priority": st.column_config.TextColumn(
                "Priority",
                help="Task priority level",
                width="medium",
            ),
            "Category": st.column_config.TextColumn(
                "Category",
                help="Task category",
                width="medium",
            ),
        }

        # Add a Restore column for user interaction
        deleted_df["Restore"] = False

        # Show the data editor for deleted tasks
        restored_df = st.data_editor(
            deleted_df,
            use_container_width=True,
            hide_index=True,
            column_config=col_config,
            column_order=["ID", "Restore", "Task", "Priority", "Category", "Time Estimate", "Dependencies"],
            disabled=["ID", "Task", "Priority", "Category", "Time Estimate", "Dependencies"]
        )

        # Process any restored tasks
        tasks_to_restore = restored_df[restored_df["Restore"]]["ID"].tolist()
        if tasks_to_restore:
            # Get the main dataframe
            if st.session_state.task_df is not None:
                for task_id in tasks_to_restore:
                    # Mark as not deleted in the main dataframe
                    if task_id in st.session_state.task_df["ID"].values:
                        idx = st.session_state.task_df[st.session_state.task_df["ID"] == task_id].index[0]
                        st.session_state.task_df.at[idx, "Deleted"] = False

                    # Remove from deleted_tasks list
                    st.session_state.deleted_tasks = [task for task in st.session_state.deleted_tasks
                                                      if task["ID"] != task_id]

                st.success(f"✅ Restored {len(tasks_to_restore)} task(s)")
                st.rerun()

        # Add spacing before permanent delete option
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

        # Destructive actions container
        st.markdown("""
        <div style="background: rgba(244, 67, 54, 0.1); padding: 15px; border-radius: 10px;
                  margin: 20px 0; border: 1px solid rgba(244, 67, 54, 0.3);">
            <h3 style="margin: 0; display: flex; align-items: center; font-size: 1.1rem; color: rgba(255, 255, 255, 0.87);">
                <span style="background: rgba(244, 67, 54, 0.2); width: 28px; height: 28px;
                      display: inline-flex; align-items: center; justify-content: center;
                      border-radius: 8px; margin-right: 10px;">
                    ⚠️
                </span>
                Danger Zone
            </h3>
            <p style="margin: 8px 0 0 38px; opacity: 0.7; font-size: 0.9rem;">
                Permanently delete all tasks - this action cannot be undone
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Option to permanently delete tasks
        col1, col2 = st.columns([2, 1])

        with col1:
            confirm = st.checkbox("I understand this action cannot be undone", key="confirm_perm_delete")

        with col2:
            if confirm:
                if st.button("🗑️ Permanently Delete All", use_container_width=True):
                    st.session_state.deleted_tasks = []
                    st.success("All deleted tasks have been permanently removed")
                    st.rerun()
    else:
        # Empty state with dark theme styling
        st.markdown("""
        <div class="empty-state-card">
            <div style="font-size: 48px; margin-bottom: 20px; opacity: 0.7;">🗑️</div>
            <h3 style="margin-bottom: 15px; font-size: 1.3rem;">No Deleted Tasks</h3>
            <p style="opacity: 0.7; max-width: 600px; margin: 0 auto 20px auto;">
                When you delete tasks from your to-do list, they will appear here for recovery.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Instructions with dark theme styling
        st.markdown("""
        <div style="background: rgba(50, 50, 50, 0.3); padding: 20px; border-radius: 10px;
                  margin: 30px 0; border: 1px solid rgba(80, 80, 80, 0.3);">
            <h3 style="margin-top: 0; font-size: 1.1rem;">How to Delete Tasks</h3>
            <ol style="margin-bottom: 0; padding-left: 20px; opacity: 0.8;">
                <li style="margin-bottom: 8px;">Go to the <strong>Manage Current</strong> tab</li>
                <li style="margin-bottom: 8px;">Check the <strong>Delete</strong> checkbox next to any task you want to remove</li>
                <li style="margin-bottom: 8px;">The task will be moved to this <strong>Deleted Tasks</strong> tab</li>
                <li>You can restore tasks from here if needed</li>
            </ol>
        </div>
        
        <div style="background: rgba(255, 152, 0, 0.1); padding: 15px; border-radius: 10px;
                  margin-top: 20px; border: 1px solid rgba(255, 152, 0, 0.2);">
            <p style="margin: 0; display: flex; align-items: center; font-size: 0.9rem; opacity: 0.8;">
                <span style="background: rgba(255, 152, 0, 0.2); width: 24px; height: 24px;
                      display: inline-flex; align-items: center; justify-content: center;
                      border-radius: 6px; margin-right: 10px;">
                    ⚠️
                </span>
                Deleted tasks are not permanently removed until you choose to do so.
            </p>
        </div>
        """, unsafe_allow_html=True)
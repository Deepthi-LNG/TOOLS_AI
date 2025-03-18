import streamlit as st
import pandas as pd
import requests
import datetime
import json
import os
from io import BytesIO
from config import OLLAMA_API, HEADERS, MODEL, SYSTEM_PROMPT

# Function to generate To-Do List
def generate_to_do_list(task_description, extra_instructions=""):
    full_prompt = task_description
    if extra_instructions:
        full_prompt += f"\n\nAdditional instructions: {extra_instructions}"

    # Add explicit instruction to filter out thinking sections
    full_prompt += "\n\nIMPORTANT: DO NOT include any <think> sections or thinking process in your response. ONLY provide the formatted to-do list."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": full_prompt}
    ]

    # Use the get_model_payload function if it exists, otherwise use default payload
    try:
        from helpers.api_helpers import get_model_payload
        payload = get_model_payload(messages)
    except:
        payload = {
            "model": MODEL,
            "messages": messages,
            "stream": False
        }

    try:
        response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
        response.raise_for_status()
        json_response = response.json()
        content = json_response.get("message", {}).get("content", "No to-do list found.")

        # Remove any <think> sections from the response
        if "<think>" in content:
            # Find all <think> sections and remove them
            while "<think>" in content and "</think>" in content:
                think_start = content.find("<think>")
                think_end = content.find("</think>", think_start) + 8  # +8 to include "</think>"
                if think_start >= 0 and think_end >= 0:
                    content = content[:think_start] + content[think_end:]

        return content.strip()
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error parsing response: {str(e)}"

# Function to save to-do list
def save_todo_list(name, content, df=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update content if we have an edited dataframe
    if df is not None:
        content = convert_df_to_text(df)

    new_list = {
        "name": name,
        "content": content,
        "created_at": timestamp,
        "id": len(st.session_state.to_do_lists) + 1
    }

    # Check if this list name already exists and update it
    existing_index = next((i for i, item in enumerate(st.session_state.to_do_lists)
                           if item["name"] == name), None)

    if existing_index is not None:
        st.session_state.to_do_lists[existing_index] = new_list
    else:
        st.session_state.to_do_lists.append(new_list)

    # Save to JSON file
    if not os.path.exists("saved_lists"):
        os.makedirs("saved_lists")

    try:
        with open("saved_lists/todo_lists.json", "w") as f:
            json.dump(st.session_state.to_do_lists, f)
    except Exception as e:
        st.error(f"Failed to save list: {str(e)}")

    return True

# Function to convert dataframe back to formatted text
def convert_df_to_text(df):
    if df.empty:
        return "No tasks available."

    # Group by category
    grouped = df.groupby("Category")

    lines = []
    task_num = 1

    for category, group in grouped:
        lines.append(f"## {category}")

        for _, row in group.iterrows():
            # Skip deleted tasks
            if row.get("Deleted", False):
                continue

            priority_str = f"[{row['Priority'].upper()}]" if row["Priority"] else ""
            time_str = f"({row['Time Estimate']})" if row["Time Estimate"] else ""
            dep_str = f" - {row['Dependencies']}" if row["Dependencies"] else ""

            task_line = f"{task_num}. {priority_str} {row['Task']} {time_str}{dep_str}".strip()
            lines.append(task_line)
            task_num += 1

    return "\n".join(lines)

# Function to load saved lists
def load_saved_lists():
    if os.path.exists("saved_lists/todo_lists.json"):
        try:
            with open("saved_lists/todo_lists.json", "r") as f:
                st.session_state.to_do_lists = json.load(f)
        except Exception as e:
            st.error(f"Failed to load saved lists: {str(e)}")

# Function to parse to-do list into dataframe
def parse_todo_to_df(todo_text):
    lines = [line.strip() for line in todo_text.split('\n') if line.strip()]
    data = []

    current_category = "Uncategorized"

    for line in lines:
        # Check if it's a category header
        if line.startswith('#'):
            current_category = line.lstrip('#').strip()
            continue

        # Try to parse numbered items
        if any(line.startswith(f"{i}.") for i in range(1, 100)):
            # Extract priority if present
            priority = "Medium"
            if "[HIGH]" in line:
                priority = "High"
            elif "[MEDIUM]" in line:
                priority = "Medium"
            elif "[LOW]" in line:
                priority = "Low"

            # Extract time estimate if present
            time_estimate = ""
            if "(" in line and ")" in line:
                time_part = line[line.find("(")+1:line.find(")")]
                if any(unit in time_part.lower() for unit in ["hour", "minute", "day"]):
                    time_estimate = time_part

            # Extract dependencies if present
            dependencies = ""
            if "Requires" in line or "requires" in line or "dependent on" in line:
                dep_part = line.split("Requires", 1)[-1] if "Requires" in line else line.split("requires", 1)[-1]
                dependencies = dep_part.strip()

            # Extract the task description
            task_desc = line
            # Remove priority tag
            for tag in ["[HIGH]", "[MEDIUM]", "[LOW]"]:
                task_desc = task_desc.replace(tag, "")

            # Remove time estimate
            if "(" in task_desc and ")" in task_desc:
                time_part = task_desc[task_desc.find("("): task_desc.find(")")+1]
                task_desc = task_desc.replace(time_part, "")

            # Remove dependencies
            if "Requires" in task_desc:
                task_desc = task_desc.split("Requires")[0]
            elif "requires" in task_desc:
                task_desc = task_desc.split("requires")[0]

            # Remove task number and clean up
            for i in range(1, 100):
                if task_desc.startswith(f"{i}."):
                    task_desc = task_desc.replace(f"{i}.", "", 1)
                    break

            task_desc = task_desc.strip()

            # Generate a unique task ID
            task_id = f"task_{len(data)}"

            data.append({
                "ID": task_id,
                "Category": current_category,
                "Task": task_desc,
                "Priority": priority,
                "Time Estimate": time_estimate,
                "Dependencies": dependencies,
                "Completed": False,
                "Deleted": False
            })

    return pd.DataFrame(data)

# Function to delete a to-do list
def delete_todo_list(list_name):
    st.session_state.to_do_lists = [item for item in st.session_state.to_do_lists if item["name"] != list_name]
    # Save updated lists to JSON file
    try:
        with open("saved_lists/todo_lists.json", "w") as f:
            json.dump(st.session_state.to_do_lists, f)

        # Use a colored success message in a dedicated container
        st.markdown(f"""
        <div style="background: #2f6c3e; padding: 16px; border-radius: 8px; color: white;">
            <p style="margin: 0;">Deleted list '{list_name}' successfully!</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to delete list: {str(e)}")

# Function to export as Excel
def export_as_excel(df):
    # Filter out deleted tasks
    export_df = df[~df.get("Deleted", False)].copy()

    # Remove the Deleted column if it exists
    if "Deleted" in export_df.columns:
        export_df = export_df.drop("Deleted", axis=1)

    # Remove the ID column if it exists
    if "ID" in export_df.columns:
        export_df = export_df.drop("ID", axis=1)

    try:
        # Try using xlsxwriter
        import xlsxwriter
        output = BytesIO()

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            export_df.to_excel(writer, sheet_name='To-Do List', index=False)
            workbook = writer.book
            worksheet = writer.sheets['To-Do List']

            # Add formats
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })

            high_priority_format = workbook.add_format({
                'bg_color': '#FFC7CE',
                'font_color': '#9C0006'
            })

            medium_priority_format = workbook.add_format({
                'bg_color': '#FFEB9C',
                'font_color': '#9C6500'
            })

            low_priority_format = workbook.add_format({
                'bg_color': '#C6EFCE',
                'font_color': '#006100'
            })

            # Write header with format
            for col_num, value in enumerate(export_df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # Set column widths
            worksheet.set_column('A:A', 15)  # Category
            worksheet.set_column('B:B', 40)  # Task
            worksheet.set_column('C:C', 10)  # Priority
            worksheet.set_column('D:D', 15)  # Time Estimate
            worksheet.set_column('E:E', 20)  # Dependencies
            worksheet.set_column('F:F', 12)  # Completed

            # Apply conditional formatting for priorities
            priority_col = export_df.columns.get_loc('Priority')
            worksheet.conditional_format(1, priority_col, len(export_df)+1, priority_col, {
                'type': 'cell',
                'criteria': 'equal to',
                'value': '"High"',
                'format': high_priority_format
            })

            worksheet.conditional_format(1, priority_col, len(export_df)+1, priority_col, {
                'type': 'cell',
                'criteria': 'equal to',
                'value': '"Medium"',
                'format': medium_priority_format
            })

            worksheet.conditional_format(1, priority_col, len(export_df)+1, priority_col, {
                'type': 'cell',
                'criteria': 'equal to',
                'value': '"Low"',
                'format': low_priority_format
            })

        return output.getvalue()

    except ImportError:
        # Fallback to basic Excel export without formatting if xlsxwriter is not installed
        st.warning("For better Excel exports, install xlsxwriter: pip install xlsxwriter")
        output = BytesIO()
        export_df.to_excel(output, index=False)
        return output.getvalue()
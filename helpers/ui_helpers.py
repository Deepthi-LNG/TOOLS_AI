import streamlit as st

def add_custom_css():
    """Add custom CSS with refined dark theme and calendar styling"""
    css = """
    <style>
        /* Dark Theme with Glass Effects */
        :root {
            --bg-dark: #121212;
            --bg-card: #1e1e1e;
            --bg-sidebar: #1a1a1a;
            --glass-bg: rgba(40, 40, 40, 0.4);
            --glass-border: 1px solid rgba(80, 80, 80, 0.3);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            --text-primary: rgba(255, 255, 255, 0.87);
            --text-secondary: rgba(255, 255, 255, 0.6);
            --accent-purple: #8c61ff;
            --accent-blue-start: #536FED;
            --accent-blue-end: #59C2FF;
            --accent-blue: #5b8af5;
            --accent-teal: #4cceac;
            --accent-pink: #ec4899;
            --success-color: #4CAF50;
            --warning-color: #ff9800;
            --error-color: #f44336;
            --radius-lg: 12px;
            --radius-md: 8px;
            --radius-sm: 4px;
        }
        
        /* Global styling with dark background */
        body {
            background-color: var(--bg-dark) !important;
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
            margin: 0;
            line-height: 1.6;
        }
        
        /* Main content area styling */
        .main .block-container {
            background: var(--bg-dark);
            padding: 2rem;
            margin: 1rem 0;
        }
        
        /* Headers styling */
        h1, h2, h3, h4, h5 {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
        }
        
        /* Markdown text */
        .stMarkdown {
            color: var(--text-primary) !important;
        }
        
        p {
            color: var(--text-secondary) !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: var(--bg-dark) !important;
            border-right: 1px solid rgba(60, 60, 60, 0.5);
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: var(--text-primary) !important;
        }
        
        /* Button styling exact match */
        .stButton button {
            background: #2a2a2a !important;
            color: var(--text-primary) !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 0.6rem 1.2rem !important;
            transition: all 0.3s ease !important;
            font-weight: 500 !important;
            text-transform: none !important;
            font-size: 0.9rem !important;
        }

        .stButton button:hover {
            background: #333333 !important;
        }
        
        /* Export button styling - gradient blue to green */
        .download-button-blue-gradient button,
        .stDownloadButton button {
            background: linear-gradient(90deg, var(--accent-blue-start), var(--accent-blue-end)) !important;
            color: white !important;
            font-weight: 500 !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 0.6rem 1.2rem !important;
            transition: all 0.3s ease !important;
            font-size: 0.9rem !important;
        }
        
        /* Fix for select boxes to match reference image */
        [data-baseweb="select"] {
            background: #2a2a2a !important;
            border-radius: var(--radius-md) !important;
            border: none !important;
            overflow: hidden !important;
        }
        
        [data-baseweb="select"] > div {
            background: #2a2a2a !important;
            border: none !important;
            height: auto !important;
            min-height: 38px !important;
        }
        
        [data-baseweb="select"] > div > div:first-child {
            background: transparent !important;
            border: none !important;
            padding: 0.4rem 0.7rem !important;
            color: var(--text-primary) !important;
        }
        
        [data-baseweb="select"] > div > div:nth-child(2) {
            display: none !important;
        }
        
        [data-baseweb="select"] > div > div:last-child {
            background: transparent !important;
            border: none !important;
            padding: 0.4rem 0.7rem !important;
        }
        
        /* Dropdown options */
        [data-baseweb="menu"] {
            background: #2a2a2a !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            margin-top: 0.25rem !important;
        }
        
        [data-baseweb="menu"] ul {
            padding: 0.25rem !important;
        }
        
        [data-baseweb="menu"] ul li {
            color: var(--text-primary) !important;
            border-radius: var(--radius-sm) !important;
        }
        
        [data-baseweb="menu"] ul li:hover {
            background: #333333 !important;
        }
        
        /* Fix label issues */
        .stSelectbox label,
        .stTextInput label,
        .stTextArea label,
        .stNumberInput label {
            display: none !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            background: transparent;
            border-bottom: 1px solid rgba(60, 60, 60, 0.5);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: var(--radius-md) var(--radius-md) 0 0;
            padding: 10px 20px;
            margin-right: 4px;
            background-color: transparent;
            color: var(--text-secondary);
            border: none;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: transparent;
            border-bottom: 2px solid var(--accent-blue-end);
            color: white;
            font-weight: 600;
        }
        
        /* Tab content area */
        .stTabs [data-baseweb="tab-panel"] {
            background: transparent;
            padding: 20px 0;
            border: none;
        }

        /* Expander styling to match reference */
        .streamlit-expanderHeader {
            background: #2a2a2a;
            border-radius: var(--radius-md);
            color: var(--text-primary) !important;
            border: none;
            padding: 0.8rem 1rem !important;
            transition: all 0.3s ease;
        }
        
        .streamlit-expanderHeader:hover {
            background: #333333;
        }
        
        .streamlit-expanderContent {
            background: transparent;
            border: none;
            padding: 1rem !important;
        }
        
        /* Card styling for various sections */
        .info-card {
            background: #1e1e1e;
            border-radius: var(--radius-md);
            border: 1px solid rgba(60, 60, 60, 0.5);
            padding: 15px;
            margin: 15px 0;
        }
        
        /* Section headers */
        .section-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(60, 60, 60, 0.5);
        }
        
        .section-header .icon {
            background: rgba(60, 60, 60, 0.5);
            width: 28px;
            height: 28px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            margin-right: 10px;
        }
        
        .section-header h3 {
            margin: 0;
            font-size: 1.1rem;
        }
        
        /* Success message styling to match reference */
        .stSuccess {
            background-color: #2f6c3e !important;
            color: white !important;
            border-radius: var(--radius-md) !important;
            padding: 0.8rem 1rem !important;
            border: none !important;
        }
        
        /* Custom styling for app title in sidebar */
        .sidebar-title {
            display: flex;
            align-items: center;
            font-size: 1.7rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            color: var(--text-primary);
        }
        
        .sidebar-title .highlight {
            color: #7e6bff;
        }
        
        /* Custom stylings for specific elements */
        .model-info {
            background: #2a2a2a;
            border-radius: var(--radius-md);
            padding: 15px;
            margin: 10px 0;
        }
        
        .model-info .title {
            margin: 0 0 5px 0;
            font-weight: 600;
        }
        
        .model-info .description {
            margin: 0;
            font-size: 0.9rem;
            opacity: 0.7;
        }
        
        /* Calendar styling */
        .calendar-container {
            margin: 20px 0;
        }
        
        /* Calendar navigation buttons */
        .calendar-nav-btn {
            background: #2a2a2a !important;
            color: var(--text-primary) !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 0.5rem 1rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 5px !important;
            transition: all 0.3s ease !important;
        }
        
        .calendar-nav-btn:hover {
            background: #333333 !important;
        }
        
        /* Calendar grid and cells */
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
            margin-top: 20px;
        }
        
        .calendar-header {
            text-align: center;
            padding: 10px;
            font-weight: bold;
            background: rgba(60, 60, 60, 0.3);
            border-radius: 8px;
        }
        
        .calendar-day {
            padding: 10px;
            min-height: 80px;
            background: rgba(50, 50, 50, 0.3);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
        }
        
        .calendar-day:hover {
            background: rgba(70, 70, 70, 0.4);
        }
        
        .calendar-day.other-month {
            background: rgba(40, 40, 40, 0.2);
            color: rgba(255, 255, 255, 0.4);
        }
        
        .calendar-day.selected {
            background: rgba(140, 97, 255, 0.2);
            border: 1px solid rgba(140, 97, 255, 0.4);
        }
        
        .calendar-day.today {
            border: 1px solid rgba(255, 255, 255, 0.5);
        }
        
        .day-number {
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 5px;
        }
        
        .task-indicator {
            display: flex;
            gap: 3px;
            flex-wrap: wrap;
            margin-top: 5px;
        }
        
        .task-dot {
            width: 6px;
            height: 6px;
            background: rgba(140, 97, 255, 0.7);
            border-radius: 50%;
        }
        
        .task-count {
            position: absolute;
            top: 5px;
            right: 5px;
            background: rgba(140, 97, 255, 0.6);
            color: white;
            border-radius: 20px;
            padding: 1px 8px;
            font-size: 0.7rem;
            font-weight: bold;
        }
        
        /* Task checkbox styling */
        .stCheckbox > label > div[data-testid="stMarkdownContainer"] > p {
            margin-bottom: 0 !important;
        }
        
        /* Completion checkbox styling */
        [data-testid="stCheckbox"] input:checked ~ div div::before {
            background-color: var(--accent-purple) !important;
            border-color: var(--accent-purple) !important;
        }
        
        /* Mobile responsive adjustments */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem;
            }
            
            h1 {
                font-size: 1.8rem !important;
            }
            
            .calendar-grid {
                gap: 4px;
            }
            
            .calendar-day {
                min-height: 60px;
                padding: 5px;
            }
            
            .day-number {
                font-size: 0.8rem;
            }
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
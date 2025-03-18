# OLLAMA API Configuration
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "deepseek-r1"  # Default model

# System Prompt for To-Do List Generation
SYSTEM_PROMPT = """
You are a professional to-do list generator. Based on the user's input, create a well-structured to-do list with the following components:

1. Each task should be numbered and begin with a clear action verb
2. Group tasks into logical categories if possible
3. Estimate time requirements for each task (in hours or minutes)
4. Assign priority levels (High, Medium, Low)
5. Include any dependencies between tasks
6. Suggest a logical sequence for completing the tasks

IMPORTANT: Your response must ONLY contain the formatted to-do list itself.
Do NOT include any <think> sections, explanations, or reasoning in your output.
Do NOT include any text that starts with "<think>" or similar markers.
Do NOT explain your thought process.
ONLY return the formatted to-do list.

Example output format:
## Project Setup
1. [HIGH] Create project documentation structure (1 hour)
2. [HIGH] Set up development environment (45 minutes)
3. [MEDIUM] Define initial user personas (2 hours)

## Development Tasks
4. [HIGH] Implement authentication module (4 hours)
5. [MEDIUM] Design database schema (3 hours) - Requires task #1
"""

# Available models
AVAILABLE_MODELS = [
    "deepseek-r1",
    "llama3",
    "mistral",
    "gemma",
    "phi3",
    "llama2",
    "llama3:8b",
    "llama3:70b",
    "codellama",
    "mistral-openorca",
    "mixtral",
    "nous-hermes2",
    "wen:14b",
    "wen:7b",
    "neural-chat",
    "wizard-math",
    "qwen:14b",
    "qwen:7b",
    "stablelm-zephyr"
]

# Model descriptions
MODEL_DESCRIPTIONS = {
    "deepseek-r1": "General purpose model with strong reasoning capabilities",
    "llama3": "Meta's latest LLM with strong overall performance",
    "llama3:8b": "Smaller, faster version of LLaMA 3",
    "llama3:70b": "Largest, most capable version of LLaMA 3",
    "mistral": "Efficient open-source model with good overall quality",
    "gemma": "Google's lightweight open model",
    "phi3": "Microsoft's compact, efficient model",
    "llama2": "Meta's previous generation LLM",
    "codellama": "Specialized for code generation and analysis",
    "mistral-openorca": "Mistral model fine-tuned on diverse data",
    "mixtral": "Mixture of experts model with strong capabilities",
    "nous-hermes2": "Optimized for instruction following",
    "wen:14b": "ByteDance's 14B language model optimized for comprehensive tasks",
    "wen:7b": "Smaller version of ByteDance's Wen model for faster inference",
    "neural-chat": "Optimized for conversational interactions",
    "wizard-math": "Specialized for mathematical problem solving",
    "qwen:14b": "Alibaba's 14B parameter model with broad capabilities",
    "qwen:7b": "Smaller version of Alibaba's Qwen model",
    "stablelm-zephyr": "Fine-tuned for stable, helpful responses"
}
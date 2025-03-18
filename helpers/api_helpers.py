import streamlit as st
from config import MODEL

def get_model_payload(messages, temperature=0.7, top_p=0.9, max_tokens=2000):
    """
    Create a payload for the Ollama API request

    Parameters:
    messages (list): List of message objects
    temperature (float): Controls randomness (0.0 to 2.0)
    top_p (float): Controls diversity via nucleus sampling (0.0 to 1.0)
    max_tokens (int): Maximum length of generated response

    Returns:
    dict: Formatted payload for API request
    """
    return {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }
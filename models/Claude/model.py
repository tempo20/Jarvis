import os
from anthropic import Anthropic
import sys
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from reminders.calenderapi import *
from models.FalconsAI.model import *
from Search_Summarize.custom_search import *

def initialize():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return Anthropic(api_key=api_key)

def get_response(client, prompt, functions=None):
    try:
        message = client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="claude-3-5-sonnet-20240620",
            functions=functions
        )
        return message
    except Exception as e:
        print(f"Error in fetching response: {e}")
        return None

def chat_loop(client):
    functions = [get_events, create_event, get_summary, get_search_summary]
    print("You can start chatting with the Anthropic API (type 'exit' to end the chat).")

    while True:
        # Get user input
        prompt = input("You: ")
        
        # Exit condition
        if prompt.lower() == 'exit':
            print("Ending chat. Goodbye!")
            break
        
        # Get response from the API
        response = get_response(client, prompt, functions)
        
        # Print or handle the response
        if response:
            print(f"Anthropic: {response}")
        else:
            print("Failed to get a response")

def main():
    client = initialize()
    chat_loop(client)


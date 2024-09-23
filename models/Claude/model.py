import os
from anthropic import Anthropic # type: ignore
import sys
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from reminders.calenderapi import *
from models.FalconsAI.model import *
from Search_Summarize.custom_search import *

tools = [
    {
        "name": "event_getter",
        "description": "A function that grabs the next few events on the user's Google calendar",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required" : []
        }
    }
]
def process_tool_call(tool_name, tool_input = None):
    if tool_name == "event_getter":
        return get_events()

def initialize():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return Anthropic(api_key=api_key)

def get_text_content(message):
    text_content = []
    for block in message.content:
        if hasattr(block, 'text'):
            text_content.append(block.text)
    return ' '.join(text_content)

def get_response(client, prompt, functions=None):
    print(f"\n{prompt}\n")
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
            tools = tools
        )
        first_response = get_text_content(message)

        if message.stop_reason == "tool_use":
            tool_use = next(block for block in message.content if block.type == "tool_use")
            tool_name = tool_use.name
            tool_input = tool_use.input

            tool_result = process_tool_call(tool_name, tool_input)
            response = first_response + f"\n{tool_result}"

        return response

    
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

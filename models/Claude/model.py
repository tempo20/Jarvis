#%%
import os
from anthropic import Anthropic
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from reminders.calenderapi import *
#%%
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
functions = [get_events, create_event]
#%%
def get_response(prompt, functions = None):
    message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="claude-3-5-sonnet-20240620",
    functions = functions
)
    return message
# %%
def handle_response(response):
    if response.function_call:
        function_name = response.function_call.name
        function_args = response.function_call.arguments

        if function_name == "get_events":
            weather_result = get_events(**function_args)
    else:
        return response.content
# %%

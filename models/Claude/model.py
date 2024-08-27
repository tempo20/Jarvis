# %%
import os
from anthropic import Anthropic
import sys
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from reminders.calenderapi import *
from models.FalconsAI.model import *
# %%
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
functions = [get_events, create_event, get_summary]
# %%

def get_response(prompt, functions=None):
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
# %%

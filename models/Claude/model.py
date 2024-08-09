#%%
import os
from anthropic import Anthropic
#%%
client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

#%%
def get_response(prompt):
    message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="claude-3-5-sonnet-20240620",
)
    return message
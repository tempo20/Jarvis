#%%
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import configparser
#%%
config = configparser.ConfigParser()
config.read('config.ini')

model_name = config.get('model', 'model_name')
device = config.get('model', 'device')
#%%
quantization_config = BitsAndBytesConfig(load_in_8bit=True)


tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
# %%
def get_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    outputs = model.generate(inputs, do_sample = True, temperature = 0.7, max_new_tokens = 1024)
    response = tokenizer.decode(outputs[0])
    return response
# %%

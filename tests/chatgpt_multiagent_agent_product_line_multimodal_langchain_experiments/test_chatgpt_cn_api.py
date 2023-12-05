"""
Interface for using the chatgpt api online service, without setting up locally.

This interface is used for development, not in production.
"""

# Do not treat the machine like people.
# You need to handle them differently.

from litellm import completion
import os
import yaml

api_key_filepath = os.path.join(
    os.path.expanduser("~"), ".chatgpt_api_key.yaml")

if os.path.exists(api_key_filepath):
    if os.path.isfile(api_key_filepath):
        # Load YAML file
        with open(api_key_filepath, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            api_key = data['api_key']
            endpoint = data['endpoint']
    else:
        raise Exception(
            f"API key path exists but found non-file object at: '{api_key_filepath}'")
else:
    raise Exception(f"API key file not found in: '{api_key_filepath}'")


os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_API_BASE"] = endpoint
model_tag = "openai/gpt-3.5-turbo"


def get_reply_from_chatgpt(content: str):
    messages = [{"content": content, "role": "user"}]
    print("sending:")
    print(messages)
    # openai call
    # many info inside. you may want to take a look?
    response = completion(model_tag, messages)
    choices = response['choices']
    reply_content = choices[0]['message']['content']
    print("reply:")
    print(reply_content)
    return reply_content

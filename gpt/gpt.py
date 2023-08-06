import os
import sys

# Get the current file's directory
current_file_dir = os.path.dirname(os.path.realpath(__file__))

# Get the root directory of the project by finding the parent directory of 'github.com/yerassyldanay/aitutor'
root_dir = current_file_dir
while os.path.basename(root_dir) != 'aitutor':
    root_dir = os.path.dirname(root_dir)

# Add the root directory to the Python path
sys.path.append(root_dir)

# Now you can import any module from your project
from constants import env, variables

### END OF IMPORTS of folders ###

import json
import aiohttp
import logging
import asyncio
from pprint import pprint
from typing import List, Tuple

from langchain.chat_models import ChatOpenAI

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class OpenAIChatGPT:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url_completion = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": 'Bearer ' + env.GPT_API_KEY,
            "Content-Type": "application/json",
        }

    async def send_request(self, messages: List[dict]) -> Tuple[str, int]:
        data = {
            "model": "gpt-4",
            "messages": messages,
        }
        # pprint(f"\nmessages: {messages}\n")

        response = None
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url_completion, headers=self.headers, data=json.dumps(data)) as resp:
                if resp is None:
                    logger.error("response is empty")
                    return None
                
                if resp.status // 100 != 2:
                    logger.error(f"status code: {resp.status} and response: {response}")
                    return None
                
                response = await resp.json()

        # logger.debug(f"response: {response}")

        if type(response) != dict:
            logger.error(f"response is not dict: {response}")
            return None

        if 'error' in response:
            logger.error(f"error: {response}")
            return None

        contents = []
        if 'choices' in response:
            for choice in response['choices']:
                if 'message' in choice and 'content' in choice['message']:
                    contents.append(choice['message']['content'])
                else:
                    logger.error('No content in choice message')
        else:
            logger.error('No choices in response data')

        total_tokens = response.get('usage', {}).get('total_tokens', -1)

        # logger.info('Contents: %s', contents)
        logger.info('Total Tokens: %s', total_tokens)
        
        return (' '.join(contents), total_tokens)

async def run():
    messages = [
        {
            "role": "system",
            "content": variables.DESCRIPTION % "Yerassyl",
        },
        {
            "role": "user",
            "content": "I want talking about football. I supporting Real Madrid"
        }
    ]
    openai_api_model = OpenAIChatGPT(env.GPT_API_KEY)
    tasks = [asyncio.create_task(openai_api_model.send_request(messages=messages))]
    result = await asyncio.gather(*tasks)
    for each in result:
        print(each)


if __name__ == '__main__':
    asyncio.run(run())

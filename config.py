import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

key_1 = os.environ.get("KEY_1")
key_2 = os.environ.get("KEY_2")
key_3 = os.environ.get("KEY_3")
key_4 = os.environ.get("KEY_4")
key_5 = os.environ.get("KEY_5")

openai_api_keys = [key_1, key_2, key_3, key_4, key_5]

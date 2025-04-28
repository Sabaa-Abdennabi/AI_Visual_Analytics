# run in the cmdd this command to set the token : set GROQ_API_KEY=eltoken_mt3ek_hni
from groq import Groq
import base64
import os

from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),  
)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
image_path = "./zara.png"

# Getting the base64 string
base64_image = encode_image(image_path)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "based  on the website provided and the ehatmap provided to show the interest center of this website interface , suggest some ui/ux recommandation for the website"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
    model="meta-llama/llama-4-scout-17b-16e-instruct",
)

print(chat_completion.choices[0].message.content)

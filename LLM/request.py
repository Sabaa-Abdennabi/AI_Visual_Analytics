# run in the cmdd this command to set the token : set GROQ_API_KEY=eltoken_mt3ek_hni ou cree un fichier .env et mettez le token dedans 
from groq import Groq
from dotenv import load_dotenv
import base64
import os
load_dotenv()
def generate_recommandations(image_path,message):
    """
    Generate UI/UX recommendations based on the provided image and message.
    
    Args:
        image_path (str): Path to the image file.
        message (str): Additional message to provide context for the recommendations.
    
    Returns:
        str: The generated recommendations.
    """
    # Initialize Groq client
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"), 
    )
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string
    base64_image = encode_image(image_path)
    text = f"Please provide UI/UX recommendations based on the image. {message}"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
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
    return chat_completion.choices[0].message.content
# if __name__ == "__main__":
#     image_path = "./zara.png"
#     message = "Please provide UI/UX recommendations based on the image."
#     recommendations = generate_recommandations(image_path, message)
#     print(recommendations)

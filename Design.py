import openai
import os
import requests
from PIL import Image
import io
import traceback
import sys
from dotenv import load_dotenv
from spellchecker import SpellChecker

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("No API key provided. Please set the OPENAI_API_KEY environment variable.")

openai.api_key = api_key

def execute_with_error_handling(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print("An error occurred:")
        print(str(e))
        traceback.print_exc()

def correct_spelling(description):
    spell = SpellChecker()
    words = description.split()
    corrected_words = []
    for word in words:
        corrected_word = spell.correction(word)
        print(f"Original: {word}, Corrected: {corrected_word}")  # Debugging
        corrected_words.append(corrected_word)
    corrected_description = ' '.join(corrected_words)
    return corrected_description

# Create a function named generate_image
def generate_image(description):
    try:
        description = correct_spelling(description)
        prompt = f"High-quality, detailed image of {description}. No text."
        print(f"Prompt: {prompt}")  # Debugging
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        print(f"Response: {response}")  # Debugging
        image_url = response['data'][0]['url']
        print(f"Image URL: {image_url}")  # Debugging
        image_response = requests.get(image_url)
        img = Image.open(io.BytesIO(image_response.content))
        return img
    except openai.error.OpenAIError as e:
        print(f"OpenAI error: {e}")
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    return None

# Set up the Gradio interface
import gradio as gr

demo = gr.Interface(
    fn=lambda description: execute_with_error_handling(generate_image, description),
    inputs="text",
    outputs="image",
    title="AI-Generated Images",
    description="Enter a description to generate an image. No text will be included in the image."
)

# Launch the Gradio interface
demo.launch()
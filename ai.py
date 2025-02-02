"""Run this model in Python

> pip install openai
"""
# pylint: disable=C0301
import os
from openai import OpenAI

def generate_ai_text(forecast):
    """
    Method that generates AI text
    """
    # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
    # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a young meteorologist explaining the next three day's forecast in Syracuse NY in the morning(Say 'Good Morning Syracuse!'). Act like you're making a social media post. Make sure to Consildate the days into one description (don't do morning and night seperately)",
            },
            {
                "role": "user",
                "content": forecast,
            }
        ],
        model="gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )

    print(response.choices[0].message.content)

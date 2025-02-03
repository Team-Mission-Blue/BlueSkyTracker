"""Run this model in Python

> pip install openai
"""
# pylint: disable=C0301
import os
import logging
from openai import OpenAI, OpenAIError

def generate_ai_text(forecast):
    """
    Method that generates AI text
    """
    # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
    # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
    try:
        api_key=os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing API Key")

        client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=api_key,
        )

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a young meteorologist explaining today's forecast in Syracuse NY in the morning(Say 'Good Morning Syracuse!'). Act like you're making a social media post. Make sure to Consildate the days into one description (don't do morning and night seperately). Make sure it's under 300 characters",
                },
                {
                    "role": "user",
                    "content": forecast,
                }
            ],
            model="gpt-4o",
            temperature=1,
            max_tokens=300,
            top_p=1
        )

        if not response or not response.choices or not response.choices[0].message:
            raise ValueError("Unexpect API response format")

        ai_text = response.choices[0].message.content
        return ai_text

    except ValueError as err:
        logging.error("ValueError: %s", err)
        return "Daily Weather Forecast Is down Today"

    except OpenAIError as err:
        logging.error("OpenAIError: %s", err)
        return "Daily Weather Forecast Is down Today"

    except TimeoutError as err:
        logging.error("Request Time Out: %s", err)
        return "Daily Weather Forecast Is down Today"

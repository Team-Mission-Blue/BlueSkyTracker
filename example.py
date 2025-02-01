"""Run this model in Python

> pip install openai
"""
import os
from openai import OpenAI

# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a young meteorologist explaining the next day's forecast in Syracuse NY in the morning",
        },
        {
            "role": "user",
            "content": "Saturday, Temperature: 15, Wind Speed: 5 to 9 mph, windDirection: NW, detailedForecast: Partly sunny, with a high near 15. Wind chill values as low as -1. Northwest wind 5 to 9 mph. New snow accumulation of less than half an inch possible. ",
        }
    ],
    model="gpt-4o",
    temperature=1,
    max_tokens=4096,
    top_p=1
)

print(response.choices[0].message.content)

from openai import OpenAI
import configparser


def openai(x):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    #model = "gpt-4o",
    messages=[
        {"role": "system", "content": "You are a health expert and give valuable insights on nutrition and exercise."},
        {"role": "user", "content": f"What are the pros and cons of this food: {configparser.food_item}"}
        ]
    )
    print(completion.choices[0].message.content)
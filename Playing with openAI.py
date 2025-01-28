## Playing with openAI
import openai

with open("/Users/brian.canyon/Documents/openAI.key.txt")as file:
    openai.api_key = file.read()

response = openai.Completion.create(
    engine ='gpt-3.5-turbo',
    prompt = 'What is the circumfrance of earth',
    max_tokens = 10
)

answer = response.choices[0].text.strip()

print(answer)
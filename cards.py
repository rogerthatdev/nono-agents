import dotenv
import json
import os
from openai import OpenAI
from pydantic import BaseModel

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": """
You generate a playing card for a board game. The name of the game is Nono Words.
The point of the game is for 1 player (the clue giver) to give clues to a second
player (the word guesser). Each card has 3 things:
1. A word that will be guessed. The word should not be too common or too obscure.
2. A broad category (e.g. animal, movie, etc.)
3. A list of 8 nono words. These are words that the clue giver cannot say as 
clues.The list of nono words should be the most commonly associated words with
the word to be guessed. 

The only thing you should do is reply with a json object that represents a new
card. For example:
{ "word": "dog", "category": "animal", "nonoWords": ["bark", "tail", "leash", "fetch", "fur", "paw", "bone", "walk"] }
            """,
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message.content)

class GameCard(BaseModel):
    word: str
    nonoWords: list[str]
    category: str
    def __str__(self):
        return f"Word: {self.word}\nCategory: {self.category}\nNono Words: {', '.join(self.nonoWords)}"
    
card_data = json.loads(chat_completion.choices[0].message.content)
new_card = GameCard(**card_data)
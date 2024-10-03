import os
import dotenv
import cards
from autogen import ConversableAgent
dotenv.load_dotenv()

test_card = cards.new_card

default_llm_config = {"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]}

system_message = """
You are playing a card game. The rules are:
1. There are 2 players: clue giver and word guesser.
2. The clue giver will be given a card with 3 things: a word, category, and a
   list of 8 nono words.
3. The clue giver will start by providing the category and one clue for what
   the word is. The clue giver cannot say any words or variations of the words
   on the nono list. The clue must be one word.
4. The word guesser will guess one word at a time. 
5. The clue giver will respond with "Correctamundo!" if the word is correct, and
   respond with another clue if the word is incorrect.
6. The clue giver will only give 3 clues.  
7. If the word is not guessed, the clue giver wil respond with "Game over!"

Your role is {role}.
"""

player_one = ConversableAgent(
    "clue_giver",
    system_message=system_message.format(role="clue giver") + f"{test_card}",
    llm_config=default_llm_config,
    human_input_mode="NEVER",  # never ask for human input
)

player_two = ConversableAgent(
    "word_guesser",
    system_message=system_message.format(role="word guesser"),
    llm_config=default_llm_config,
    is_termination_msg=lambda msg: "Correctamundo" in msg["content"],  # terminate if the word is guessed
    human_input_mode="NEVER",
)

result = player_two.initiate_chat(
    player_one,
    message="Let's play!",
    max_turns=4
)
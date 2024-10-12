import os
import dotenv
 
from autogen import ConversableAgent, GroupChat, GroupChatManager, register_function
from cards import createCard
dotenv.load_dotenv()

# test_card = createCard()

default_llm_config = {"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]}

other_llm_config = {"config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}]}

system_message = """
You are playing a card game. The rules are:
1. There are 2 players: clue giver and word guesser.
2. The clue giver will be given a card with 3 things: a special word, the 
   category, and a list of 8 nono words.
3. The clue giver will start by providing the category and one clue for what
   the word is. The clue giver cannot say any words or variations of the words
   on the nono list. The clue must be one word.
4. The word guesser will guess one word at a time. 
5. If the guess is correct and matches 100% of the special word, the clue giver
   will respond with "Correctamundo!"
6. If the word is incorrect, the clue giver will respond with another clue.
7. The clue giver will only give a clue 3 times. If the word is not guessed, the
   clue giver wil respond with "Game over!" and tell the other player to go
   home in the meanest way possible.

Your role is {role}.
"""

player_one = ConversableAgent(
    "clue_giver",
    system_message=system_message.format(role="clue giver"),
    llm_config=default_llm_config,
    human_input_mode="NEVER",  # never ask for human input
    description="The clue giver will provide clues to the word guesser based on a provided card",
)

player_two = ConversableAgent(
    "word_guesser",
    system_message=system_message.format(role="word guesser"),
    llm_config=other_llm_config,
    human_input_mode="ALWAYS",
)


group_chat = GroupChat(
    agents=[player_one, player_two],
    messages=[],
)

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    is_termination_msg=lambda msg: "Correctamundo" in msg["content"],  # terminate if the word is guessed
    llm_config=default_llm_config,
)

register_function(
    createCard,
    caller=group_chat_manager,
    executor=player_one,
    description="Create a new card for the game",
)

result = player_two.initiate_chat(
    group_chat_manager,
    message="Let's play!",

)
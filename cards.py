from pydantic import BaseModel

class GameCard(BaseModel):
    word: str
    nonoWords: list[str]
    category: str
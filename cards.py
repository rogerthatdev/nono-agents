from pydantic import BaseModel

class GameCard(BaseModel):
    word: str
    nonoWords: list[str]
    category: str
    def __str__(self):
        return f"Word: {self.word}\nCategory: {self.category}\nNono Words: {', '.join(self.nonoWords)}"
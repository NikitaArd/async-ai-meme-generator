import re

from config.settings import MEMES_PATH_PATTERN

class Meme:
    def __init__(self, id: str|int, meme_source: str, meme_description: str, meme_examples: str):
        self.id = int(id)    
        self.meme_source = meme_source
        self.meme_description = meme_description
        self.meme_examples = meme_examples

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        try:
            self._id = int(value)
        except ValueError:
            raise ValueError("id must be integer or integer-like string")

    @property
    def meme_source(self):
        return self._meme_source

    @meme_source.setter
    def meme_source(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"value should be a str not {type(value)}")
        
        if re.match(MEMES_PATH_PATTERN, value) is None:
            raise ValueError(f"meme_source is invalid, expected ./assets/meme_source/[filename] got {value}")
        
        self._meme_source = value

    @property
    def meme_description(self):
        return self._meme_description

    @meme_description.setter
    def meme_description(self, value:str):
        self._meme_description = value

    @property
    def meme_examples(self):
        return self._meme_examples

    @meme_examples.setter
    def meme_examples(self, value:str):
        if not isinstance(value, str):
            raise ValueError(f"value should be a str not {type(value)}")

        self._meme_examples = value.split("\n") 
        
    def __repr__(self):
        result = f"""
Selected meme template:
Source: {self.meme_source}
Description: {self.meme_description}
Examples:
{self.meme_examples}
        """

        return result
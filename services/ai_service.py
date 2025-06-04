from openai import OpenAI
import os
from dotenv import load_dotenv
import json

class MemeGenerator:
    def __init__(self, use_pseudo_response=False):
        load_dotenv()
        if not use_pseudo_response:
            self.client = OpenAI(api_key=os.environ.get("OPEN_AI_API_KEY"))
        self.use_pseudo_response = use_pseudo_response
        self.pseudo_response = {
            "memes": [
                "me waiting for my friends to understand that codefast gets you coding in two weeks but they still on that 6-month grind",
                "me watching my competitor's online course with outdated content like... nah fam, we move on from that",
                "me trying to figure out why my buddy's layers of abstraction ain't paying off, when i could've been making bank with codefast",
                "me scrolling through competitor reviews, realizing they're still teaching in 2020 while codefast is already in 2023", 
                "me over here like, 'you know you could've learned how to code in two weeks instead of that 6-month struggle, right?'"
            ]
        }
        
    def generate_memes(self, product_description, meme_description, meme_examples):
        if self.use_pseudo_response:
            print("Using pseudo response instead of real API for meme generation...")
            print("Successfully generated memes using pseudo response!")
            return self.pseudo_response
            
        print("Using OpenAI API for meme generation...")
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are a meme marketing expert. Your task is to create 5 humorous, engaging memes to promote a product. Each meme must be distinct and humorous, while also subtly mocking competitors' shortcomings without making fun of the product itself. Keep the tone extremely casual using Gen-Z/internet slang. Use a variety of meme templates and avoid repetition in jokes/format. The memes should be written in lowercase, and there should be no emojis. Your response should be formatted as a JSON object containing the list of memes."
                        }
                    ]
                },
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": f"""You are a meme marketing expert tasked with creating 5 humorous, engaging memes to promote a product. Follow these guidelines:

1. Tone: Extremely casual, using Gen-Z/internet slang 
2. Variety: Each meme must use a distinct template 
3. Focus: Subtly mock competitors' shortcomings, not the product itself.
4. Style: All lowercase, no emojis, avoid repetition in jokes/format.
5. Make these memes less professional and for wider audience

Product description:
{product_description}

Meme description:
{meme_description}

Examples of the output:
{meme_examples}"""
                        }
                    ]
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "memes_collection",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "memes": {
                                "type": "array",
                                "description": "A list of memes.",
                                "items": {
                                    "type": "string",
                                    "description": "A single meme"
                                }
                            }
                        },
                        "required": [
                            "memes"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        print("Successfully generated memes using OpenAI!")
        return json.loads(response.choices[0].message.content)
# Project created: December 2024
# Open-sourced : May 2025


from db.database import DBController
from db.helpers import Meme

from services.ai_service import MemeGenerator
from services.video_service import VideoGenerator
from services.helpers import select_meme_file

from config.settings import MEMES_SOURCE, USE_PSEUDO

import inquirer
import asyncio
    
async def main():
    modes = {
        1: 'Add new source meme to memory.',
        2: 'Create a new meme.'
    }
    
    question = inquirer.List('mode', message="Chose the script mode please:", choices=[modes[1], modes[2]])
    selected_mode = inquirer.prompt([question])["mode"]
    
    db = DBController()
    
    if selected_mode == modes[1]:
        print(f"Available meme files in {MEMES_SOURCE}:")
        
        meme_name = select_meme_file(MEMES_SOURCE)
        meme_source = f"{MEMES_SOURCE}/{meme_name}"
        
        meme_description = input("\nEnter meme description: ")
        
        print("\nEnter meme examples (separated by semicolons):")
        meme_examples = input()
        meme_examples = meme_examples.replace(";", "\n")
        
        db.insert_meme(meme_source, meme_description, meme_examples)
        
        print("Meme added to a local database")
    elif selected_mode == modes[2]:
        product_description = input("Enter your product description: ")
        
        memes = db.select_memes()
        
        choices = list(map(lambda key: (memes[key][1], key), memes))
        questions = [inquirer.List('meme', choices=choices, carousel=True)]
        
        selected_meme_id = inquirer.prompt(questions)["meme"]
        selected_meme = Meme(selected_meme_id, *memes[selected_meme_id])

        generated_memes = MemeGenerator(use_pseudo_response=USE_PSEUDO).generate_memes(product_description, selected_meme.meme_description, selected_meme.meme_examples)["memes"]
        video_generator = VideoGenerator(chroma_video_path=selected_meme.meme_source)
        
        tasks = [video_generator.generate_video(meme, i) for i, meme in enumerate(generated_memes, 1)]
        
        output_paths = await asyncio.gather(*tasks)
        
        for i, path in enumerate(output_paths, 1):
            print(f"Video {i} generated at: {path}")
    else:
        exit("Exiting program.")
        
    db.close()

if __name__ == "__main__":
    asyncio.run(main())



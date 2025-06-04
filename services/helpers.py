import inquirer
import os

def select_meme_file(memes_dir):
    files = [f for f in os.listdir(memes_dir) if f.endswith(".mp4")]
    questions = [
        inquirer.List('meme_file',
                        message="Select a meme file",
                        choices=files,
                        carousel=True)
    ]
    answer = inquirer.prompt(questions)
    return answer['meme_file']
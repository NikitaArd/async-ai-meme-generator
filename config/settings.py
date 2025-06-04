import re

MEMES_SOURCE = "./assets/memes_source"
MEMES_PATH_PATTERN = rf'^{re.escape(MEMES_SOURCE)}/[^/]+$'

USE_PSEUDO = False

DATABASE_FILE_NAME = "memes.db"

BACKGROUND_DIR = "./assets/backgrounds"
FONT_PATH = "./assets/fonts/font-3.otf"
FONT_SIZE = 55
OUTPUT_DIR = "./output"

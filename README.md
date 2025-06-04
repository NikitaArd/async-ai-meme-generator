### ⚠️ Originally developed in December 2024 – open-sourced in may 2025 with client approval.

</br>
</br>
</br>

# Task

The client needed an automated system for generating short-form, humorous meme videos to promote various products on social media. The tool had to use AI (ChatGPT) to generate captions, combine them with greenscreen video templates, and render finalized meme videos.

# Meme Generator

A Python-based tool for generating custom memes with text overlays on green screen videos.

## Overview

This project allows you to create custom meme videos by:
1. Adding green screen meme templates to a database
2. Generating custom text for these templates using AI
3. Automatically creating videos with the text overlaid on the meme templates

## Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system (required for video processing)
- OpenAI API key (for generating meme text)

## Installation

### Installing FFmpeg

FFmpeg is required for video processing. Here's how to install it on different operating systems:

#### Windows
1. Download the FFmpeg build from [FFmpeg's official website](https://ffmpeg.org/download.html#build-windows) or use [gyan.dev builds](https://www.gyan.dev/ffmpeg/builds/)
2. Extract the ZIP file to a location on your computer (e.g., `C:\ffmpeg`)
3. Add FFmpeg to your system PATH:
   - Right-click on "This PC" or "My Computer" and select "Properties"
   - Click on "Advanced system settings"
   - Click on "Environment Variables"
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and add the path to the FFmpeg `bin` folder (e.g., `C:\ffmpeg\bin`)
   - Click "OK" on all dialogs to save changes
4. Verify installation by opening Command Prompt and typing: `ffmpeg -version`

#### macOS
Using Homebrew:
```
brew install ffmpeg
```

Using MacPorts:
```
sudo port install ffmpeg
```

#### Linux (Ubuntu/Debian)
```
sudo apt update
sudo apt install ffmpeg
```

#### Linux (Fedora)
```
sudo dnf install ffmpeg
```

Verify installation on macOS/Linux:
```
ffmpeg -version
```

### Project Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPEN_AI_API_KEY=your_openai_api_key_here
   ```

## Project Structure

- `assets/` – Contains static resources used in the meme generation process
  - `backgrounds/` – Background images for the memes
  - `fonts/` – Fonts used for meme text
  - `memes_source/` – Raw meme video files with greenscreen overlays
- `config/` – Project configuration files
- `db/` – Database-related code
- `services/` – Modules for interacting with the OpenAI API and handling video editing
- `output/` – Directory where generated meme videos are saved
- `memes.db` – SQLite database that stores metadata about meme templates
- `main.py` – Entry point for running the meme generation process

## Usage

### Step 1: Add Meme Templates to the Database

1. Download green screen meme videos from [Green Screen Memes](https://greenscreenmemes.com)
2. Place the downloaded video files in the `./assets/memes_source/` directory
3. Run the script choosing the proper option when you get asked:
   ```
   python main.py
   ```
4. Follow the prompts to:
   - Select a meme video file
   - Enter a description for the meme
   - Provide example text for the meme (separated by semicolons)

### Step 2: Generate Memes

1. Run the main script:
   ```
   python main.py
   ```

2. Follow the prompts to:
   - Enter your product description
   - Select a meme template from the database
   - Wait for the AI to generate meme text
   - Wait for the videos to be generated

3. The generated videos will be saved in the `output/` directory as:
   - `output_video_1.mp4`
   - `output_video_2.mp4`
   - etc.

## Example

1. Add a "waiting monkey" meme to the database:
   - Place `waiting_monkey.mp4` in the `./assets/memes_source/` directory
   - Run `python main.py`
   - Select `waiting_monkey.mp4`
   - Description: "Monkey waiting impatiently"
   - Examples: "me waiting for my code to compile;me waiting for my friend who said they'd be ready in 5 minutes"

2. Generate memes:
   - Run `python main.py`
   - Product description: "Fast coding bootcamp that teaches programming in 2 weeks"
   - Select "Monkey waiting impatiently" from the list
   - The script will generate 5 meme videos with different text

## Troubleshooting

- If you encounter video processing errors, ensure FFmpeg is properly installed
- If text generation fails, check your OpenAI API key in the `.env` file
- If a video file doesn't work, ensure it has a proper green screen background

## Acknowledgements

- [Green Screen Memes](https://greenscreenmemes.com) for providing green screen meme templates
- OpenAI for the text generation API
- MoviePy for video processing capabilities 
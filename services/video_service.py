import os
import asyncio
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.video.fx import MaskColor
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from concurrent.futures import ThreadPoolExecutor

from config.settings import BACKGROUND_DIR, FONT_PATH, OUTPUT_DIR, FONT_SIZE

class VideoGenerator:
    def __init__(self, background_path=None, chroma_video_path=None):
        self.backgrounds_dir = BACKGROUND_DIR
        self.chroma_video_path = chroma_video_path or "meme-green.mp4"
        self.font_path = FONT_PATH
        self.font_size = FONT_SIZE
        self.output_dir = OUTPUT_DIR
        self.output_base = "output_video"
        self.output_ext = ".mp4"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.text_color = "white"
        self.text_position = ("center", "top")
        self.output_size = (1080, 1920)  # 9:16 aspect ratio
        self.executor = ThreadPoolExecutor()
        
        self.available_backgrounds = []
        self.used_backgrounds = []
        
    async def create_text_clip(self, text_content, duration):
        return await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: TextClip(
                text=text_content,
                font_size=self.font_size,
                font=self.font_path,
                color=self.text_color,
                stroke_color="black",
                stroke_width=4,
                size=(1000, None),
                method="caption",
                text_align="center",
                vertical_align="top",
                margin=(0, 180)
            ).with_duration(duration).with_position(self.text_position)
        )
    
    async def process_chroma_video(self):
        def _process():
            chroma_clip = VideoFileClip(self.chroma_video_path)
            mask = MaskColor(
                color=(7, 233, 1),
                threshold=160,
                stiffness=80
            )
            chroma_clip = mask.apply(chroma_clip)
            chroma_clip = chroma_clip.resized(height=1600)
            return chroma_clip.with_position("center")
            
        return await asyncio.get_event_loop().run_in_executor(
            self.executor,
            _process
        )
    
    async def get_available_filename(self, index):
        def _get_filename():
            output_path = os.path.join(self.output_dir, f"{self.output_base}_{index}{self.output_ext}")
            return output_path
            
        return await asyncio.get_event_loop().run_in_executor(
            self.executor,
            _get_filename
        )

    async def get_background(self):
        def _get_background():
            if not self.available_backgrounds and not self.used_backgrounds:
                backgrounds = [f for f in os.listdir(self.backgrounds_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
                if not backgrounds:
                    raise Exception("No background images found in ./backgrounds directory")
                self.available_backgrounds = backgrounds

            if not self.available_backgrounds:
                self.available_backgrounds = self.used_backgrounds
                self.used_backgrounds = []

            background = self.available_backgrounds.pop(0)
            self.used_backgrounds.append(background)
            return os.path.join(self.backgrounds_dir, background)
            
        return await asyncio.get_event_loop().run_in_executor(
            self.executor,
            _get_background
        )
    
    async def generate_video(self, text_content, index):
        chroma_clip = await self.process_chroma_video()
        video_duration = chroma_clip.duration
        
        background_path = await self.get_background()
        bg_clip = await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: ImageClip(background_path).resized(new_size=self.output_size).with_duration(video_duration)
        )
        
        text_clip = await self.create_text_clip(text_content, video_duration)
        
        def _create_final_video():
            final_video = CompositeVideoClip(
                [bg_clip, chroma_clip, text_clip],
                size=self.output_size
            ).with_duration(video_duration)
            
            if chroma_clip.audio:
                final_video = final_video.with_audio(chroma_clip.audio)
            return final_video
            
        final_video = await asyncio.get_event_loop().run_in_executor(
            self.executor,
            _create_final_video
        )
        
        output_path = await self.get_available_filename(index)
        
        await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: final_video.write_videofile(
                output_path,
                fps=24,
                codec="libx264",
                audio_codec="aac",
                audio_bitrate="50k",
                threads=16
            )
        )
        
        return output_path
        
    def __del__(self):
        self.executor.shutdown(wait=True)

if __name__ == "__main__":
    async def generate_multiple_videos():
        generator = VideoGenerator()
        texts = [
            "First video text",
            "Second video text", 
            "Third video text",
            # "Fourth video text",
            # "Fifth video text"
        ]

        tasks = [generator.generate_video(text, i+1) for i, text in enumerate(texts)]
        
        output_paths = await asyncio.gather(*tasks)
        
        for i, path in enumerate(output_paths, 1):
            print(f"Video {i} generated at: {path}")

    asyncio.run(generate_multiple_videos())

   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   from pytube import YouTube
   import os
   from moviepy.editor import AudioFileClip

   app = FastAPI()

   class VideoRequest(BaseModel):
       url: str

   @app.post("/download")
   async def download_video(request: VideoRequest):
       video_url = request.url

       if not video_url:
           raise HTTPException(status_code=400, detail="URL is required")

       try:
           yt = YouTube(video_url)
           audio_stream = yt.streams.filter(only_audio=True).first()
           
           # Pobranie audio jako plik
           audio_file = audio_stream.download(filename="temp_audio")
           mp3_file = audio_file.replace(".webm", ".mp3")
           audio_clip = AudioFileClip(audio_file)
           audio_clip.write_audiofile(mp3_file)
           audio_clip.close()

           # Usunięcie tymczasowego pliku
           os.remove(audio_file)

           return {"download_url": mp3_file}
       except Exception as e:
           raise HTTPException(status_code=400, detail=str(e))

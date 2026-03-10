from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import yt_dlp
import os

# 1. Define the app (Crucial!)
app = FastAPI()

# 2. Setup templates folder
templates = Jinja2Templates(directory="templates")


# 3. The Home Page route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 4. The Download logic route
@app.get("/download-web")
async def web_download(url: str, name_file: str, background_tasks: BackgroundTasks):
    filename = f"{name_file}.mp4"
    options = {'format': 'best', 'outtmpl': filename}

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    background_tasks.add_task(os.remove, filename)
    return FileResponse(path=filename, filename=filename)
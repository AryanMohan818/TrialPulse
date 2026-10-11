import os
from pathlib import Path
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TrailPulse - Touch Grass Outdoor Companion")

# Resolve absolute path of the app directory
BASE_DIR = Path(__file__).resolve().parent

# Mount static files and setup templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Configuration
HF_API_KEY = os.getenv("HF_TOKEN", "")
GEMMA_MODEL = "google/gemma-2-2b-it"

class MissionRequest(BaseModel):
    duration_minutes: int = 15
    environment: str = "park"

# Curated field tasks for instant offline reliability
OFFLINE_MISSIONS = {
    "park": [
        "Find 3 distinct tree leaf shapes and observe their textures without touching your phone.",
        "Spot two different bird species: note their calls and flight patterns.",
        "Find a quiet bench or patch of grass, close your eyes for 3 minutes, and count 5 unique ambient sounds."
    ],
    "trail": [
        "Hike 10 minutes out without looking at a screen. Notice changes in elevation and soil texture.",
        "Search for signs of local wildlife tracks, burrows, or insect activity along the path.",
        "Take a slow 360-degree look at the tree canopy and identify where the sunlight hits strongest."
    ],
    "backyard": [
        "Walk barefoot on the grass or soil for 5 minutes and focus on the temperature and texture.",
        "Observe a single patch of garden soil or plant for 2 minutes to count how many insects interact with it.",
        "Take 10 deep belly breaths facing the sun or open breeze."
    ],
    "urban": [
        "Spot 3 places where nature is reclaiming urban concrete (moss in sidewalks, vines on brick).",
        "Walk down a street you have never walked down before at a slow, deliberate pace.",
        "Find the tallest tree on your block and pause underneath its canopy for 60 seconds."
    ]
}

def generate_with_gemma(prompt: str) -> str:
    """Query Hugging Face Inference API for open-weight Gemma 2."""
    if not HF_API_KEY:
        return ""
    
    api_url = f"https://api-inference.huggingface.co/models/{GEMMA_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n",
        "parameters": {"max_new_tokens": 250, "temperature": 0.7}
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                text = result[0]["generated_text"]
                return text.split("<start_of_turn>model\n")[-1].strip()
    except Exception as e:
        print(f"Gemma API inference error: {e}")
    return ""

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/mission")
async def create_mission(req: MissionRequest):
    env = req.environment.lower()
    if env not in OFFLINE_MISSIONS:
        env = "park"
        
    prompt = (
        f"You are TrailPulse, an outdoor micro-mission generator for the 'Touch Grass' challenge. "
        f"Generate a {req.duration_minutes}-minute outdoor exploration mission for someone in a {req.environment} setting. "
        f"The goal is minimal screen time and sensory grounding. "
        f"Provide: 1 mission title, and exactly 3 clear sensory field tasks (e.g. sound, touch, sight). "
        f"Keep the whole text under 80 words. Be inspiring and brief."
    )
    
    ai_text = generate_with_gemma(prompt)
    is_open_ai_generated = bool(ai_text)
    
    if not ai_text:
        tasks = OFFLINE_MISSIONS.get(env, OFFLINE_MISSIONS["park"])
        ai_text = (
            f"**Mission: {req.environment.capitalize()} Micro-Explorer ({req.duration_minutes} Mins)**\n\n"
            f"1. {tasks[0]}\n"
            f"2. {tasks[1]}\n"
            f"3. {tasks[2]}"
        )
    
    return JSONResponse({
        "success": True,
        "environment": req.environment,
        "duration": req.duration_minutes,
        "model": "Gemma 2 (open-weights)" if is_open_ai_generated else "Local Open Heuristic Engine (Offline)",
        "mission_markdown": ai_text
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
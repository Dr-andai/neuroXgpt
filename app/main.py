from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Load dataset
df = pd.read_parquet(
    "hf://datasets/BrainGPT/BrainBench_GPT-4_v0.1.csv/data/train-00000-of-00001-1c06a67d80bbbd1d.parquet"
)

session_store = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/start", response_class=HTMLResponse)
async def start(request: Request):
    trial = df.sample(1).iloc[0]
    show_original = random.choice([True, False])
    abstract = trial["original_abstract"] if show_original else trial["incorrect_abstract"]
    correct = "no" if show_original else "yes"

    session_store["trial"] = {
        "doi": trial["doi"],
        "journal_section": trial["journal_section"],
        "abstract": abstract,
        "correct": correct
    }
    session_store["results"] = []

    return RedirectResponse("/trial", status_code=302)

@app.get("/trial", response_class=HTMLResponse)
async def trial(request: Request):
    trial = session_store.get("trial", None)
    if not trial:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse("trial.html", {
        "request": request,
        "abstract": trial["abstract"],
        "journal_section": trial["journal_section"]
    })

@app.post("/submit-trial", response_class=HTMLResponse)
async def submit_trial(request: Request, altered: str = Form(...), confidence: int = Form(...)):
    trial = session_store.get("trial", None)
    correct = trial["correct"]

    session_store["results"].append({
        "user_guess": altered,
        "confidence": confidence,
        "correct_answer": correct,
        "is_correct": altered == correct
    })

    return RedirectResponse("/results", status_code=302)

@app.get("/results", response_class=HTMLResponse)
async def results(request: Request):
    return templates.TemplateResponse("results.html", {
        "request": request,
        "results": session_store["results"],
        "category": session_store["trial"]["journal_section"]
    })

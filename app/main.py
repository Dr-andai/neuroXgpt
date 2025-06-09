from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Load and cache dataset at startup
CSV_URL = "https://huggingface.co/datasets/BrainGPT/BrainBench_GPT-4_v0.1.csv"
df = pd.read_csv(CSV_URL)

# In-memory session store (for demo)
session_store = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/start", response_class=HTMLResponse)
async def start(request: Request, category: str = Form(...)):
    filtered = df[df["journal_section"] == category]
    trials = random.sample(list(filtered.to_dict(orient="records")), 3)

    # Choose random version and set correct answer
    session_trials = []
    for trial in trials:
        show_original = random.choice([True, False])
        abstract_shown = trial["original_abstract"] if show_original else trial["incorrect_abstract"]
        correct_answer = "no" if show_original else "yes"
        session_trials.append({
            "doi": trial["doi"],
            "abstract": abstract_shown,
            "correct": correct_answer
        })

    session_store["category"] = category
    session_store["trial_index"] = 0
    session_store["trials"] = session_trials
    session_store["results"] = []

    return RedirectResponse("/trial", status_code=302)

@app.get("/trial", response_class=HTMLResponse)
async def trial(request: Request):
    idx = session_store.get("trial_index", 0)
    if idx >= 3:
        return RedirectResponse("/results", status_code=302)

    trial = session_store["trials"][idx]
    return templates.TemplateResponse("trial.html", {
        "request": request,
        "trial_num": idx + 1,
        "abstract": trial["abstract"]
    })

@app.post("/submit-trial", response_class=HTMLResponse)
async def submit_trial(request: Request, altered: str = Form(...), confidence: int = Form(...)):
    idx = session_store.get("trial_index", 0)
    trial = session_store["trials"][idx]
    correct = trial["correct"]

    session_store["results"].append({
        "trial": idx + 1,
        "user_guess": altered,
        "confidence": confidence,
        "correct_answer": correct,
        "is_correct": altered == correct
    })

    session_store["trial_index"] += 1
    return RedirectResponse("/trial", status_code=302)

@app.get("/results", response_class=HTMLResponse)
async def results(request: Request):
    return templates.TemplateResponse("results.html", {
        "request": request,
        "results": session_store["results"],
        "category": session_store.get("category", "N/A")
    })

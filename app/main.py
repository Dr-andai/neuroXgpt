from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import random
import os 

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Load dataset
hf_token = os.getenv("HUGGINGFACE_TOKEN")

df = pd.read_parquet(
    "hf://datasets/BrainGPT/BrainBench_GPT-4_v0.1.csv/data/train-00000-of-00001-1c06a67d80bbbd1d.parquet",
    storage_options={"token": hf_token}
)

session_store = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/start", response_class=HTMLResponse)
async def start(request: Request):
    trials_raw = df.sample(3).to_dict(orient="records")
    session_trials = []

    for trial in trials_raw:
        show_original = random.choice([True, False])
        abstract_shown = trial["original_abstract"] if show_original else trial["incorrect_abstract"]
        correct_answer = "no" if show_original else "yes"
        session_trials.append({
            "doi": trial["doi"],
            "journal_section": trial["journal_section"],
            "abstract": abstract_shown,
            "correct": correct_answer
        })

    session_store["trial_index"] = 0
    session_store["trials"] = session_trials
    session_store["results"] = []

    return RedirectResponse("/trial", status_code=302)

@app.get("/trial", response_class=HTMLResponse)
async def trial(request: Request):
    idx = session_store.get("trial_index", 0)
    trials = session_store.get("trials", [])

    if idx >= len(trials):
        return RedirectResponse("/results", status_code=302)

    trial = trials[idx]
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
        "is_correct": altered == correct,
        "journal_section": trial["journal_section"]
    })

    session_store["trial_index"] += 1
    return RedirectResponse("/trial", status_code=302)

@app.get("/results", response_class=HTMLResponse)
async def results(request: Request):
    return templates.TemplateResponse("results.html", {
        "request": request,
        "results": session_store["results"]
    })

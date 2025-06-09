from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# In-memory session tracking (for dev/demo only)
session_store = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/start", response_class=HTMLResponse)
async def start(request: Request, category: str = Form(...)):
    session_store["category"] = category
    session_store["trial"] = 1
    session_store["results"] = []
    return RedirectResponse("/trial", status_code=302)

@app.get("/trial", response_class=HTMLResponse)
async def trial(request: Request):
    if session_store.get("trial", 0) > 3:
        return RedirectResponse("/results", status_code=302)

    # Placeholder abstract for now
    abstract = "This is a placeholder abstract from the category: " + session_store.get("category", "Unknown")

    return templates.TemplateResponse("trial.html", {
        "request": request,
        "trial_num": session_store["trial"],
        "abstract": abstract
    })

@app.post("/submit-trial", response_class=HTMLResponse)
async def submit_trial(request: Request, altered: str = Form(...), confidence: int = Form(...)):
    session_store["results"].append({
        "trial": session_store["trial"],
        "user_guess": altered,
        "confidence": confidence,
        "correct_answer": "TODO"
    })
    session_store["trial"] += 1
    return RedirectResponse("/trial", status_code=302)

@app.get("/results", response_class=HTMLResponse)
async def results(request: Request):
    return templates.TemplateResponse("results.html", {
        "request": request,
        "results": session_store["results"],
        "category": session_store.get("category", "N/A")
    })

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit(
    request: Request,
    selected: str = Form(...),
    confidence: int = Form(...)
):
    # Placeholder for logic to store results and call model
    return templates.TemplateResponse("thank_you.html", {"request": request, "selected": selected, "confidence": confidence})

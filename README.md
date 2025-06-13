# 🧠 BrainBench: Abstract Alteration Detection Web App

BrainBench is a FastAPI-based web application that helps evaluate whether neuroscience abstracts have been synthetically altered. It enables both human users and an LLM (GPT-2) to determine if an abstract is original or machine-modified.

---

## 🚀 Features

- Users are shown a series of neuroscience abstracts.
- For each one, they decide whether the abstract has been altered.
- GPT-2 also gives its prediction via a model hosted on Hugging Face Spaces.
- After 3 trials, results are shown with side-by-side comparisons.

---

## 🛠 Tech Stack

- **FastAPI** – Backend server
- **Jinja2** – HTML templating
- **Hugging Face Transformers** – GPT-2 model for predictions
- **Hugging Face Spaces** – Hosting the LLM endpoint
- **Docker** – Containerization for deployment

---

## 🧪 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Dr-andai/neuro_app.git
cd brainbench
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the App

```bash
uvicorn app.main:app --reload
```

Then go to `http://127.0.0.1:8000`

---

## 🌐 Remote Model Endpoint

This app sends input to a Hugging Face Spaces endpoint that runs GPT-2:

```
https://andaimd-brainbench.hf.space/predict
```

### Request Format (JSON)

```json
{
  "input": "The abstract text here..."
}
```

### Response Format

```json
{
  "output": "The model’s predicted answer"
}
```

---

## 🧪 Dataset

We use a `parquet` file hosted on Hugging Face Datasets:
```
hf://datasets/BrainGPT/BrainBench_GPT-4_v0.1.csv
```

Columns:
- `doi`
- `journal_section`
- `original_abstract`
- `incorrect_abstract`

---

## 📁 Project Structure

```
brainbench/
├── app/
│   ├── main.py              # FastAPI app
│   ├── model_loader.py      # GPT-2 loader (optional for future local use)
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS styling
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🧑‍🔬 Authors

- **David Andai, MD** – Project lead, research design
- GPT-2 (🤖) – Automated prediction

---

## 📜 License

MIT License
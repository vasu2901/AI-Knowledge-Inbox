# AI Knowledge Inbox

AI Knowledge Inbox is a full-stack application that lets users:
1. Save short notes or URLs 
2. Ask questions over their saved content 
3. Get answers powered by a simple RAG pipeline 

The project is split into a **React frontend** and a **FastAPI backend**.

---

## Tech Stack

1. Frontend: React

2. Backend: FastAPI

3. Language: Python, JavaScript

4. AI Platform: Google Gemini

5. API Server: Uvicorn

6. Database: In-Memory Storage

---

## Setup

1. Clone the repository

```bash
git clone https://github.com/vasu2901/AI-Knowledge-Inbox
```

2. Frontend (React.js) Setup

```bash
cd frontend
npm i
```

3. Backend (FastApi) Setup

```bash
cd backend

# Create a virtual environment
python -m venv .venv

# Initialize the virtual environment

## Windows
./.venv/Scripts/activate

## MacOS/ Linux
source ./.venv/bin/activate

# Install the python libraries
pip install -r requirements.txt
```

4. Create two .env files inside each folder and add the respective values. For guidance, use .env.example file.

5. Open two different terminals for frontend and backend.

6. In terminal 1, Start the FastApi Server
```bash
uvicorn main:app --workers 1 # this command will work with in-memory storage and will not reload on any memory update.
```

7. In terminal 2, Start the React Server
```bash
npm start
```

---

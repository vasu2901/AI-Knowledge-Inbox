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

## ScreenShots

1. Storing a Text
2. Storing an URL
3. Fetching response for a prompt with context

---

## Sample Response - 

### Prompt - "Tell me About Serpwe"

### Response - 
```markdown
Serpwe is an AI-powered SEO tool designed to help users build topical authority and outrank competition by simplifying the SEO workflow into four steps: discovering keywords, organizing them into clusters, generating content briefs, and writing optimized content (Source: https://serpwe.com).

Key features and capabilities of the platform include:

*   **Keyword Discovery:** It identifies trending and semantically relevant keywords using autocomplete data from Google and Bing (Source: https://serpwe.com).
*   **Clustering:** The tool uses real-time SERP data and AI to group similar keywords into "Keyword Clusters." It also offers "Topical Clustering" using Natural Language Processing (NLP) to help users understand how these clusters relate to each other for content calendar planning (Source: https://serpwe.com).
*   **Content Briefs:** It generates outlines and structures based on real-time competitor analysis, including NLP-ready keywords and context to satisfy search intent (Source: https://serpwe.com).
*   **AI Writing Assistant:** This feature converts briefs into SEO-optimized, "human-like" articles. It includes built-in rank tracking and allows for real-time publishing to a CMS (Source: https://serpwe.com).
*   **Integrations:** Users can upload keywords from other popular SEO tools to be clustered within Serpwe (Source: https://serpwe.com).

According to user reviews, Serpwe is noted for its "unlimited pricing model," which distinguishes it from other credit-based clustering tools. It currently holds a 5/5 rating on ProductHunt and a 4/5 rating on Trustpilot, with over 1,000 users (Source: https://serpwe.com).

```


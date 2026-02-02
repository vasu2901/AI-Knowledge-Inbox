import requests
import numpy as np
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses  import JSONResponse
from pydantic import BaseModel
import os
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
from google import genai
from google.genai import types
import logging
from fastapi.encoders import jsonable_encoder

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:8000",
        "https://estrogenically-pitchiest-teisha.ngrok-free.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API")
)

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API"))

# In-Memory global chunks
CHUNKS = []
REQUEST_DATA = []

class Data(BaseModel):
    text: str = None
    url: str = None
    
class Query(BaseModel):
    prompt: str

# for creating embeddings
def embed(text: str):
    try:
        print(f"Generating embeddings for {text}")
        result = gemini_client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
        )
        print(f"Embeddings {result}")
        embedding = result.embeddings[0].values
        return np.array(embedding, dtype=np.float32)
    except Exception as e:
        logging.error(f"Embedding Error {e}")
        return None

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def extract_text_from_url(url: str) -> str:
    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style"]):
        s.decompose()
    return " ".join(soup.stripped_strings)

def store_chunks(chunks, source_type, source_ref):
    for chunk in chunks:
        CHUNKS.append({
            "text": chunk,
            "embedding": embed(chunk),
            "source_type": source_type,
            "source_ref": source_ref
        })
        
@app.post("/ingest")
def ingest(data: Data):
    
    if not data.text and not data.url:
        return JSONResponse(content={"message": "Invalid Request Body"}, status_code=400)
    elif data.text and data.url:
        return JSONResponse(content={"message": "Both text and url cant be sent in one body"}, status_code=406)
    elif data.text:
        chunks = chunk_text(data.text)
        store_chunks(chunks, "text", data.text)
        REQUEST_DATA.append({
            "data": data.text,
            "added_at": datetime.now()
        })
        return JSONResponse(content={"chunks_added": len(chunks)}, status_code=201)
    else:
        url_data = extract_text_from_url(data.url)
        chunks = chunk_text(url_data)
        store_chunks(chunks, "url", data.url)
        REQUEST_DATA.append({
            "data": data.url,
            "added_at": datetime.now()
        })
        return JSONResponse(content={"chunks_added": len(chunks)}, status_code=201)
    
@app.get("/items")
def items():
    return JSONResponse(content=jsonable_encoder({"items": REQUEST_DATA}), status_code=status.HTTP_200_OK)

@app.post("/query")
def query(query: Query):
    if not query.prompt:
        return JSONResponse(content={"message": "Invalid request Body"},status_code=400)
    elif not CHUNKS:
        return JSONResponse(content={"message": "No context added yet."}, status_code=422)
    else:
        embedded_prompt = embed(query.prompt)
        
        similarity_scores = []
        
        for chunk in CHUNKS:
            score = cosine_similarity(
                np.array(embedded_prompt).reshape(1, -1),
                np.array(chunk["embedding"]).reshape(1, -1)
            )[0][0]

            similarity_scores.append((score, chunk))        

        top = sorted(similarity_scores, key=lambda x: x[0], reverse=True)[:5]
        
        context = "\n\n".join(
            f"[Source: {c['source_type']} - {c['source_ref']}]\n{c['text']}"
            for _, c in top
        )
        
        prompt = f"""
            Answer the question using the context below.
            If the answer is not in the context, say you don't know.
            Cite sources.

            Context:
            {context}

            Question:
            {query.prompt}
            """
        try:
            response = gemini_client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            
            print(f"Gemini response - {response}")

            answer = response.text
            return JSONResponse(content={"answer": answer}, status_code=201)

        except Exception as e:
            logging.error(f"AI error: {e}")

            return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)

        

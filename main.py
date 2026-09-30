from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import os

app = FastAPI()

# Tüm faq.md içeriğini döndüren API uç noktası
@app.get("/api/all-faq")
async def get_all_faq():
    if not os.path.exists("faq.md"):
        return {"content": "faq.md dosyası bulunamadı."}
    with open("faq.md", "r", encoding="utf-8") as f:
        content = f.read()
    return {"content": content}

# CORS İzinlerini Tanımlıyoruz (Bağlantı kopmalarını engeller)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
# "static" klasörünü dış dünyaya açıyoruz (HTML, CSS, JS burdan sunulur)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Yerel embedding modeli (Cümleleri vektöre dönüştürür)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Qdrant İstemcisi (Bellek içi yerel veritabanı)
qdrant_client = QdrantClient(":memory:")
collection_name = "faq_collection"

qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config={"size": model.get_embedding_dimension(), "distance": "Cosine"}
)

# faq.md dosyasını okuyup Qdrant vektör tabanına işleyen fonksiyon
def init_vector_db():
    if not os.path.exists("faq.md"):
        print("[Uyarı] faq.md dosyası bulunamadı!")
        return
    
    with open("faq.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Soru bloklarına ayır
    sections = content.split("## Soru: ")[1:]
    documents = []
    
    for i, sec in enumerate(sections):
        lines = sec.split("\n")
        question = lines[0].strip()
        answer = "\n".join(lines[1:]).replace("Cevap:", "").strip()
        full_text = f"Soru: {question} Cevap: {answer}"
        documents.append({"id": i, "text": full_text, "question": question, "answer": answer})

    if not documents:
        return

    # Vektörleştir
    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts).tolist()
    
    # Qdrant için PointStruct nesnelerini oluşturuyoruz
    points = [
        models.PointStruct(
            id=doc["id"],
            vector=embeddings[idx],
            payload={"question": doc["question"], "answer": doc["answer"]}
        )
        for idx, doc in enumerate(documents)
    ]

    qdrant_client.upsert(
        collection_name=collection_name,
        points=points
    )
    print(f"[Sistem] {len(documents)} adet SSS kaydı Qdrant veritabanına başarıyla yüklendi.")

# Sunucu ayağa kalkarken veritabanını doldur
init_vector_db()

# Anlamsal Soru Arama API Uç Noktası
@app.post("/api/ask")
async def ask_question(request: Request):
    data = await request.json()
    query = data.get("query", "")
    
    if not query:
        return {"answer": "Lütfen geçerli bir soru yazın."}
    
    # Kullanıcı sorusunu vektöre çevir
    query_vector = model.encode(query).tolist()
    
    # Qdrant'ta en yakın anlamsal eşleşmeyi güncel query_points metodu ile arıyoruz
    search_result = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=1
    ).points
    
    if search_result:
        best_match = search_result[0].payload
        return {
            "question": best_match["question"],
            "answer": best_match["answer"]
        }
    return {"answer": "Aradığınız kriterlerle ilgili faq.md dosyasında bir bilgi bulunamadı."}

# Anasayfa İstismarı (static/UI.html dosyasını tarayıcıya sunar)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    html_path = os.path.join("static", "UI.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Hata: static/UI.html dosyası bulunamadı. Lütfen static klasörü içine UI.html ekleyin.</h3>"
from fastapi import FastAPI

from app.schemas import MaterialCreate


app = FastAPI(title="Функция", version="0.1.0")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/materials/validate", response_model=MaterialCreate)
def validate_material(material: MaterialCreate):
    return material

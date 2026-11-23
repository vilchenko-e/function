from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app import materials
from app.database import initialize_database
from app.schemas import MaterialCreate, MaterialRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Функция",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/materials/validate", response_model=MaterialCreate)
def validate_material(material: MaterialCreate):
    return material


@app.post(
    "/api/materials",
    response_model=MaterialRead,
    status_code=201,
)
def create_material(material: MaterialCreate):
    created_material = materials.create_material(material)

    if created_material is None:
        return JSONResponse(
            status_code=409,
            content={"detail": "Такой материал уже существует"},
        )

    return created_material


@app.get("/api/materials", response_model=list[MaterialRead])
def list_materials():
    return materials.list_materials()


@app.get("/api/materials/{material_id}", response_model=MaterialRead)
def get_material(material_id: int):
    material = materials.get_material(material_id)

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Материал не найден",
        )

    return material

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, os

app = FastAPI(title="3D Weather Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"


def load_json(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return {"error": f"{name} not found"}
    return json.load(open(path))


@app.get("/")
def home():
    return {
        "status": "Backend running",
        "endpoints": {
            "wind_raw": "/wind/{level}/{step}",
            "wind_small": "/wind/{level}/{step}/small",
            "temperature": "/temperature/{step}",
            "pressure": "/pressure",
            "clouds": "/clouds"
        }
    }


@app.get("/wind/{level}/{step}")
def wind(level: str, step: str):
    return load_json(f"wind_{level}_f{step}.json")



@app.get("/temperature/{step}")
def temperature(step: str):
    return load_json(f"temperature_f{step}.json")


@app.get("/pressure")
def pressure():
    return load_json("pressure.json")


@app.get("/clouds")
def clouds():
    return load_json("clouds.json")


@app.get("/wind/{level}/{step}/small")
def wind_small(level: str, step: str):
    data = load_json(f"wind_{level}_f{step}.json")

    stride = 5  # reduce resolution
    return {
        "lat": data["lat"][::stride],
        "lon": data["lon"][::stride],
        "u": [row[::stride] for row in data["u"][::stride]],
        "v": [row[::stride] for row in data["v"][::stride]],
    }

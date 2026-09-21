from fastapi import FastAPI

from app.core.config import DEBUG
from app.schemas.ads import AdCreate

app = FastAPI(
    debug=DEBUG,
    title='API',
    summary='API for advertisement',
    version='0.0.1'
)

@app.post('/advertisement')
def create_ad(ad: AdCreate):
    pass
from fastapi import FastAPI
from routers import UploadLocalImgs

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# include the router
app.include_router(UploadLocalImgs.router)

# Path: routers/UploadLocalImgs.py

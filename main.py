from fastapi import FastAPI
from routers import upload_local_imgs_webui
from fastapi import FastAPI, Form


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# include the router
app.include_router(UploadLocalImgs.router)

# Path: routers/upload_local_imgs_webui.py

app = FastAPI()


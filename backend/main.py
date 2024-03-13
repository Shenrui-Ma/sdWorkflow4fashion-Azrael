from fastapi import FastAPI
from routers import UploadLocalImg

app = FastAPI()

app.include_router(UploadLocalImg.router)  # 将get_localimg的路由添加到你的应用中

@app.get("/")
def read_root():
    return {"Hello": "World"}
# local txt2img E:\novelai-webui-aki-v3\outputs\txt2img-images
# local img2img E:\novelai-webui-aki-v3\outputs\img2img-images
# local extras E:\novelai-webui-aki-v3\outputs\extras-images

# always get 3 newest images from each folder and return them as a list of dictionaries
# interface in 3 routes: /txt2img, /img2img, /extras

import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
import os
from datetime import datetime
import json

router = APIRouter()

# 全部改成返回json格式
def get_newest_images(folder_path, num_images):
    # get all files in the folder
    files = os.listdir(folder_path)
    # sort by creation date
    files.sort(key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    # get the 3 newest files
    newest_files = files[-num_images:] 
    # return the newest files
    return newest_files

# txt2img
@router.get("/txt2img")
async def get_txt2img_images():
    # get the 3 newest images from the txt2img folder
    txt2img_images = get_newest_images("E:/novelai-webui-aki-v3/outputs/txt2img-images", 3)
    # return the image paths as JSON
    return jsonable_encoder(txt2img_images)

# img2img
@router.get("/img2img")
async def get_img2img_images():
    # get the 3 newest images from the img2img folder
    img2img_images = get_newest_images("E:/novelai-webui-aki-v3/outputs/img2img-images", 3)
    # return the image paths as JSON
    return jsonable_encoder(img2img_images)

# extras
@router.get("/extras")
async def get_extras_images():
    # get the 3 newest images from the extras folder
    extras_images = get_newest_images("E:/novelai-webui-aki-v3/outputs/extras-images", 3)
    # return the image paths as JSON
    return jsonable_encoder(extras_images)





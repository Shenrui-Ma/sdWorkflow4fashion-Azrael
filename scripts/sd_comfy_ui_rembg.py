# 模板名称是rembg.json

import json
import base64
import websocket
from PIL import Image
import io
from sd_comfy_ui_api import SDComfyUIApi, SDComfyUIConfig, SDComfyUI_i2i_Api


# 调用SDComfyUI_i2i_Api类的generate_image_from_image方法生成图像，只不过template_name是rembg,并且prompt为空, output_node_id是10
config=SDComfyUIConfig(server_ip="127.0.0.1", server_port=8188)
sd_client=SDComfyUI_i2i_Api(config)

def rembg(image_path):
    
    image_data=sd_client.generate_image_from_image(image_path=image_path, template_name="rembg", output_node_id="10")

    # show
    if image_data:
        image=Image.open(io.BytesIO(image_data))
        image.show()
    else:
        print("未能生成图像，请检查输入参数和服务器配置。")

    return image_data

if __name__=="__main__":
    image_path=r"C:\Users\KingR\Desktop\Weixin Image_20240330231541.png"
    rembg(image_path)


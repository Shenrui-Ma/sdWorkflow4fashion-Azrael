# 模板是change_cloth(masked&rmvbg).json

import json
import base64
import websocket
from PIL import Image
import io
from sd_comfy_ui_api import SDComfyUIApi, SDComfyUIConfig

class SDComfyUIDressUpApi(SDComfyUIApi):
    def __init__(self, config: SDComfyUIConfig) -> None:
        super().__init__(config)

    def image_to_base64(self, image_path):
        # 将图片转换为Base64编码
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def generate_dressed_image(self, person_image_path, clothes_image_path, template_name, output_node_id) -> bytes:
        # 读取模板
        TEMPLATE_TEXT = open(f"./templates/{template_name}.json", encoding='utf-8').read()
        workflow = json.loads(TEMPLATE_TEXT)

        # 将人物图片和衣服图片转换为Base64编码
        person_image_base64 = self.image_to_base64(person_image_path)
        clothes_image_base64 = self.image_to_base64(clothes_image_path)

        # 修改工作流模板中的节点以接收Base64编码的图片
        workflow["10"]["inputs"]["image"] = person_image_base64  # 节点10接收人物图片
        workflow["15"]["inputs"]["image"] = clothes_image_base64  # 节点15接收衣服图片

        # 使用WebSocket连接发送工作流并接收生成的图片
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.SERVER_ADDRESS, self.CLIENT_ID))
        images = self.get_images(ws, workflow)
        ws.close()

        # 返回指定节点ID的第一张图像
        return images[output_node_id][0] if output_node_id in images else None

# 使用示例
config = SDComfyUIConfig(server_ip='127.0.0.1', server_port=8188)
dress_up_api = SDComfyUIDressUpApi(config)
dressed_image = dress_up_api.generate_dressed_image(
    person_image_path='path_to_person_image.png',
    clothes_image_path='path_to_clothes_image.png',
    template_name='dress_up_template',
    output_node_id='24'  # 根据模板，节点24是保存图像的节点
)

# 将生成的图片保存到文件
if dressed_image:
    with open('dressed_person.png', 'wb') as image_file:
        image_file.write(dressed_image)


def main(config):
    # 初始化SDComfyUIDressUpApi实例，设置服务器IP
    server_ip = "127.0.0.1"
    sd_client = SDComfyUIDressUpApi(SDComfyUIConfig(server_ip=server_ip))
    
    # 从config获取参数
    person_image_path = config.person_image_path
    clothes_image_path = config.clothes_image_path
    template_name = config.template_name
    output_node_id = config.output_node_id
    
    # 生成穿衣图片
    image_data = sd_client.generate_dressed_image(person_image_path, clothes_image_path, template_name, output_node_id)
    # 这里可以添加代码来处理image_data，例如保存到文件或显示图像

    # 显示图像
    if image_data:
        image = Image.open(io.BytesIO(image_data))
        image.show()
    else:
        print("未能生成图像，请检查输入参数和服务器配置。")

if __name__ == "__main__":
    # 设置自定义参数
    person_image_path = "path_to_person_image.png"
    clothes_image_path = "path_to_clothes_image.png"
    template_name = "dress_up_template"
    output_node_id = "24"  # 根据模板，节点24是保存图像的节点
    
    # 创建config
    config = SDComfyUIConfig(server_ip="127.0.0.1", template_name=template_name, output_node_id=output_node_id)
    config.person_image_path = person_image_path
    config.clothes_image_path = clothes_image_path
    
    main(config)

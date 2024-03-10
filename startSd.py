import requests
import base64
from PIL import Image
import io

# 定义Stable Diffusion Web UI的API端点URL
url = 'https://your-stable-diffusion-web-ui-url.com/sdapi/v1/txt2img'

# 定义要发送的prompt
prompt = "a red dress with floral pattern"

# 构建请求payload
payload = {
    "prompt": prompt,
    "steps": 50,  # 生成图片的步数
    "seed": 5  # 随机种子
}

# 发送POST请求
response = requests.post(url, json=payload)

# 解析响应
data = response.json()
image_data = base64.b64decode(data['images'][0])

# 将图片数据转换为PIL图像
image = Image.open(io.BytesIO(image_data))

# 显示图片
image.show()
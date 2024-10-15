import cv2
import io
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from rembg.bg import remove
print("导入rembg成功")
import os

if __name__ == '__main__':
    img_url = r"E:\ComfyUI-aki\ComfyUI-aki-v1.3\output\ComfyUI_00360_.png"
    folder_path = os.path.dirname(img_url) 
    with open(img_url, 'rb') as f:
        a = f.read()

    result_a = remove(data=a)
    result_Image = Image.open(io.BytesIO(result_a))
    result_numpy = np.asarray(result_Image)

    plt.subplot(1, 2, 1)
    plt.imshow(cv2.imread(img_url))
    plt.title('original image')

    plt.subplot(1, 2, 2)
    plt.imshow(result_numpy)
    plt.title('remove background image')
    plt.show()

    # 获取文件名和文件夹路径
    file_name = os.path.basename(img_url)
    older_path = os.path.dirname(img_url)

    # 将字节对象转换为NumPy数组并保存处理后的图像
    result_numpy_uint8 = (result_numpy).astype(np.uint8)

    # 翻转颜色
    result_rgb = cv2.cvtColor(result_numpy_uint8, cv2.COLOR_BGR2RGB)

    save_path = os.path.join(folder_path, 'removed_' + file_name)
    cv2.imwrite(save_path, result_rgb)
    print('Image saved successfully at:', save_path)
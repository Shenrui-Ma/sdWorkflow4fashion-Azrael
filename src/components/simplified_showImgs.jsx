import React, { useState } from 'react';

// 图片展示组件
const ImageDisplay = ({ images }) => {
  return (
    <div>
      {images.map((image, index) => (
        <img key={index} src={image} alt={`Image ${index}`} />
      ))}
    </div>
  );
};

// 主程序组件
const App = () => {
  // 定义状态
  const [txt2imgImages, setTxt2imgImages] = useState([]);
  const [img2imgImages, setImg2imgImages] = useState([]);
  const [extrasImages, setExtrasImages] = useState([]);

  const handleClick = async () => {
    const txt2imgResponse = await fetch('http://localhost:5173/txt2img');
    //先输出response看类型
    console.log(txt2imgResponse);// 发现类型是Response，不是json,所以要转化为json
    // 转化为json:
    const txt2imgImages = await txt2imgResponse.json();
    // 输出转化后的json看类型
    console.log(txt2imgImages);// 发现类型是数组，可以直接使用
    setTxt2imgImages(txt2imgImages.json);
  

    const img2imgResponse = await fetch('http://localhost:5173/img2img');
    const img2imgImages = await img2imgResponse.json();
    setImg2imgImages(img2imgImages);

    const extrasResponse = await fetch('http://localhost:5173/extras');
    const extrasImages = await extrasResponse.json();
    setExtrasImages(extrasImages);
};

  // 页面渲染
  return (
    <div>
      <button onClick={handleClick}>获取图片</button>
      <ImageDisplay images={txt2imgImages} />
      <ImageDisplay images={img2imgImages} />
      <ImageDisplay images={extrasImages} />
    </div>
  );
};

export default App;
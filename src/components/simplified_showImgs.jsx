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
    // 调用API端点以获取图片
    const txt2imgResponse = await fetch('/txt2img');
    const txt2imgData = await txt2imgResponse.json();
    console.log(txt2imgData); // 打印获取的数据
    setTxt2imgImages(txt2imgData);
  
    const img2imgResponse = await fetch('/img2img');
    const img2imgData = await img2imgResponse.json();
    setImg2imgImages(img2imgData);
  
    const extrasResponse = await fetch('/extras');
    const extrasData = await extrasResponse.json();
    setExtrasImages(extrasData);
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
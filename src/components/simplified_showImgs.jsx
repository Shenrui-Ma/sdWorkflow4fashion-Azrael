import React, { useState } from 'react';

// 图片展示组件
const ImageDisplay = ({ images }) => {
  if (!Array.isArray(images)) {
    return <div>Error: images is not an array</div>;
  }
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
    // txt2img
    const txt2imgUrl = 'http://localhost:5173/txt2img';
    try {
      const txt2imgResponse = await fetch(txt2imgUrl);
      const txt2imgImages = await txt2imgResponse.json();
      setTxt2imgImages(prevImages => [...prevImages, ...txt2imgImages]);
    } catch (error) {
      console.error('Error fetching txt2img:', error);
    }
  
    // img2img
    const img2imgUrl = 'http://localhost:5173/img2img';
    try {
      const img2imgResponse = await fetch(img2imgUrl);
      const img2imgImages = await img2imgResponse.json();
      setImg2imgImages(prevImages => [...prevImages, ...img2imgImages]);
    } catch (error) {
      console.error('Error fetching img2img:', error);
    }
  
    // extras
    const extrasUrl = 'http://localhost:5173/extras';
    try {
      const extrasResponse = await fetch(extrasUrl);
      const extrasImages = await extrasResponse.json();
      setExtrasImages(prevImages => [...prevImages, ...extrasImages]);
    } catch (error) {
      console.error('Error fetching extras:', error);
    }
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
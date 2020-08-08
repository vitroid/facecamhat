# facecamhat

picameraで撮影し、opencvで顔認識し、顔の部分だけをunicornhathd(16x16 pixels)に表示するサンプルプログラム。

## Requirements

* Raspbian-lite

## Installation

もっぱら大変なのは、OpenCVをRaspbian上で動くようにする準備。

```shell
% make install
```

## Test

```shell
python3 camera_opencv.py
```

## Sample

![](https://i.gyazo.com/f6978ffdba7bf8b2458c547d57970b7f.jpg)

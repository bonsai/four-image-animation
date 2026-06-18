# Four Image Animation

4枚の画像から90秒のアニメーション動画を生成するツールです。

## 前提条件

- [FFmpeg](https://ffmpeg.org/) がインストールされていること

## 使い方

### Linux/Mac

```bash
chmod +x animate.sh
./animate.sh image1.png image2.png image3.png image4.png
```

### Windows

```batch
animate.bat image1.png image2.png image3.png image4.png
```

## 出力

- `output.mp4` - 90秒のアニメーション動画（1920x1080、30fps）

## 特徴

- 各画像にフェードイン/フェードアウト効果
- 画像は1920x1080にリサイズ（アスペクト比保持）
- 合計90秒の動画を生成

## 画像の準備

`images/` フォルダにアニメーションに使用する4枚の画像を配置してください。

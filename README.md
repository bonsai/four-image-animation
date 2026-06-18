# Four Image Animation

Ollama + Stable Diffusion 1.5 + Stable Video Diffusion (SVD) を使った
AI自動アニメーション生成パイプライン。

4枚の「はがきサイズ」イラストを生成し、それぞれをアニメーション化して
スマホ縦型（9:16）の90秒動画を自動生成します。

## 概要

```
テーマ入力 → Ollama (ストーリー) → SD 1.5 (画像) → SVD (動画) → FFmpeg → 90秒動画
```

## 前提条件

- Python 3.10+
- [FFmpeg](https://ffmpeg.org/)
- [Ollama](https://ollama.ai/) (ローカルサーバー)
- GPU推奨 (VRAM 8GB以上)

## セットアップ

```bash
git clone https://github.com/bonsai/four-image-animation.git
cd four-image-animation
pip install -r requirements.txt
ollama pull llama3
```

## 使い方

```bash
python main.py --theme "夏の冒険"
```

## パイプライン

| ステップ | 出力 |
|---------|------|
| 1. ストーリー生成 (Ollama) | 4シーンのプロンプト + ナレーション |
| 2. 画像生成 (SD 1.5) | はがきサイズ画像×4枚 (1024×576) |
| 3. 動画生成 (SVD) | アニメーションクリップ×4 |
| 4. 動画編集 (FFmpeg) | output.mp4 (90秒、1080×1920) |

## 出力仕様

| 項目 | 仕様 |
|------|------|
| 解像度 | 1080 × 1920 px (9:16) |
| フレームレート | 24 fps |
| 総尺 | 90秒 |
| シーン数 | 4 |

詳細は [PRD.md](PRD.md) を参照。

#!/usr/bin/env python3
"""
AI Animation Pipeline
Ollama + SD 1.5 + SVD で4枚の画像から90秒アニメーションを生成
"""

import argparse
import yaml
from pathlib import Path
from modules.story_generator import StoryGenerator
from modules.image_generator import ImageGenerator
from modules.video_generator import VideoGenerator
from modules.video_editor import VideoEditor


def load_config(config_path: str = "config.yaml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="AI Animation Pipeline")
    parser.add_argument("--theme", type=str, help="アニメーションのテーマ")
    parser.add_argument("--config", type=str, default="config.yaml", help="設定ファイルパス")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.theme:
        config["theme"] = args.theme

    print(f"=== AI Animation Pipeline ===")
    print(f"テーマ: {config['theme']}")
    print()

    # Step 1: ストーリー生成 (Ollama)
    print("[Step 1/4] ストーリー生成中...")
    story_gen = StoryGenerator(config)
    story = story_gen.generate(config["theme"])
    print(f"  -> {len(story['scenes'])}シーン生成完了")
    print()

    # Step 2: 画像生成 (SD 1.5)
    print("[Step 2/4] 画像生成中...")
    image_gen = ImageGenerator(config)
    images = image_gen.generate_batch(story["scenes"])
    print(f"  -> {len(images)}枚の画像生成完了")
    print()

    # Step 3: 動画生成 (SVD)
    print("[Step 3/4] アニメーション生成中...")
    video_gen = VideoGenerator(config)
    clips = video_gen.generate_batch(images)
    print(f"  -> {len(clips)}クリップ生成完了")
    print()

    # Step 4: 動画編集 (FFmpeg)
    print("[Step 4/4] 動画編集中...")
    editor = VideoEditor(config)
    output_path = editor.combine(clips, story["narrations"])
    print(f"  -> 出力: {output_path}")
    print()

    print("=== 完了 ===")


if __name__ == "__main__":
    main()

"""
FFmpegを使った動画編集モジュール
"""

import subprocess
from pathlib import Path


class VideoEditor:
    def __init__(self, config: dict):
        self.config = config
        self.output_config = config.get("output", {})
        self.scene_config = config.get("scenes", {})

    def combine(self, clips: list, narrations: list = None) -> Path:
        """クリップを結合して最終動画を生成"""
        output_width = self.output_config.get("resolution", {}).get("width", 1080)
        output_height = self.output_config.get("resolution", {}).get("height", 1920)
        fps = self.output_config.get("fps", 24)
        transition_duration = self.scene_config.get("transition_duration", 1.0)

        output_path = Path(self.config["paths"]["output_file"])

        # 一時ファイルリストを作成
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)

        resized_clips = []
        for i, clip in enumerate(clips, 1):
            resized_path = temp_dir / f"resized_{i:02d}.mp4"
            # 9:16にリサイズして回転
            cmd = [
                "ffmpeg", "-y",
                "-i", str(clip),
                "-vf", f"scale={output_height}:{output_width}:force_original_aspect_ratio=decrease,"
                       f"pad={output_height}:{output_width}:(ow-iw)/2:(oh-ih)/2,"
                       f"transpose=1",
                "-r", str(fps),
                str(resized_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            resized_clips.append(resized_path)

        # ファイルリストを作成
        concat_file = temp_dir / "concat.txt"
        with open(concat_file, "w") as f:
            for clip in resized_clips:
                f.write(f"file '{clip.absolute()}'\n")

        # 結合
        temp_output = temp_dir / "combined.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-t", str(self.output_config.get("duration", 90)),
            str(temp_output)
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        # 最終出力にコピー
        import shutil
        shutil.move(str(temp_output), str(output_path))

        # 一時ファイルを削除
        import shutil as sh
        sh.rmtree(temp_dir, ignore_errors=True)

        return output_path

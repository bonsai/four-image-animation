"""
Stable Video Diffusion (SVD) 動画生成モジュール
"""

import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
from pathlib import Path


class VideoGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.video_config = config.get("video", {})
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # SVDパイプライン初期化
        model_id = self.video_config.get(
            "model",
            "stabilityai/stable-video-diffusion-img2vid-xt"
        )
        self.pipe = StableVideoDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)

        # 出力ディレクトリ作成
        self.output_dir = Path(config["paths"]["videos_dir"])
        self.output_dir.mkdir(exist_ok=True)

    def generate(self, image_path: Path, scene_number: int) -> Path:
        """単一画像からアニメーションを生成"""
        frames = self.video_config.get("frames", 25)
        motion_bucket_id = self.video_config.get("motion_bucket_id", 127)
        guidance_scale = self.video_config.get("guidance_scale", 3.0)

        # 画像をロード
        image = load_image(str(image_path))

        # アニメーション生成
        generator = torch.Generator(device=self.device)
        generator.manual_seed(42)

        output_frames = self.pipe(
            image,
            num_frames=frames,
            motion_bucket_id=motion_bucket_id,
            guidance_scale=guidance_scale,
            generator=generator
        ).frames[0]

        # 動画として保存
        output_path = self.output_dir / f"clip_{scene_number:02d}.mp4"
        export_to_video(output_frames, str(output_path), fps=24)

        return output_path

    def generate_batch(self, image_paths: list) -> list:
        """複数画像からアニメーションを生成"""
        paths = []
        for i, image_path in enumerate(image_paths, 1):
            path = self.generate(image_path, i)
            paths.append(path)
        return paths

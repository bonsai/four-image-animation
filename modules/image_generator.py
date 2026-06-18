"""
Stable Diffusion 1.5 画像生成モジュール
"""

import torch
from diffusers import StableDiffusionPipeline
from pathlib import Path


class ImageGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.image_config = config.get("image", {})
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # パイプライン初期化
        model_id = self.image_config.get("model", "runwayml/stable-diffusion-v1-5")
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)

        # 出力ディレクトリ作成
        self.output_dir = Path(config["paths"]["images_dir"])
        self.output_dir.mkdir(exist_ok=True)

    def generate(self, prompt: str, scene_number: int) -> Path:
        """単一画像を生成"""
        width = self.image_config.get("width", 1024)
        height = self.image_config.get("height", 576)
        steps = self.image_config.get("steps", 30)
        guidance_scale = self.image_config.get("guidance_scale", 7.5)

        image = self.pipe(
            prompt,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale
        ).images[0]

        output_path = self.output_dir / f"scene_{scene_number:02d}.png"
        image.save(output_path)
        return output_path

    def generate_batch(self, scenes: list) -> list:
        """複数シーンの画像を生成"""
        paths = []
        for scene in scenes:
            path = self.generate(
                scene["image_prompt"],
                scene["scene_number"]
            )
            paths.append(path)
        return paths

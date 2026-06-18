"""
Ollamaを使ったストーリー生成モジュール
"""

import json
import ollama
from pathlib import Path


STORY_PROMPT_TEMPLATE = """
あなたはアニメーションの脚本家です。
以下のテーマで4シーンの物語を作成してください。

テーマ: {theme}

各シーンについて以下のJSON形式で出力してください:
{{
  "scenes": [
    {{
      "scene_number": 1,
      "title": "シーンタイトル",
      "image_prompt": "画像生成プロンプト（英語、 Stable Diffusion形式）",
      "animation_description": "アニメーションの動き説明",
      "narration": "ナレーション（日本語、短めに）"
    }}
  ]
}}

出力はJSONのみを返してください。マークダウンは不要です。
"""


class StoryGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.ollama_config = config.get("ollama", {})
        self.model = self.ollama_config.get("model", "llama3")
        self.host = self.ollama_config.get("host", "http://localhost:11434")

    def generate(self, theme: str) -> dict:
        """テーマからストーリーを生成"""
        prompt = STORY_PROMPT_TEMPLATE.format(theme=theme)

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.8}
        )

        # JSONをパース
        story_text = response["response"]
        # JSONブロックを抽出
        if "```json" in story_text:
            story_text = story_text.split("```json")[1].split("```")[0]
        elif "```" in story_text:
            story_text = story_text.split("```")[1].split("```")[0]

        story = json.loads(story_text.strip())

        # 保存
        output_dir = Path(self.config["paths"]["videos_dir"])
        output_dir.mkdir(exist_ok=True)
        with open(output_dir / "story.json", "w", encoding="utf-8") as f:
            json.dump(story, f, ensure_ascii=False, indent=2)

        return story

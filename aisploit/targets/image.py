import json
import os
from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from openai import OpenAI

from ..core import BaseImageTarget, BasePromptValue, ContentFilteredException, Response


@dataclass
class BaseBedrockImageTarget(BaseImageTarget, ABC):
    session: boto3.Session = field(default_factory=lambda: boto3.Session())
    region_name: str = "us-east-1"

    def __post_init__(self):
        self._client = self.session.client("bedrock-runtime", region_name=self.region_name)


@dataclass
class BedrockAmazonImageTarget(BaseBedrockImageTarget):
    model: str = "titan-image-generator-v1"
    quality: str = "standard"
    seed: int = 0
    cfg_scale: int = 8

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        width, height = self.size.split("x")
        body = {
            "textToImageParams": {
                "text": prompt.to_string(),
            },
            "taskType": "TEXT_IMAGE",
            "imageGenerationConfig": {
                "seed": self.seed,
                "cfgScale": self.cfg_scale,
                "quality": self.quality,
                "width": int(width),
                "height": int(height),
                "numberOfImages": 1,
            },
        }

        try:
            response = self._client.invoke_model(
                body=json.dumps(body),
                modelId=f"amazon.{self.model}",
            )

            response_body = json.loads(response["body"].read())

            if response_body["error"]:
                raise Exception(response_body["error"])

            base64_image = response_body["images"][0]

            if self.show_image:
                self._show_base64_image(base64_image)

            return Response(content=base64_image)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                if "blocked by our content filters" in e.response['Error']['Message']:
                    raise ContentFilteredException(e.response['Error']['Message']) from e

            raise e


@dataclass
class BedrockStabilityImageTarget(BaseBedrockImageTarget):
    model: str = "stable-diffusion-xl-v1"
    steps: int = 50
    seed: int = 0
    cfg_scale: int = 8

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        width, height = self.size.split("x")
        body = {
            "text_prompts": [{"text": prompt.to_string(), "weight": 1}],
            "seed": self.seed,
            "cfg_scale": self.cfg_scale,
            "width": int(width),
            "height": int(height),
            "steps": self.steps,
        }

        response = self._client.invoke_model(
            body=json.dumps(body),
            modelId=f"stability.{self.model}",
        )

        response_body = json.loads(response["body"].read())

        finish_reason = response_body.get("artifacts")[0].get("finishReason")

        if finish_reason == "CONTENT_FILTERED":
            raise ContentFilteredException(f"Image error: {finish_reason}")

        if finish_reason == "ERROR":
            raise Exception(f"Image error: {finish_reason}")

        base64_image = response_body["artifacts"][0]["base64"]

        if self.show_image:
            self._show_base64_image(base64_image)

        return Response(content=base64_image)


@dataclass
class OpenAIImageTarget(BaseImageTarget):
    api_key: Optional[str] = None

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.environ["OPENAI_API_KEY"]

        self._client = OpenAI(api_key=self.api_key)

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        response = self._client.images.generate(
            prompt=prompt.to_string(),
            size=self.size,
            n=1,
            response_format="b64_json",
        )

        base64_image = response.data[0].b64_json

        if self.show_image:
            self._show_base64_image(base64_image)

        return Response(content=base64_image)

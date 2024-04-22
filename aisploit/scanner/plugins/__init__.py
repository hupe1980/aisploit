from .image_markdown_injection import ImageMarkdownInjectionPlugin
from .many_shot import ManyShotPlugin
from .prompt_injection import PromptInjectionPlugin
from .sample_signatures import EICARPlugin, GTPhishPlugin, GTubePlugin
from .self_similarity import SelfSimilarityPlugin

__all__ = [
    "ImageMarkdownInjectionPlugin",
    "ManyShotPlugin",
    "PromptInjectionPlugin",
    "EICARPlugin",
    "GTubePlugin",
    "GTPhishPlugin",
    "SelfSimilarityPlugin",
]

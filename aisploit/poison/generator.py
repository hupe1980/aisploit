from typing import Literal
import random
import numpy as np
import torch

Device = Literal["cuda", "cpu", "mps"]


class PoisonGenerator:
    def __init__(self, *, device: Device = "cuda", seed: int = 4711) -> None:
        self._seed(seed)

    def _seed(self, seed: int) -> None:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)

from abc import ABC


class BaseJob(ABC):
    def __init__(self, *, verbose=False) -> None:
        self.verbose = verbose

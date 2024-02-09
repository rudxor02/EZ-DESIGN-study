from abc import ABC, abstractmethod

from pydantic import BaseModel


class CPU(ABC, BaseModel):
    @abstractmethod
    def process(self, data: list[int]) -> list[list[int]]:
        pass


class CPUFactory:
    @staticmethod
    def make_cpu(type: str) -> CPU:
        if type == "single":
            return SingleCoreCPU()
        elif type == "dual":
            return DualCoreCPU()
        else:
            raise ValueError("Invalid CPU type")


class SingleCoreCPU(CPU):
    def process(self, data: list[int]) -> list[list[int]]:
        return [data]


class DualCoreCPU(CPU):
    def process(self, data: list[int]) -> list[list[int]]:
        return [data[::2], data[1::2]]

from abc import ABC, abstractmethod
from typing import Optional


class Memory(ABC):
    size: int
    data: list[int]

    @abstractmethod
    def read(self, address: int) -> int:
        pass

    @abstractmethod
    def write(self, address: int, data: int) -> None:
        pass


class RAM(Memory):
    def __init__(self, size: int):
        self.size = size
        self.data = [0] * size

    def read(self, address: int):
        return self.data[address]

    def write(self, address: int, data: int):
        self.data[address] = data


class ROM(Memory):
    def __init__(self, data: list[int]):
        self.data = data
        self.size = len(data)

    def read(self, address: int):
        return self.data[address]

    def write(self, address: int, data: int):
        raise ValueError("Cannot write to ROM")


class MemoryFactory(ABC):
    @staticmethod
    @abstractmethod
    def make_memory(
        size: Optional[int] = None, data: Optional[list[int]] = None
    ) -> Memory:
        pass


class RamFactory(MemoryFactory):
    @staticmethod
    def make_memory(
        size: Optional[int] = None, data: Optional[list[int]] = None
    ) -> Memory:
        if data is not None:
            raise ValueError("Cannot initialize RAM with data")
        if size is None:
            raise ValueError("Size is required to initialize RAM")
        return RAM(size=size)


class RomFactory(MemoryFactory):
    @staticmethod
    def make_memory(
        size: Optional[int] = None, data: Optional[list[int]] = None
    ) -> Memory:
        if size is not None:
            raise ValueError("Cannot initialize ROM with size")
        if data is None:
            raise ValueError("Data is required to initialize ROM")
        return ROM(data=data)

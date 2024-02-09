from typing import TypedDict

from pydantic import BaseModel

from week1.cpu import CPU, CPUFactory
from week1.memory import Memory, RamFactory, RomFactory


class ComputerState(TypedDict):
    cpu_processed: list[list[int]]
    ram_data: list[int]
    rom_data: list[int]


class Computer(BaseModel):
    cpu: CPU
    ram: Memory
    rom: Memory

    def _load_all(self, memory: Memory) -> list[int]:
        return [memory.read(i) for i in range(memory.size)]

    def bootstrap(self) -> ComputerState:
        data = self._load_all(self.rom)
        cpu_processed = self.cpu.process(data)
        return {
            "cpu_processed": cpu_processed,
            "ram_data": self._load_all(self.ram),
            "rom_data": self._load_all(self.rom),
        }

    class Config:
        arbitrary_types_allowed = True


class ComputerBuilder:
    @staticmethod
    def build_computer(type: str) -> Computer:
        if type == "laptop":
            cpu = CPUFactory.make_cpu(type="single")
            ram = RamFactory.make_memory(size=8)
            rom = RomFactory.make_memory(data=[1, 2, 3, 4])
            return Computer(cpu=cpu, ram=ram, rom=rom)
        elif type == "desktop":
            cpu = CPUFactory.make_cpu(type="dual")
            ram = RamFactory.make_memory(size=16)
            rom = RomFactory.make_memory(data=[1, 2, 3, 4, 5, 6, 7, 8])
            return Computer(cpu=cpu, ram=ram, rom=rom)
        else:
            raise ValueError("Invalid computer type")

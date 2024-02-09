import pytest

from week1.computer import ComputerBuilder
from week1.cpu import CPUFactory
from week1.memory import RamFactory, RomFactory


@pytest.mark.computer
class TestComputer:
    def test_laptop(self):
        computer = ComputerBuilder.build_computer(type="laptop")
        state = computer.bootstrap()
        assert state["cpu_processed"] == [[1, 2, 3, 4]]
        assert state["ram_data"] == [0] * 8
        assert state["rom_data"] == [1, 2, 3, 4]

    def test_desktop(self):
        computer = ComputerBuilder.build_computer(type="desktop")
        state = computer.bootstrap()
        assert state["cpu_processed"] == [[1, 3, 5, 7], [2, 4, 6, 8]]
        assert state["ram_data"] == [0] * 16
        assert state["rom_data"] == [1, 2, 3, 4, 5, 6, 7, 8]

    def test_invalid_computer(self):
        with pytest.raises(ValueError):
            ComputerBuilder.build_computer(type="invalid")


@pytest.mark.memory
class TestMemory:
    def test_ram(self):
        memory = RamFactory.make_memory(size=8)
        assert memory.size == 8
        assert memory.read(0) == 0
        assert memory.read(7) == 0
        memory.write(0, 1)
        assert memory.read(0) == 1
        memory.write(7, 2)
        assert memory.read(7) == 2

    def test_rom(self):
        memory = RomFactory.make_memory(data=[1, 2, 3, 4])
        assert memory.size == 4
        assert memory.read(0) == 1
        assert memory.read(3) == 4
        with pytest.raises(ValueError):
            memory.write(0, 1)
        with pytest.raises(ValueError):
            memory.write(3, 4)

    def test_invalid_memory(self):
        with pytest.raises(ValueError):
            RamFactory.make_memory(data=[1, 2, 3, 4])
        with pytest.raises(ValueError):
            RomFactory.make_memory(size=8)


@pytest.mark.cpu
class TestCPU:
    def test_single_core(self):
        cpu = CPUFactory.make_cpu(type="single")
        assert cpu.process([1, 2, 3, 4]) == [[1, 2, 3, 4]]

    def test_dual_core(self):
        cpu = CPUFactory.make_cpu(type="dual")
        assert cpu.process([1, 2, 3, 4]) == [[1, 3], [2, 4]]

    def test_invalid_cpu(self):
        with pytest.raises(ValueError):
            CPUFactory.make_cpu(type="invalid")

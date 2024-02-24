import curses
from abc import ABC, abstractmethod
from curses import wrapper
from typing import Any

from pydantic import BaseModel


class CalculatorException(Exception):
    pass


class Calculator(BaseModel):
    history: list["Snapshot"] = []
    value: float = 0.0
    expression: str = ""

    def calculate(self) -> None:
        try:
            self.value = float(eval(self.expression))
            self.create_snapshot()
            self.expression = "%.3f" % self.value
        except Exception:
            raise CalculatorException("Invalid syntax")

    def create_snapshot(self):
        self.history.append(Snapshot(value=self.value, expression=self.expression))


class Snapshot(BaseModel):
    value: float
    expression: str


class Command(ABC):
    @staticmethod
    @abstractmethod
    def execute(calculator: Calculator, **kwargs: Any):
        pass


class Undo(Command):
    @staticmethod
    def execute(calculator: Calculator, **kwargs: Any):
        if calculator.history:
            sanpshot = calculator.history.pop()
            calculator.value = sanpshot.value
            calculator.expression = sanpshot.expression


class Do(Command):
    @staticmethod
    def execute(calculator: Calculator, **kwargs: Any):
        calculator.calculate()


class SaveExpression(Command):
    @staticmethod
    def execute(calculator: Calculator, **kwargs: Any):
        calculator.expression = kwargs["expression"]


class DeleteExpression(Command):
    @staticmethod
    def execute(calculator: Calculator, **kwargs: Any):
        calculator.expression = calculator.expression[:-1]


class PaintScreen(Command):
    @staticmethod
    def execute(calculator: Calculator, **kwargs: Any):
        screen = kwargs["screen"]
        screen.erase()
        ScreenH, ScreenW = screen.getmaxyx()
        instructions = [
            "Press 'q' to quit",
            "Press 'backspace' to delete",
            "Press 'enter' to calculate",
            "Press 'u' to undo",
        ]
        for i, instruction in enumerate(instructions):
            screen.addstr(i, 0, instruction)
        for i, snapshot in enumerate(calculator.history):
            str_ = f"{snapshot.expression} = " + "%.3f" % snapshot.value
            screen.addstr(i, ScreenW - 1 - len(str_), str_)
        screen.addstr(ScreenH - 1, 0, calculator.expression)


def main(screen: Any):
    calculator = Calculator()
    screen.clear()

    key = " "

    while key != "q":
        if ord(key) == curses.KEY_BACKSPACE or ord(key) == 127:
            DeleteExpression.execute(calculator)
        elif key == "\n":
            try:
                Do.execute(calculator)
            except CalculatorException as e:
                SaveExpression.execute(calculator, expression=e.args[0])
        elif key == "u":
            Undo.execute(calculator)
        else:
            SaveExpression.execute(calculator, expression=calculator.expression + key)

        PaintScreen.execute(calculator, screen=screen)

        key = screen.getkey()


wrapper(main)

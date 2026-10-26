from enum import IntEnum
from typing import NamedTuple
from sudoku_engine.basic_types import Color, Vertex , NO_VERTEX

class StepKind(IntEnum):
    
    ASSIGN = 0
    UNASSIGN = 1
    SOLUTION_FOUND = 2
    FINISHED = 3

class StepEvent(NamedTuple):
    kind: StepKind
    vertex: Vertex = NO_VERTEX
    color: Color = 0

    @staticmethod
    def assign(v: Vertex, c: Color) -> 'StepEvent':
        return StepEvent(StepKind.ASSIGN, v, c)

    @staticmethod
    def unassign(v: Vertex, c: Color) -> 'StepEvent':
        return StepEvent(StepKind.UNASSIGN, v, c)

    @staticmethod
    def solution_found() -> 'StepEvent':
        return StepEvent(StepKind.SOLUTION_FOUND , NO_VERTEX , 0)

    @staticmethod
    def finished() -> 'StepEvent':
        return StepEvent(StepKind.FINISHED , NO_VERTEX , 0)



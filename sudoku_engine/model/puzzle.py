from sudoku_engine.basic_types import Color, Vertex
from dataclasses import dataclass


class PuzzleFormatError(ValueError):
  def __init__(self, message: str, position: int):
    self.message = message
    self.position = position
    
  def __str__(self) -> str:
    if self.position == -1: return self.message
    return self.message + " tại chỉ mục " + str(self.position)


@dataclass(frozen=True, slots=True)
class Puzzle:
  givens: tuple[Color, ...]
  
  @staticmethod
  def fromString(text: str) -> 'Puzzle':
    if len(text) != 81: raise PuzzleFormatError("Độ dài phải là 81, nhận được " + str(len(text)), -1)
    
    A = []
    for i in range(len(text)):
      if (not (text[i] in '.0123456789')): raise PuzzleFormatError("Sai ký tự nhập vào", i)
      if text[i] != '.': A.append(int(text[i]))
      else: A.append(0)
      
    return Puzzle(tuple(A))
    

  @staticmethod
  def empty() -> 'Puzzle':
    return Puzzle(tuple(0 for _ in range(81)))
    
  def toString(self) -> str:
    
  
  def givenAt(self, v: Vertex) -> Color:
    ...
    
  def isGiven(self, v: Vertex) -> bool:
    ...
    
  def givenCount(self) -> int:
    ...
    
  def withGiven(self, v: Vertex, c: Color) -> 'Puzzle':
    ...
  
if __name__ == '__main__':
  A=Puzzle.fromString("01544nd410"*8+'s')
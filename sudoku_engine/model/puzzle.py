from sudoku_engine.basic_types import Color, Vertex
from dataclasses import dataclass


class PuzzleFormatError(ValueError):
  """Lớp lỗi khi nhập đề bài từ Puzzle.fromString() bị sai kí tự hoặc số lượng kí tự"""
  
  def __init__(self, message: str, position: int):
    self.message = message
    self.position = position
    
  def __str__(self) -> str:
    if self.position == -1: return self.message
    return self.message + " tại chỉ mục " + str(self.position)


@dataclass(frozen=True, slots=True)
class Puzzle:
  """Đọc đề bài tử chuỗi"""
  givens: tuple[Color, ...]
  
  @staticmethod
  def fromString(text: str) -> 'Puzzle':
    """Nhập đề bài từ chuỗi"""
    if len(text) != 81: raise PuzzleFormatError("Độ dài phải là 81, nhận được " \
                                                + str(len(text)), -1)
    
    A = []
    for i in range(len(text)):
      if (not (text[i] in '.0123456789')): raise PuzzleFormatError("Sai ký tự nhập vào", i)
      if text[i] != '.': A.append(int(text[i]))
      else: A.append(0)
      
    return Puzzle(tuple(A))
    

  @staticmethod
  def empty() -> 'Puzzle':
    """Tạo một đề bài trống"""
    return Puzzle(tuple(0 for _ in range(81)))
    
  def toString(self) -> str:
    res: str = ""
    for s in self.givens:
      if (s != 0): res += str(s)
      else: res += '.'
    return res
  
  def givenAt(self, v: Vertex) -> Color:
    return self.givens[v]
    
  def isGiven(self, v: Vertex) -> bool:
    """Kiểm tra xem một đỉnh của đề bài có là ô trống hay không"""
    if self.givens[v] != 0: return True
    return False
    
  def givenCount(self) -> int:
    """Số lượng ô manh mối của đề bài"""
    count = 0
    for num in self.givens:
      if num != 0: count += 1
    return count
    
  def withGiven(self, v: Vertex, c: Color) -> 'Puzzle':
    """Tạo một đề bài mới nhưng đỉnh v có màu c thay cho đề bài cũ"""
    new_givens = tuple(self.givens[i] if i != v else c for i in range(81))
    return Puzzle(new_givens)
  
if __name__ == '__main__':
  A=Puzzle.fromString("0154441045"*8+'4')
  print(A.toString())
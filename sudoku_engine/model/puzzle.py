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
    """Chuyển Puzzle thành chuỗi"""
    res: str = ""
    for s in self.givens:
      if (s != 0): res += str(s)
      else: res += '.'
    return res
  
  def givenAt(self, v: Vertex) -> Color:
    """Một đỉnh của đề bài có màu là gì"""
    return self.givens[v]
    
  def isGiven(self, v: Vertex) -> bool:
    """Nếu đỉnh có manh mối thì trả về True"""
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
  SAMPLE = ("53..7...." "6..195..." ".98....6." "8...6...3" "4..8.3..1"
            "7...2...6" ".6....28." "...419..5" "....8..79")

  def expect_error(text: str, position: int):
    try:
      Puzzle.fromString(text)
    except PuzzleFormatError as e:
      assert e.position == position, (text, e.position)
      return
    raise AssertionError("Không báo lỗi với: " + repr(text))

  p = Puzzle.fromString(SAMPLE)
  assert p.toString() == SAMPLE                     # fromString rồi toString
  assert p.givenCount() == 30
  assert (p.givenAt(0), p.givenAt(80), p.givenAt(2)) == (5, 9, 0)
  assert p.isGiven(1) and not p.isGiven(2)

  assert Puzzle.fromString("0" * 81) == Puzzle.empty()
  assert Puzzle.empty().toString() == "." * 81
  assert Puzzle.empty().givenCount() == 0

  e = Puzzle.empty()
  q = e.withGiven(40, 7)
  assert q.givenAt(40) == 7 and q.givenCount() == 1 and len(q.givens) == 81
  assert e.givenCount() == 0                        # đề cũ không đổi
  assert q.withGiven(40, 0) == e

  for bad in ("", "1" * 80, "1" * 82): expect_error(bad, -1)
  for i, ch in ((0, "x"), (40, " "), (80, "a")):
    expect_error("." * i + ch + "." * (80 - i), i)

  print("Tất cả phép thử của Puzzle đều qua")

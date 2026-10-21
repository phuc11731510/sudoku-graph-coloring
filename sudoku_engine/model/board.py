from sudoku_engine.basic_types import CliqueId, Color, ColorSet, Vertex
from sudoku_engine.model.puzzle import Puzzle
from sudoku_engine.model.sudoku_graph import SudokuGraph, GRAPH
from sudoku_engine.model.color_set_ops import ColorSetOps


class Board:
  """Lớp nóng nhất của engine, giữ trạng thái thay đổi của bài toán"""
  
  graph: SudokuGraph
  colors: list[Color] # Danh sách 81 số
  # Danh sách 27 số, mỗi số biểu thị tập các số đã dùng trong một id nhóm
  usedColors: list[ColorSet]
  uncoloredCount: int

  def __init__(self):
    self.graph = GRAPH
    self.colors = [0 for _ in range(81)]
    self.usedColors = [0 for _ in range(27)]
    self.uncoloredCount = 81
    
  @staticmethod
  def fromPuzzle(puzzle: Puzzle) -> 'Board | None':
    """Tạo đối tượng Board từ một Puzzle"""
    B = Board()
    for i in range(81):
      color = puzzle.givenAt(i)
      B.colors[i] = color
      
    for color in B.colors:
      if color != 0: B.uncoloredCount -= 1
      
    for i in range(81):
      if B.colors[i] == 0: continue
      for clique_k in B.graph.cliquesOf(i):
        if ColorSetOps.contains(B.usedColors[clique_k], B.colors[i]): return None
        B.usedColors[clique_k] = ColorSetOps.add(B.usedColors[clique_k], B.colors[i])
    return B

  @staticmethod
  def empty() -> 'Board':
    """Tạo một bảng trống"""
    return Board()

  def copy(self) -> 'Board':
    """Tạo một bản sao độc lập của bảng"""
    B = Board()
    B.colors = self.colors[:]
    B.usedColors = self.usedColors[:]
    B.uncoloredCount = self.uncoloredCount
    return B

  def colorOf(self, v: Vertex) -> Color:
    """Màu hiện tại của đỉnh v"""
    return self.colors[v]

  def isColored(self, v: Vertex) -> bool:
    """Đỉnh v đã được tô chưa"""
    if self.colors[v] != 0: return True
    return False

  def colorArray(self) -> list[Color]:
    """Bản sao mảng màu của cả 81 đỉnh"""
    return self.colors[:]

  def usedColorsOf(self, k: CliqueId) -> ColorSet:
    """Tập màu đã dùng trong nhóm k"""
    return self.usedColors[k]

  def forbiddenColors(self, v: Vertex) -> ColorSet:
    """Trả về tập màu bị cấm ở v"""
    res = ColorSetOps.EMPTY_SET
    for clique in self.graph.cliquesOf(v):
      res = res | self.usedColors[clique]
    return res

  def availableColors(self, v: Vertex) -> ColorSet:
    """Tập các màu là ứng viên của một đỉnh"""
    return ColorSetOps.complement(self.forbiddenColors(v))

  def saturation(self, v: Vertex) -> int:
    """Độ bão hòa của một đỉnh (số lượng màu bị cấm của đỉnh)"""
    return ColorSetOps.size(self.forbiddenColors(v))

  def uncoloredNeighborCount(self, v: Vertex) -> int:
    """Số đỉnh kề của v chưa được tô"""
    U: tuple[Vertex,...] = self.graph.neighborsOf(v)
    count = 0
    for u in U:
      if self.colors[u] == 0: count+=1
    return count

  def canAssign(self, v: Vertex, c: Color) -> bool:
    """Có đặt được màu c vào đỉnh v hay không (c có là\
      một trong những ứng viên của đỉnh v hay không)"""
    return (self.colors[v] == 0)\
           and ColorSetOps.contains(self.availableColors(v), c)

  def assign(self, v: Vertex, c: Color) -> None:
    """Thực hiện tô đỉnh v bằng màu c"""
    if not 0<=v<=80: raise ValueError("Đỉnh phải nằm trong 0..80, nhận được " + str(v))
    if self.colors[v] != 0: raise ValueError("Đỉnh " + str(v) + " đã được tô")
    if not ColorSetOps.contains(self.availableColors(v), c): raise ValueError("Màu " + str(c) + " không thể đặt vào đỉnh " + str(v))
    
    self.colors[v] = c
    for clique in self.graph.cliquesOf(v):
      self.usedColors[clique] = ColorSetOps.add(self.usedColors[clique], c)
    self.uncoloredCount -= 1

    return None

  def unassign(self, v: Vertex) -> Color:
    """Bỏ màu của đỉnh v, trả về màu vừa bỏ"""
    if not 0<=v<=80: raise ValueError("Đỉnh phải nằm trong 0..80, nhận được " + str(v))
    if self.colors[v] == 0: raise ValueError("Đỉnh " + str(v) + " chưa được tô")

    c = self.colors[v]
    self.colors[v] = 0
    for clique in self.graph.cliquesOf(v):
      self.usedColors[clique] = ColorSetOps.remove(self.usedColors[clique], c)
    self.uncoloredCount += 1

    return c

  def isComplete(self) -> bool:
    """Mọi đỉnh đã được tô hay chưa"""
    return self.uncoloredCount == 0

  def checkInvariants(self) -> bool:
    """Kiểm tra 3 thuộc tính quan trọng của lớp này\
      có thực sự khớp thông tin với nhau một cách đúng đắn hay không"""
    expected: list[ColorSet] = [ColorSetOps.EMPTY_SET for _ in range(27)]
    uncoloredC = 0
    for v in range(81):
      c = self.colors[v]
      if not 0<=c<=9: return False
      if c == 0:
        uncoloredC += 1
        continue
      for clique in self.graph.cliquesOf(v):
        if ColorSetOps.contains(expected[clique], c): return False
        expected[clique] = ColorSetOps.add(expected[clique], c)
    if expected != self.usedColors: return False
    if uncoloredC != self.uncoloredCount: return False

    return True


if __name__ == '__main__':
  import random

  SAMPLE = ("53..7...." "6..195..." ".98....6." "8...6...3" "4..8.3..1"
            "7...2...6" ".6....28." "...419..5" "....8..79")
  SOLVED = ("534678912" "672195348" "198342567" "859761423" "426853791"
            "713924856" "961537284" "287419635" "345286179")

  def expect_error(f, *args):
    try:
      f(*args)
    except ValueError:
      return
    raise AssertionError("Không báo lỗi với: " + f.__name__ + str(args))

  def snapshot(b):
    return (list(b.colors), list(b.usedColors), b.uncoloredCount)

  # Bảng trống
  E = Board.empty()
  assert E.uncoloredCount == 81 and E.colors == [0] * 81 and E.usedColors == [0] * 27
  assert E.graph is GRAPH and Board.empty().graph is E.graph      # đồ thị dùng chung
  assert E.checkInvariants() and not E.isComplete()
  assert E.saturation(40) == 0 and E.availableColors(40) == 511
  assert E.uncoloredNeighborCount(40) == 20

  # fromPuzzle với đề mẫu (các ví dụ trên thẻ UML)
  B = Board.fromPuzzle(Puzzle.fromString(SAMPLE))
  assert B is not None and B.checkInvariants()
  assert B.uncoloredCount == 51 and (B.colorOf(0), B.colorOf(2)) == (5, 0)
  assert (B.usedColorsOf(0), B.usedColorsOf(11), B.usedColorsOf(18)) == (84, 128, 436)
  assert B.isColored(0) and not B.isColored(2)
  assert sum(B.isColored(v) for v in range(81)) == 30
  assert B.colorArray() == B.colors and B.colorArray() is not B.colors
  assert B.forbiddenColors(2) == 500 and B.availableColors(2) == 11
  assert B.saturation(2) == 6 and B.saturation(59) == 8
  assert B.uncoloredNeighborCount(59) == 11
  assert [B.canAssign(2, c) for c in range(1, 10)] == [True, True, False, True] + [False] * 5

  # fromPuzzle: đề xung đột phải trả về None (hàng, cột và khối)
  assert Board.fromPuzzle(Puzzle.fromString("55" + SAMPLE[2:])) is None
  assert Board.fromPuzzle(Puzzle.fromString("5" + "." * 8 + "5" + "." * 71)) is None
  assert Board.fromPuzzle(Puzzle.fromString("5" + "." * 9 + "5" + "." * 70)) is None
  assert Board.fromPuzzle(Puzzle.empty()).checkInvariants()

  # assign / unassign theo ví dụ trên thẻ UML
  before = snapshot(B)
  B.assign(2, 1)
  assert B.colorOf(2) == 1 and B.uncoloredCount == 50
  assert (B.usedColorsOf(0), B.usedColorsOf(11), B.usedColorsOf(18)) == (85, 129, 437)
  assert B.checkInvariants() and not B.canAssign(2, 1)
  assert B.unassign(2) == 1
  assert snapshot(B) == before and B.checkInvariants()

  # copy độc lập với bản gốc, nhưng dùng chung đồ thị
  C = B.copy()
  assert snapshot(C) == snapshot(B) and C.graph is B.graph
  C.assign(2, 1)
  assert snapshot(B) == before and C.colorOf(2) == 1 and C.checkInvariants()
  A = B.colorArray(); A[2] = 9
  assert B.colorOf(2) == 0

  # Tiền điều kiện của assign / unassign
  expect_error(B.assign, 0, 1)        # đỉnh đã tô
  expect_error(B.assign, 2, 3)        # màu bị cấm ở đỉnh 2
  expect_error(B.assign, 2, 0)        # màu ngoài 1..9
  expect_error(B.assign, 2, 10)
  expect_error(B.assign, -1, 1)       # đỉnh ngoài 0..80
  expect_error(B.assign, 81, 1)
  expect_error(B.unassign, 2)         # đỉnh chưa tô
  expect_error(B.unassign, -1)
  expect_error(B.unassign, 81)
  assert snapshot(B) == before        # các lần báo lỗi không làm đổi bảng

  # Bảng đầy: đề giải sẵn
  F = Board.fromPuzzle(Puzzle.fromString(SOLVED))
  assert F is not None and F.isComplete() and F.uncoloredCount == 0 and F.checkInvariants()
  assert all(F.availableColors(v) == 0 or F.isColored(v) for v in range(81))
  F.unassign(40)
  assert not F.isComplete() and F.availableColors(40) == ColorSetOps.bitOf(5)

  # checkInvariants phải phát hiện bảng bị làm hỏng
  def broken(change):
    b = B.copy()
    change(b)
    return b.checkInvariants()
  assert not broken(lambda b: setattr(b, 'uncoloredCount', b.uncoloredCount + 1))
  assert not broken(lambda b: b.usedColors.__setitem__(0, 0))
  assert not broken(lambda b: b.usedColors.__setitem__(0, b.usedColors[0] | 2))
  assert not broken(lambda b: b.colors.__setitem__(0, 4))
  assert not broken(lambda b: b.colors.__setitem__(1, 5))      # hai chữ số 5 cùng hàng 0
  assert not broken(lambda b: b.colors.__setitem__(2, 12))     # màu ngoài 0..9

  # Chuỗi assign / unassign ngẫu nhiên: bất biến luôn đúng, và hoàn tác về đúng trạng thái đầu
  random.seed(1)
  R = Board.fromPuzzle(Puzzle.fromString(SAMPLE))
  start = snapshot(R)
  placed = []
  for _ in range(20000):
    if placed and random.random() < 0.45:
      v = placed.pop(random.randrange(len(placed)))
      c = R.colorOf(v)
      assert R.unassign(v) == c
    else:
      v = random.randrange(81)
      if not R.isColored(v) and R.availableColors(v) != 0:
        c = random.choice(ColorSetOps.toList(R.availableColors(v)))
        assert R.canAssign(v, c)
        R.assign(v, c)
        placed.append(v)
    assert R.checkInvariants()
  while placed: R.unassign(placed.pop())
  assert snapshot(R) == start

  print("Tất cả phép thử của Board đều qua")

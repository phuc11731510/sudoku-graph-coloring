from sudoku_engine.basic_types import NO_VERTEX, Vertex
from sudoku_engine.model.board import Board
from sudoku_engine.search.vertex_selector import VertexSelector


class FirstUncoloredSelector(VertexSelector):
  """Lớp phụ trách việc chọn đỉnh chưa tô theo chỉ mục thấp nhất"""

  def select(self, board: Board, previous: Vertex) -> Vertex:
    """Trả về đỉnh chưa tô theo chỉ mục thấp nhất"""
    for v in range(max(previous, 0), 81):
      if not board.isColored(v): return v
    return NO_VERTEX

  def name(self) -> str:
    return "first-uncolored"


if __name__ == '__main__':
  from sudoku_engine.model.puzzle import Puzzle

  SAMPLE = ("53..7...." "6..195..." ".98....6." "8...6...3" "4..8.3..1"
            "7...2...6" ".6....28." "...419..5" "....8..79")
  SOLVED = ("534678912" "672195348" "198342567" "859761423" "426853791"
            "713924856" "961537284" "287419635" "345286179")

  S = FirstUncoloredSelector()

  # Tên và kiểu
  assert S.name() == "first-uncolored"
  assert isinstance(S, VertexSelector)

  # Ví dụ trên thẻ UML (đề mẫu): 2, rồi 3, rồi 5 (ô 4 là số cho sẵn)
  B = Board.fromPuzzle(Puzzle.fromString(SAMPLE))
  assert S.select(B, NO_VERTEX) == 2
  B.assign(2, 1)
  assert S.select(B, 2) == 3
  B.assign(3, 2)
  assert S.select(B, 3) == 5

  # V1: select không sửa bảng
  before = (list(B.colors), list(B.usedColors), B.uncoloredCount)
  S.select(B, 3); S.select(B, NO_VERTEX)
  assert (list(B.colors), list(B.usedColors), B.uncoloredCount) == before

  # Bảng trống: đỉnh 0; gợi ý previous không đổi kết quả khi mọi đỉnh trước nó đã tô
  E = Board.empty()
  assert S.select(E, NO_VERTEX) == 0
  E.assign(0, 1)
  assert S.select(E, 0) == 1 and S.select(E, NO_VERTEX) == 1

  # previous chưa tô vẫn đúng: trả về chính nó nếu nó là đỉnh chưa tô nhỏ nhất từ đó trở đi
  assert S.select(Board.empty(), 7) == 7

  # Quay lui: bỏ màu ở đỉnh 2 thì select lại từ gốc ra 2
  B.unassign(3); B.unassign(2)
  assert S.select(B, NO_VERTEX) == 2

  # V2: bảng đầy trả về NO_VERTEX (kể cả với previous ở cuối)
  F = Board.fromPuzzle(Puzzle.fromString(SOLVED))
  assert S.select(F, NO_VERTEX) == NO_VERTEX == -1
  assert S.select(F, 80) == NO_VERTEX
  assert S.select(F, 81) == NO_VERTEX

  # Ô cuối cùng là ô chưa tô duy nhất
  F.unassign(80)
  assert S.select(F, NO_VERTEX) == 80 and S.select(F, 79) == 80 and S.select(F, 80) == 80

  # Mô phỏng bộ giải: tô theo lời giải SOLVED, thứ tự được chọn phải đúng là 0, 1, ..., 80
  G = Board.empty()
  prev = NO_VERTEX
  order = []
  while True:
    v = S.select(G, prev)
    if v == NO_VERTEX: break
    order.append(v)
    G.assign(v, int(SOLVED[v]))
    prev = v
  assert order == list(range(81)) and G.isComplete()

  print("Tất cả phép thử của FirstUncoloredSelector đều qua")

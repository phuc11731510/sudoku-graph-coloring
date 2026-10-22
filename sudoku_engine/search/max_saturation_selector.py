from sudoku_engine.basic_types import NO_VERTEX, Vertex
from sudoku_engine.model.board import Board
from sudoku_engine.model.color_set_ops import ColorSetOps
from sudoku_engine.search.vertex_selector import TieBreak, VertexSelector


class MaxSaturationSelector(VertexSelector):
  """Bộ chọn đỉnh theo độ bão hòa"""

  tieBreak: TieBreak

  def __init__(self, tieBreak: TieBreak = TieBreak.LOWEST_INDEX) -> None:
    self.tieBreak = tieBreak

  def select(self, board: Board, previous: Vertex = NO_VERTEX) -> Vertex:
    """Thực hiện chọn đỉnh theo độ bão hòa"""
    if self.tieBreak == TieBreak.LOWEST_INDEX:
      max_sat, max_v = -1, NO_VERTEX
      for v in range(81):
        if board.isColored(v): continue
        sat = board.saturation(v)
        
        if sat >= 9: return v
        if sat > max_sat:
          max_sat = sat
          max_v = v
      
      return max_v
    
    elif self.tieBreak == TieBreak.MOST_UNCOLORED_NEIGHBORS:
      max_sat, MAX_V = -1, []
      for v in range(81):
        if board.isColored(v): continue
        sat = board.saturation(v)
        if sat > max_sat:
          max_sat = sat
          MAX_V = [v]
        elif sat == max_sat:
          MAX_V.append(v)
      
      if not MAX_V: return NO_VERTEX

      A = {}
      for v in MAX_V:
        A[v] = board.uncoloredNeighborCount(v)
        
      max_UNC = max(A.values())

      for v in MAX_V:
        if A[v] == max_UNC: return v

  def name(self) -> str:
    return "max-saturation"


if __name__ == '__main__':
  import random

  from sudoku_engine.model.puzzle import Puzzle

  SAMPLE = ("53..7...." "6..195..." ".98....6." "8...6...3" "4..8.3..1"
            "7...2...6" ".6....28." "...419..5" "....8..79")
  SOLVED = ("534678912" "672195348" "198342567" "859761423" "426853791"
            "713924856" "961537284" "287419635" "345286179")
  LOW, MOST = TieBreak.LOWEST_INDEX, TieBreak.MOST_UNCOLORED_NEIGHBORS

  def snapshot(b):
    return (list(b.colors), list(b.usedColors), b.uncoloredCount)

  # Đáp án tham chiếu viết độc lập: lấy mọi đỉnh chưa tô có độ bão hòa lớn nhất rồi áp luật hòa
  def oracle(b, tb):
    cand = [v for v in range(81) if not b.isColored(v)]
    if not cand: return NO_VERTEX
    top = max(b.saturation(v) for v in cand)
    tied = [v for v in cand if b.saturation(v) == top]
    if tb is LOW: return tied[0]
    best = max(b.uncoloredNeighborCount(v) for v in tied)
    return [v for v in tied if b.uncoloredNeighborCount(v) == best][0]

  # Tên, kiểu và luật hòa mặc định
  assert MaxSaturationSelector().name() == "max-saturation"
  assert isinstance(MaxSaturationSelector(), VertexSelector)
  assert MaxSaturationSelector().tieBreak is LOW
  assert MaxSaturationSelector(MOST).tieBreak is MOST

  L, N = MaxSaturationSelector(LOW), MaxSaturationSelector(MOST)

  # Các ví dụ trên thẻ UML (đề mẫu, lúc đầu)
  B = Board.fromPuzzle(Puzzle.fromString(SAMPLE))
  dist = {}
  for v in range(81):
    if not B.isColored(v): dist[B.saturation(v)] = dist.get(B.saturation(v), 0) + 1
  assert dist == {3: 1, 4: 2, 5: 14, 6: 17, 7: 13, 8: 4}
  assert [v for v in range(81) if not B.isColored(v) and B.saturation(v) == 8] == [40, 59, 62, 70]
  assert [B.uncoloredNeighborCount(v) for v in (40, 59, 62, 70)] == [10, 11, 11, 11]
  assert L.select(B, NO_VERTEX) == 40 and B.availableColors(40) == ColorSetOps.bitOf(5)
  assert N.select(B, NO_VERTEX) == 59       # 59, 62, 70 cùng có 11, lấy chỉ số nhỏ nhất
  assert L.select(B) == 40 and N.select(B) == 59   # previous có giá trị mặc định
  assert L.select(B, 40) == 40 and N.select(B, 59) == 59   # previous bị bỏ qua

  # V1: select không sửa bảng
  before = snapshot(B)
  L.select(B, NO_VERTEX); N.select(B, NO_VERTEX)
  assert snapshot(B) == before

  # Bảng trống: mọi đỉnh hòa nhau, cả hai luật lấy đỉnh 0; bảng đầy: NO_VERTEX
  assert L.select(Board.empty()) == 0 and N.select(Board.empty()) == 0
  F = Board.fromPuzzle(Puzzle.fromString(SOLVED))
  assert L.select(F) == NO_VERTEX == -1 and N.select(F) == NO_VERTEX
  F.unassign(37)
  assert L.select(F) == 37 and N.select(F) == 37    # đỉnh chưa tô duy nhất

  # Ngõ cụt: đỉnh hết màu (độ bão hòa 9) phải được chọn, dù ở đầu hay ở cuối chỉ số
  def deadEndBoard(mirror):
    b = Board.empty()
    for v, c in ((1, 1), (2, 2), (3, 3), (4, 4), (9, 5), (18, 6), (27, 7), (36, 8), (10, 9)):
      b.assign(80 - v if mirror else v, c)
    return b
  for mirror in (False, True):
    D = deadEndBoard(mirror)
    for sel in (L, N):
      v = sel.select(D)
      assert D.saturation(v) == 9 and D.availableColors(v) == 0
    assert L.select(D) == (80 if mirror else 0)   # chỉ có một đỉnh hết màu
  # M1 và luật hòa: đối chiếu với đáp án tham chiếu trên các trạng thái ngẫu nhiên
  random.seed(1)
  R = Board.fromPuzzle(Puzzle.fromString(SAMPLE))
  placed = []
  decoys = 0     # số trạng thái có đỉnh độ bão hòa 8 đứng trước một đỉnh độ bão hòa 9
  for _ in range(400):
    if placed and random.random() < 0.3:
      R.unassign(placed.pop(random.randrange(len(placed))))
    else:
      v = random.randrange(81)
      if not R.isColored(v) and R.availableColors(v) != 0:
        R.assign(v, random.choice(ColorSetOps.toList(R.availableColors(v))))
        placed.append(v)
    state = snapshot(R)
    nines = [u for u in range(81) if not R.isColored(u) and R.saturation(u) == 9]
    if nines and any(R.saturation(u) == 8 for u in range(nines[0]) if not R.isColored(u)): decoys += 1
    for sel, tb in ((L, LOW), (N, MOST)):
      v = sel.select(R, NO_VERTEX)
      assert v == oracle(R, tb)
      if v != NO_VERTEX:
        assert not R.isColored(v)
        assert all(R.saturation(v) >= R.saturation(u) for u in range(81) if not R.isColored(u))
    assert snapshot(R) == state
  assert decoys > 0     # vòng ngẫu nhiên có chạm trường hợp mà dừng sớm ở 8 sẽ chọn sai

  # Mô phỏng bộ giải tham lam trên đề mẫu: tô màu nhỏ nhất còn dùng được, 51 nút, bước đầu đúng
  firstSteps = {}
  for sel, tb in ((L, LOW), (N, MOST)):
    G = Board.fromPuzzle(Puzzle.fromString(SAMPLE))
    prev, nodes = NO_VERTEX, 0
    while True:
      v = sel.select(G, prev)
      if v == NO_VERTEX: break
      assert G.availableColors(v) != 0
      c = ColorSetOps.lowest(G.availableColors(v))
      firstSteps.setdefault(tb, (v, c))
      G.assign(v, c)
      prev, nodes = v, nodes + 1
    assert nodes == 51 and G.isComplete() and G.checkInvariants()
  assert firstSteps[LOW] == (40, 5)     # thẻ UML: bước đầu của DSATUR là ASSIGN ô 40 màu 5
  assert firstSteps[MOST] == (59, 7)

  print("Tất cả phép thử của MaxSaturationSelector đều qua")

from sudoku_engine.basic_types import CliqueId, Edge, Vertex


class SudokuGraph:
  """Cấu trúc đồ thị của bàn Sudoku, mọi bàn đều giống nhau"""
  VERTEX_COUNT: int = 81
  EDGE_COUNT: int = 810

  # Lưu trữ thông tin xem một đỉnh liệu nó nằm trong 3 id Clique nào
  cliqueOf: tuple[tuple[CliqueId, ...], ...]
  # Lưu trữ thông tin xem có các đỉnh nào thuộc một id Clique cụ thể
  cliqueVertices: tuple[tuple[Vertex, ...], ...]
  # Lưu trữ thông tin xem tại một đỉnh thì có những đỉnh nào kề với nó
  neighbors: tuple[tuple[Vertex, ...], ...]
  # Lưu trữ 810 cạnh trong đồ thị
  edges: tuple[Edge, ...]

  def __init__(self):
    A = [(i, j) for i in range(9) for j in range(9)]
    B = {(i, j) : 9*i + j for i, j in A}
    self.cliqueOf = tuple((a, 9 + b, 18 + (a//3)*3 + b//3) for a, b in A)
  
    self.cliqueVertices = []
    for i in range(9):
      self.cliqueVertices.append(tuple(j for j in range(9*i, 9*i+9)))
    for i in range(9):
      self.cliqueVertices.append(tuple(j for j in range(i, i+9*8+1, 9)))
    for i in range(9):
      r0, c0 = 3 * (i // 3), 3 * (i % 3)
      self.cliqueVertices.append(tuple(B[(r, c)] for r in range(r0, r0 + 3) for c in range(c0, c0 + 3)))
    self.cliqueVertices = tuple(self.cliqueVertices)
    
    self.neighbors = []
    for v in range(0, 81):
      clique1, clique2, clique3 = self.cliqueOf[v]
      self.neighbors.append(tuple(sorted(\
            (set(self.cliqueVertices[clique1])\
             | set(self.cliqueVertices[clique2]) \
             | set(self.cliqueVertices[clique3])) - {v} \
            )))
    self.neighbors = tuple(self.neighbors)
    
    self.edges = tuple((u, v) for u in range(81) for v in self.neighbors[u] if v > u)

  def rowOf(self, v: Vertex) -> int:
    """Hàng của một đỉnh là mấy"""
    if not 0<=v<=80: raise ValueError("Đỉnh phải nằm trong 0..80, nhận được " + str(v))
    return v//9

  def colOf(self, v: Vertex) -> int:
    """Cột của một đỉnh là mấy"""
    if not 0<=v<=80: raise ValueError("Đỉnh phải nằm trong 0..80, nhận được " + str(v))
    return v%9

  def boxOf(self, v: Vertex) -> int:
    """Đỉnh này thuộc ô 3x3 thứ mấy"""
    return 3*(self.rowOf(v)//3) + self.colOf(v)//3

  def cliquesOf(self, v: Vertex) -> tuple[CliqueId, ...]:
    """Đỉnh này nằm trong 3 Clique nào"""
    return self.cliqueOf[v]

  def neighborsOf(self, v: Vertex) -> tuple[Vertex, ...]:
    """Đỉnh này có những đỉnh nào kề với nó"""
    return self.neighbors[v]

  def areAdjacent(self, u: Vertex, v: Vertex) -> bool:
    """Đỉnh u có kề với đỉnh v hay không"""
    if not 0<=u<=80: raise ValueError("Đỉnh phải nằm trong 0..80, nhận được " + str(u))
    if not 0<=v<=80: raise ValueError("Đỉnh phải nằm trong 0..80, nhận được " + str(v))
    return v in self.neighborsOf(u)

  def degreeOf(self, v: Vertex) -> int:
    """Bậc của một đỉnh (luôn là 20)"""
    return 20


GRAPH = SudokuGraph()


if __name__ == '__main__':
  G = GRAPH

  def expect_error(f, *args):
    try:
      f(*args)
    except ValueError:
      return
    raise AssertionError("Không báo lỗi với: " + f.__name__ + str(args))

  # G1: 81 đỉnh, 27 nhóm, mỗi nhóm 9 đỉnh, mỗi đỉnh nằm trong đúng 3 nhóm
  assert len(G.cliqueOf) == 81 and len(G.cliqueVertices) == 27 and len(G.neighbors) == 81
  assert all(len(t) == 9 and list(t) == sorted(t) for t in G.cliqueVertices)
  assert all(len(t) == 3 and list(t) == sorted(t) for t in G.cliqueOf)
  assert all(v in G.cliqueVertices[k] for v in range(81) for k in G.cliqueOf[v])
  assert all(sum(v in t for t in G.cliqueVertices) == 3 for v in range(81))

  # G2: mỗi đỉnh có đúng 20 đỉnh kề, khác nhau, khác chính nó, tăng dần
  assert all(len(t) == 20 and list(t) == sorted(set(t)) for t in G.neighbors)
  assert all(v not in G.neighbors[v] for v in range(81))

  # G3: kề nhau là quan hệ đối xứng
  assert all((u in G.neighbors[v]) == (v in G.neighbors[u]) for u in range(81) for v in range(81))

  # G4: đúng 810 cạnh, u < v, mỗi cạnh một lần, mỗi cạnh là một cặp kề
  assert len(G.edges) == G.EDGE_COUNT == 810 and G.VERTEX_COUNT == 81
  assert all(u < v for u, v in G.edges) and len(set(G.edges)) == 810
  assert all(v in G.neighbors[u] for u, v in G.edges)
  assert G.edges[0] == (0, 1) and G.edges[-1] == (79, 80)

  # Các ví dụ trên thẻ UML
  assert G.cliqueOf[40] == (4, 13, 22) and G.cliqueOf[2] == (0, 11, 18)
  assert G.cliqueVertices[0] == (0, 1, 2, 3, 4, 5, 6, 7, 8)
  assert G.cliqueVertices[18] == (0, 1, 2, 9, 10, 11, 18, 19, 20)
  assert G.neighbors[0] == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72)

  # Các phương thức
  assert (G.rowOf(40), G.colOf(40), G.boxOf(40)) == (4, 4, 4)
  assert (G.colOf(2), G.boxOf(10)) == (2, 0)
  assert all(G.rowOf(v) * 9 + G.colOf(v) == v for v in range(81))
  assert all(G.cliquesOf(v) == (G.rowOf(v), 9 + G.colOf(v), 18 + G.boxOf(v)) for v in range(81))
  assert all(G.neighborsOf(v) is G.neighbors[v] for v in range(81))
  assert G.areAdjacent(0, 10) and not G.areAdjacent(0, 29) and not G.areAdjacent(5, 5)
  assert sum(G.areAdjacent(u, v) for u in range(81) for v in range(81)) == 81 * 20
  assert all(G.degreeOf(v) == 20 for v in range(81))

  # Đỉnh ngoài 0..80 phải báo lỗi
  for bad in (-1, 81):
    expect_error(G.rowOf, bad)
    expect_error(G.colOf, bad)
    expect_error(G.boxOf, bad)
    expect_error(G.areAdjacent, bad, 0)
    expect_error(G.areAdjacent, 0, bad)

  print("Tất cả phép thử của SudokuGraph đều qua")

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
  pass

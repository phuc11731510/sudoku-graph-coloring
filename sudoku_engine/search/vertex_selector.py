from abc import ABC, abstractmethod
from enum import Enum

from sudoku_engine.basic_types import NO_VERTEX, Vertex
from sudoku_engine.model.board import Board


class VertexSelector(ABC):
  """Giao diện của bộ thuật toán chọn đỉnh chưa tô"""
  @abstractmethod
  def select(self, board: Board, previous: Vertex) -> Vertex:
    """Phương thức chọn đỉnh tùy theo cách giải sudoku"""

  @abstractmethod
  def name(self) -> str:
    """Tên của phương pháp chọn đỉnh"""


class TieBreak(Enum):
  """Cách chọn đỉnh DSATUR khi nhiều đỉnh cùng độ bão hòa lớn nhất"""

  LOWEST_INDEX = 0
  MOST_UNCOLORED_NEIGHBORS = 1


if __name__ == '__main__':
  def expect_error(f, *args):
    try:
      f(*args)
    except TypeError:
      return
    raise AssertionError("Không báo lỗi với: " + f.__name__ + str(args))

  # TieBreak: đúng hai giá trị, khác nhau, tra theo tên được
  assert [t.name for t in TieBreak] == ['LOWEST_INDEX', 'MOST_UNCOLORED_NEIGHBORS']
  assert TieBreak.LOWEST_INDEX is not TieBreak.MOST_UNCOLORED_NEIGHBORS
  assert TieBreak['LOWEST_INDEX'] is TieBreak.LOWEST_INDEX

  # VertexSelector là lớp trừu tượng: không tạo trực tiếp được
  expect_error(VertexSelector)

  # Lớp con thiếu một phương thức trừu tượng cũng không tạo được
  class OnlyName(VertexSelector):
    def name(self) -> str:
      return "only-name"
  expect_error(OnlyName)

  # Lớp con có đủ hai phương thức thì tạo được
  class Dummy(VertexSelector):
    def select(self, board: Board, previous: Vertex) -> Vertex:
      return NO_VERTEX
    def name(self) -> str:
      return "dummy"
  d = Dummy()
  assert isinstance(d, VertexSelector) and d.name() == "dummy"
  assert d.select(Board.empty(), NO_VERTEX) == NO_VERTEX == -1

  print("Tất cả phép thử của VertexSelector và TieBreak đều qua")

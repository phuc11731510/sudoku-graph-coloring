from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class SolveLimits:
  """Đối tượng biểu diễn tham số điều khiển của một lần giải\n
    Chỉ có giới số lượng node tối đa và giới hạn số lượng solution"""
  maxNodes: int = 0
  solutionLimit: int = 1

  @staticmethod
  def defaults() -> 'SolveLimits':
    return SolveLimits()


class SolveStatus(Enum):
  """Đối tượng biểu diễn các cách mà một lần giải có thể kết thúc"""
  SOLVED = 0
  UNSOLVABLE = 1
  STUCK = 2
  LIMIT_REACHED = 3
  INVALID_PUZZLE = 4


@dataclass(slots=True)
class SearchStats:
  """Đối tượng chứa các con số đếm để so sánh thuật toán
  `nodes` là số lần `assign` do bộ giải thực hiện
  `backtracks` là số lần `unassign` do bộ giải thực hiện
  `choicePoints` biểu thị số lần chọn đỉnh mà đỉnh đó có từ hai màu khả thi trở lên (tức là đoán)
  `forcedMoves` biểu thị số lần chọn đỉnh mà đỉnh đó chỉ có một màu duy nhất khả thi (tức là bắt buộc)
  `deadEnds` là số lần chọn đỉnh nhưng không may đỉnh đó không có màu nào
  `maxDepth` là độ sâu lớn nhất của quá trình đệ quy tìm kiếm
  """
  nodes: int = 0
  backtracks: int = 0
  choicePoints: int = 0
  forcedMoves: int = 0
  deadEnds: int = 0
  maxDepth: int = 0

  def selections(self) -> int:
    """Trả về tổng số lần chọn đỉnh của bộ giải"""
    return self.choicePoints + self.forcedMoves + self.deadEnds

  def add(self, other: 'SearchStats') -> None:
    """Cộng dồn thống kê của các lần chạy khác, lấy maxDepth là lớn nhất của một trong hai lần chạy"""
    self.maxDepth = max(self.maxDepth, other.maxDepth)
    self.nodes += other.nodes
    self.backtracks += other.backtracks
    self.choicePoints += other.choicePoints
    self.forcedMoves += other.forcedMoves
    self.deadEnds += other.deadEnds
    
  def reset(self) -> None:
    """Đặt tất cả bộ đếm về 0"""
    self.nodes = 0
    self.backtracks = 0
    self.choicePoints = 0
    self.forcedMoves = 0
    self.deadEnds = 0
    self.maxDepth = 0
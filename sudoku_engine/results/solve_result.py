from dataclasses import dataclass
from enum import Enum, auto

@dataclass(frozen=True, slots=True)
class SolveLimits:
    maxNodes: int = 0
    solutionLimit: int = 1

    def __post_init__(self):
        
        if self.maxNodes < 0:
            raise ValueError("Vi phạm L1: maxNodes phải >= 0 (0 là không giới hạn).")
        if self.solutionLimit < 1:
            raise ValueError("Vi phạm L2: solutionLimit phải >= 1.")

    @staticmethod
    def defaults() -> "SolveLimits":
        """Trả về cấu hình giới hạn mặc định: maxNodes = 0, solutionLimit = 1."""
        return SolveLimits(maxNodes=0, solutionLimit=1)

class SolveStatus(Enum):
    """trạng thái của quá trình giải sudoku"""
    SOLVED = auto()          # thành công.
    UNSOLVABLE = auto()     # Skhông có lời giải.
    IN_PROGRESS = auto()     # đang giải
    NODE_LIMIT_REACHED = auto()  # đã đạt giới hạn số nút tối đa.
    SOLUTION_LIMIT_REACHED = auto()  # đã đạt giới hạn số lời giải.



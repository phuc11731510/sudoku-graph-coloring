

class Puzzle:
  def __init__(self):
    self.givens=tuple(0 for _ in range(81))
    
  def fromString(text: str) -> 'Puzzle':
    return None
  
  @staticmethod
  def empty() -> 'Puzzle':
    return Puzzle()
  
  def isGiven(self, v: int) -> bool:
    if self.givens[v] == 0:return False
    return True
  
if __name__=='__main__':
  A=Puzzle.empty()
  print(A.givens)
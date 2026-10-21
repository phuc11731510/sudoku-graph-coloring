from sudoku_engine.basic_types import Color, ColorSet


class ColorSetOps:
  EMPTY_SET: ColorSet = 0
  FULL_SET: ColorSet = 511

  @staticmethod
  def bitOf(c: Color) -> ColorSet:
    """Trả về ColorSet đại diện cho tập chỉ có một màu c"""
    if not 1<=c<=9: raise ValueError("Màu phải nằm trong 1..9, nhận được " + str(c))
    return 1 << (c-1)

  @staticmethod
  def contains(s: ColorSet, c: Color) -> bool:
    """Kiểm tra xem màu c có nằm trong tập s hay không"""
    if not 1<=c<=9: raise ValueError("Màu phải nằm trong 1..9, nhận được " + str(c))
    return ((s >> (c-1)) & 1) != 0
  
  @staticmethod
  def add(s: ColorSet, c: Color) -> ColorSet:
    """Thêm màu c vào tập s"""
    if not 1<=c<=9: raise ValueError("Màu phải nằm trong 1..9, nhận được " + str(c))
    return s | (1 << (c-1))

  @staticmethod
  def remove(s: ColorSet, c: Color) -> ColorSet:
    """Bỏ màu c khỏi tập s"""
    if not 1<=c<=9: raise ValueError("Màu phải nằm trong 1..9, nhận được " + str(c))
    return s & (~(1 << (c-1)))

  @staticmethod
  def size(s: ColorSet) -> int:
    """Đếm số màu trong tập"""
    return s.bit_count()

  @staticmethod
  def complement(s: ColorSet) -> ColorSet:
    """Trả về tập các bit là phần bù của s"""
    return ColorSetOps.FULL_SET ^ s

  @staticmethod
  def isSingle(s: ColorSet) -> bool:
    """Liệu s có đại diện cho tập chỉ có 1 màu hay không"""
    return s!=0 and ( (s & (s-1)) == 0)

  @staticmethod
  def lowest(s: ColorSet) -> Color:
    """Màu nhỏ nhất của s là gì"""
    if s == 0: raise ValueError("Tập rỗng không có màu nhỏ nhất")
    return (s & (-s)).bit_length()

  @staticmethod
  def toList(s: ColorSet) -> list[Color]:
    """Liệt kê các màu theo thứ tự tăng dần trong s"""
    res: list[Color] = []
    offset = 0
    while s != 0:
      a = (s & (-s)).bit_length()
      res.append(offset + a)
      s = s >> a
      offset += a
    return res

if __name__ == '__main__':
  C = ColorSetOps

  def expect_error(f, *args):
    try:
      f(*args)
    except ValueError:
      return
    raise AssertionError("Không báo lỗi với: " + f.__name__ + str(args))

  def expected_colors(s):
    return [c for c in range(1, 10) if (s >> (c - 1)) & 1]

  # Hằng số
  assert C.EMPTY_SET == 0 and C.FULL_SET == 511 == 0b111111111

  # Các ví dụ trên thẻ UML
  assert C.bitOf(5) == 16
  assert C.contains(11, 4) and not C.contains(11, 3)
  assert C.add(84, 1) == 85 and C.remove(85, 1) == 84
  assert C.size(500) == 6 and C.complement(500) == 11
  assert C.isSingle(16) and not C.isSingle(11) and not C.isSingle(0)
  assert C.lowest(11) == 1 and C.lowest(8) == 4
  assert C.toList(11) == [1, 2, 4]

  # bitOf: chín màu ứng với chín bit riêng, hợp lại thành FULL_SET
  assert [C.bitOf(c) for c in range(1, 10)] == [1, 2, 4, 8, 16, 32, 64, 128, 256]
  assert sum(C.bitOf(c) for c in range(1, 10)) == C.FULL_SET

  # Kiểm tra trên mọi tập con của chín màu (512 tập)
  for s in range(512):
    colors = expected_colors(s)
    assert C.toList(s) == colors
    assert C.size(s) == len(colors)
    assert C.complement(s) == C.FULL_SET & ~s and C.size(s) + C.size(C.complement(s)) == 9
    assert C.isSingle(s) == (len(colors) == 1)
    if s != 0: assert C.lowest(s) == colors[0]
    for c in range(1, 10):
      assert C.contains(s, c) == (c in colors)
      assert C.contains(C.add(s, c), c) and not C.contains(C.remove(s, c), c)
      assert C.add(C.add(s, c), c) == C.add(s, c)        # thêm màu đã có thì không đổi
      assert C.remove(C.remove(s, c), c) == C.remove(s, c)  # bỏ màu không có thì không đổi
      assert C.add(s, c) <= C.FULL_SET and C.remove(s, c) >= 0  # giữ trong 0..511 (C1)

  # Tập rỗng không có màu nhỏ nhất
  expect_error(C.lowest, 0)

  # Màu ngoài 1..9 phải báo lỗi
  for bad in (0, 10, -1):
    expect_error(C.bitOf, bad)
    expect_error(C.contains, 11, bad)
    expect_error(C.add, 11, bad)
    expect_error(C.remove, 11, bad)

  print("Tất cả phép thử của ColorSetOps đều qua")

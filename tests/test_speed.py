import numpy as np
from botris.core import CBoard
from timeit import default_timer as timer

cb: CBoard = CBoard()
for i in range(cb.height):
    cb.set(i, i)

npb = np.array(cb.board)
_ = cb.numpy_view()

# test speed of CBoard.board
start = timer()
for _ in range(10000000):
    _ = cb.board
    npb = np.array(cb.board)
end = timer()
print(f"Time for CBoard.board: {end-start}")
# 12.234543800004758 s

# test speed of CBoard.numpy_view()
start = timer()
for _ in range(10000000):
    _ = cb.numpy_view()
end = timer()
print(f"Time for CBoard.numpy_view(): {end-start}")
# 13.667099500074983 s
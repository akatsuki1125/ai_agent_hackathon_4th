import sys
import tty
import termios

fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)

try:
    tty.setcbreak(fd)
    while True:
        ch = sys.stdin.read(1)
        if ch == "q":
            break
        print(f"got: {ch!r}")
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old)
import sys, tty, termios
import requests

fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)

try:
    tty.setcbreak(fd)
    while True:
        ch = sys.stdin.read(1)
        print(ch)
        requests.post("http://127.0.0.1:8000/send", ch)
        if ch=="q":
            break

finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old)
# termios/tty メモ

## 1文字ずつ読むコードの意味
このコードは「Enter を押さずに、1文字入力のたびに読み取る」ための設定と後片付けです。

```py
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
```

### ざっくり流れ
- `sys.stdin.fileno()` で端末のファイル番号を取得。
- `termios.tcgetattr` で現在の端末設定を保存。
- `tty.setcbreak` で **1文字入力で即読み取り**できるモードに切り替え。
- `sys.stdin.read(1)` で1文字ずつ読む。
- `finally` で端末設定を元に戻す（戻さないと端末が変な状態になる）。

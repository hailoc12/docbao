import sys

from easyprocess import EasyProcess

python = sys.executable
cmd = [
    python,
    "-c",
    'print("hello")',
]
s = EasyProcess(cmd).call().stdout
print(s)

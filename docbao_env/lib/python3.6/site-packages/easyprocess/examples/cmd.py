import sys

from easyprocess import EasyProcess

python = sys.executable

print("-- Run program, wait for it to complete, get stdout:")
s = EasyProcess([python, "-c", "print(3)"]).call().stdout
print(s)

print("-- Run program, wait for it to complete, get stderr:")
s = EasyProcess([python, "-c", "import sys;sys.stderr.write('4\\n')"]).call().stderr
print(s)

print("-- Run program, wait for it to complete, get return code:")
s = EasyProcess([python, "--version"]).call().return_code
print(s)

print("-- Run program, wait 1 second, stop it, get stdout:")
s = EasyProcess(["ping", "localhost"]).start().sleep(1).stop().stdout
print(s)

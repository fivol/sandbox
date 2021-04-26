from ctypes import cdll
lib = cdll.LoadLibrary("./library.so")
lib.print_hello()

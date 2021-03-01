import ctypes
load = ctypes.cdll.LoadLibrary("./frozenfrog.dll")
SetSignals = load.SetSignals
SetSignals.argtypes = [ctypes.c_int, ctypes.c_int,]
GetSignals = load.GetSignals
GetSignals.argtypes = [ctypes.c_int, ]

SetValues = load.SetValues
SetValues.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double,]
GetValues = load.GetValues
GetValues.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,]
GetValues.restype = ctypes.c_double

SetValues(0,0,0,0,0,-200.00)
print(GetValues(0,0,0,0,0))

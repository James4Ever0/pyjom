from pymem import *
from win32con import *
from win32event import *
from win32process import *
import ctypes

# pip install pywin32
# pip install pymem

dll = ctypes.WinDLL('kernel32.dll')


class Asm(Pymem):
    def __init__(self, process_name=None):
        super().__init__(process_name)
        self.ba = b''
        print("By 风雨无阻")

    def CallRemote(self, code):
        if code == "":
            return False

        alloc = VirtualAllocEx(self.process_handle, 0, len(code), MEM_COMMIT, PAGE_EXECUTE_READWRITE)

        if self.write_bytes(alloc, code, len(code)):
            VirtualFreeEx(self.process_handle, alloc, 0, MEM_RELEASE)
            return False
        hThread = dll.CreateRemoteThread(self.process_handle, 0, 0, alloc, NULL, CREATE_SUSPENDED, NULL)

        if hThread == 0:
            VirtualFreeEx(self.process_handle, alloc, 0, MEM_RELEASE)
            return False

        ResumeThread(hThread)
        WaitForSingleObject(hThread, INFINITE)
        VirtualFreeEx(self.process_handle, alloc, 0, MEM_RELEASE)
        # 每次调用完call后清空 ba
        self.ba = b''
        return True

    @staticmethod
    def ToBytes(ba):
        tmp = str(ba)
        return bytes(bytearray.fromhex(tmp))

    @staticmethod
    def intToBytes(v, n):
        tmp = ""
        tmp2 = "0000000" + hex(v & 0xFFFFFFFF)[2:]
        tmp2 = tmp2[len(tmp2) - n: len(tmp2)]

        for i in range(0, int(len(tmp2) / 2)):
            tmp = tmp + tmp2[len(tmp2) - 2 * (i + 1): len(tmp2) - 2 * i]

        return bytes(bytearray.fromhex(tmp))

    def getCode(self):
        return self.ba

    def push(self, v):
        if 127 >= v >= -128:
            self.ba += self.ToBytes("6A") + self.intToBytes(v, 2)
        else:
            self.ba += self.ToBytes("68") + self.intToBytes(v, 8)

    def pushad(self):
        self.ba += self.ToBytes("60")

    def popad(self):
        self.ba += self.ToBytes("61")

    def call_eax(self):
        self.ba += self.ToBytes("FF D0")

    def mov_eax(self, v):
        self.ba += self.ToBytes("B8") + self.intToBytes(v, 8)

    def mov_ebx(self, v):
        self.ba += self.ToBytes("BB") + self.intToBytes(v, 8)

    def mov_ecx(self, v):
        self.ba += self.ToBytes("B9") + self.intToBytes(v, 8)

    def mov_edx(self, v):
        self.ba += self.ToBytes("BA") + self.intToBytes(v, 8)

    def mov_edi(self, v):
        self.ba += self.ToBytes("BF") + self.intToBytes(v, 8)

    def ret(self):
        self.ba += self.ToBytes("C3")

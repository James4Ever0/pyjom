
#define _CRT_SECURE_NO_WARNINGS
#define _CRT_NON_CONFORMING_SWPRINTFS
#define WIN32_LEAN_AND_MEAN
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// 头文件
#include <Windows.h>
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//导出函数
#pragma comment(linker, "/EXPORT:GetFileVersionInfoA=_AheadLib_GetFileVersionInfoA,@1")
#pragma comment(linker, "/EXPORT:GetFileVersionInfoByHandle=_AheadLib_GetFileVersionInfoByHandle,@2")
//--#pragma comment(linker, "/EXPORT:GetFileVersionInfoExA=_AheadLib_GetFileVersionInfoExA,@3")
#pragma comment(linker, "/EXPORT:GetFileVersionInfoExW=_AheadLib_GetFileVersionInfoExW,@4")
#pragma comment(linker, "/EXPORT:GetFileVersionInfoSizeA=_AheadLib_GetFileVersionInfoSizeA,@5")
//--#pragma comment(linker, "/EXPORT:GetFileVersionInfoSizeExA=_AheadLib_GetFileVersionInfoSizeExA,@6")
#pragma comment(linker, "/EXPORT:GetFileVersionInfoSizeExW=_AheadLib_GetFileVersionInfoSizeExW,@7")
#pragma comment(linker, "/EXPORT:GetFileVersionInfoSizeW=_AheadLib_GetFileVersionInfoSizeW,@8")
#pragma comment(linker, "/EXPORT:GetFileVersionInfoW=_AheadLib_GetFileVersionInfoW,@9")
#pragma comment(linker, "/EXPORT:VerFindFileA=_AheadLib_VerFindFileA,@10")
#pragma comment(linker, "/EXPORT:VerFindFileW=_AheadLib_VerFindFileW,@11")
#pragma comment(linker, "/EXPORT:VerInstallFileA=_AheadLib_VerInstallFileA,@12")
#pragma comment(linker, "/EXPORT:VerInstallFileW=_AheadLib_VerInstallFileW,@13")
#pragma comment(linker, "/EXPORT:VerLanguageNameA=_AheadLib_VerLanguageNameA,@14")
#pragma comment(linker, "/EXPORT:VerLanguageNameW=_AheadLib_VerLanguageNameW,@15")
#pragma comment(linker, "/EXPORT:VerQueryValueA=_AheadLib_VerQueryValueA,@16")
#pragma comment(linker, "/EXPORT:VerQueryValueW=_AheadLib_VerQueryValueW,@17")


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 原函数地址指针
PVOID pfnGetFileVersionInfoA;
PVOID pfnGetFileVersionInfoByHandle;
//PVOID pfnGetFileVersionInfoExA;
PVOID pfnGetFileVersionInfoExW;
PVOID pfnGetFileVersionInfoSizeA;
PVOID pfnGetFileVersionInfoSizeExA;
PVOID pfnGetFileVersionInfoSizeExW;
PVOID pfnGetFileVersionInfoSizeW;
PVOID pfnGetFileVersionInfoW;
PVOID pfnVerFindFileA;
PVOID pfnVerFindFileW;
PVOID pfnVerInstallFileA;
PVOID pfnVerInstallFileW;
PVOID pfnVerLanguageNameA;
PVOID pfnVerLanguageNameW;
PVOID pfnVerQueryValueA;
PVOID pfnVerQueryValueW;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 宏定义
#define EXTERNC extern "C"
#define NAKED __declspec(naked)
#define EXPORT __declspec(dllexport)

#define ALCPP EXPORT NAKED
#define ALSTD EXTERNC EXPORT NAKED void __stdcall
#define ALCFAST EXTERNC EXPORT NAKED void __fastcall
#define ALCDECL EXTERNC NAKED void __cdecl
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 
// 
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// AheadLib 命名空间
namespace AheadLib
{
HMODULE m_hModule = NULL;	// 原始模块句柄
DWORD m_dwReturn[17] = { 0 };	// 原始函数返回地址


// 获取原始函数地址
FARPROC WINAPI GetAddress(PCSTR pszProcName)
{
	FARPROC fpAddress;
	CHAR szProcName[16];
	TCHAR tzTemp[MAX_PATH];

	fpAddress = GetProcAddress(m_hModule, pszProcName);
	if (fpAddress == NULL)
	{
		if (HIWORD(pszProcName) == 0)
		{
			wsprintfA(szProcName, "%d", pszProcName);
			pszProcName = szProcName;
		}

		wsprintf(tzTemp, TEXT("无法找到函数 %hs，程序无法正常运行。"), pszProcName);
		MessageBox(NULL, tzTemp, TEXT("AheadLib"), MB_ICONSTOP);
		ExitProcess(-2);
	}

	return fpAddress;
}

// 初始化原始函数地址指针
inline VOID WINAPI InitializeAddresses()
{
	pfnGetFileVersionInfoA = GetAddress("GetFileVersionInfoA");
	pfnGetFileVersionInfoByHandle = GetAddress("GetFileVersionInfoByHandle");
	//pfnGetFileVersionInfoExA = GetAddress("GetFileVersionInfoExA");
	pfnGetFileVersionInfoExW = GetAddress("GetFileVersionInfoExW");
	pfnGetFileVersionInfoSizeA = GetAddress("GetFileVersionInfoSizeA");
	//pfnGetFileVersionInfoSizeExA = GetAddress("GetFileVersionInfoSizeExA");
	pfnGetFileVersionInfoSizeExW = GetAddress("GetFileVersionInfoSizeExW");
	pfnGetFileVersionInfoSizeW = GetAddress("GetFileVersionInfoSizeW");
	pfnGetFileVersionInfoW = GetAddress("GetFileVersionInfoW");
	pfnVerFindFileA = GetAddress("VerFindFileA");
	pfnVerFindFileW = GetAddress("VerFindFileW");
	pfnVerInstallFileA = GetAddress("VerInstallFileA");
	pfnVerInstallFileW = GetAddress("VerInstallFileW");
	pfnVerLanguageNameA = GetAddress("VerLanguageNameA");
	pfnVerLanguageNameW = GetAddress("VerLanguageNameW");
	pfnVerQueryValueA = GetAddress("VerQueryValueA");
	pfnVerQueryValueW = GetAddress("VerQueryValueW");
}

// 加载原始模块
inline BOOL WINAPI Load()
{
	SYSTEM_INFO si;
	GetNativeSystemInfo(&si);
	auto is64os = (si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64 || si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_IA64);
	wchar_t sys64_32_path[MAX_PATH] = L"c:\\Windows\\SysWOW64\\version.dll";
	wchar_t sys32_32_path[MAX_PATH] = L"c:\\Windows\\system32\\version.dll";
	wchar_t buf[MAX_PATH] = {};
	GetSystemDirectory(buf, 256);
	sys64_32_path[0] = buf[0];
	sys32_32_path[0] = buf[0];
	if (is64os) {
		m_hModule = LoadLibrary(sys64_32_path);
	}
	else {
		m_hModule = LoadLibrary(sys32_32_path);
	}
	if (!m_hModule) {
		MessageBox(0, 0, 0, 0);
	}
	if (m_hModule) {
		InitializeAddresses();
	}
	return (m_hModule != NULL);
}

// 释放原始模块
inline VOID WINAPI Free()
{
	if (m_hModule)
	{
		FreeLibrary(m_hModule);
	}
}
}
using namespace AheadLib;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*包含头文件*/
void Thread(HMODULE hModule)
{
	/*判断是否是目标检测*/
	/*..业务代码*/

}
BOOL WINAPI DllMain(HMODULE hModule, DWORD dwReason, PVOID pvReserved)
{
	if (dwReason == DLL_PROCESS_ATTACH) {
		DisableThreadLibraryCalls(hModule);
		Load();
		CreateThread(0, 0, (LPTHREAD_START_ROUTINE)Thread, hModule, 0, 0);

	}
	else if (dwReason == DLL_PROCESS_DETACH) {
		Free();
	}

	return TRUE;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


ALCDECL AheadLib_GetFileVersionInfoA(void)
{
	__asm JMP pfnGetFileVersionInfoA;
}


ALCDECL AheadLib_GetFileVersionInfoByHandle(void)
{
	__asm JMP pfnGetFileVersionInfoByHandle;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 导出函数
//ALCDECL AheadLib_GetFileVersionInfoExA(void)
//{
//	__asm JMP pfnGetFileVersionInfoExA;
//}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


ALCDECL AheadLib_GetFileVersionInfoExW(void) {
	__asm JMP pfnGetFileVersionInfoExW;
}

ALCDECL AheadLib_GetFileVersionInfoSizeA(void)
{
	__asm JMP pfnGetFileVersionInfoSizeA;
}

ALCDECL AheadLib_GetFileVersionInfoSizeExA(void)
{
	__asm JMP pfnGetFileVersionInfoSizeExA;
}


ALCDECL AheadLib_GetFileVersionInfoSizeExW(void)
{
	__asm JMP pfnGetFileVersionInfoSizeExW;
}

ALCDECL AheadLib_GetFileVersionInfoSizeW(void)
{
	__asm JMP pfnGetFileVersionInfoSizeW;
}

ALCDECL AheadLib_GetFileVersionInfoW(void)
{
	__asm JMP pfnGetFileVersionInfoW;
}

ALCDECL AheadLib_VerFindFileA(void)
{
	__asm JMP pfnVerFindFileA;
}

ALCDECL AheadLib_VerFindFileW(void)
{
	__asm JMP pfnVerFindFileW;
}

ALCDECL AheadLib_VerInstallFileA(void)
{
	__asm JMP pfnVerInstallFileA;
}

ALCDECL AheadLib_VerInstallFileW(void)
{
	__asm JMP pfnVerInstallFileW;
}

ALCDECL AheadLib_VerLanguageNameA(void)
{
	__asm JMP pfnVerLanguageNameA;
}

ALCDECL AheadLib_VerLanguageNameW(void)
{
	__asm JMP pfnVerLanguageNameW;
}

ALCDECL AheadLib_VerQueryValueA(void)
{
	__asm JMP pfnVerQueryValueA;
}

ALCDECL AheadLib_VerQueryValueW(void)
{
	__asm JMP pfnVerQueryValueW;
}

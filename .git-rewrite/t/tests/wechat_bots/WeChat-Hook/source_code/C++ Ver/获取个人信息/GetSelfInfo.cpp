#include "pch.h"
#include <Windows.h>
#include <stdio.h>
#include "resource.h"
#include "malloc.h"

/*
WeChatWin.dll

WeChatWin.dll+222EBB4		�ǳ�		��ַ		Ӣ���ǳ�
[WeChatWin.dll+222EBB4]		�ǳ�		��ַ		�����ǳ�
WeChatWin.dll+222EBE8		�ֻ�
WeChatWin.dll+222ECBC		ʡ/������
WeChatWin.dll+222ECD4		����
WeChatWin.dll+222EF30		����
WeChatWin.dll+222F058		��½�ֻ��ͺ�
WeChatWin.dll+222ED30		΢�ź�			���û������Ϊ��


[WeChatWin.dll+222EBB4+2E0]+0			ͷ��URL		222EE94
[WeChatWin.dll+222EBB4+46C]+0			΢��ID		222F020
[WeChatWin.dll+222EBB4+1C]+1			����

*/


//��Ϣ�ṹ��
struct wechatText
{
	wchar_t* pStr;
	int strLen;
	int iStrLen;
};

//wxid/UNICODE �ṹ��
struct wxString2
{
	wchar_t* pStr;
	int strLen;
	int strMaxLen;
	int fill;
	int	fill2;
};



DWORD ȡ΢��ģ���ַ()
{
	//��ȡģ����(��ַ)
	HMODULE winAddr = LoadLibrary("WeChatWin.dll");
	return (DWORD)winAddr;
}


wchar_t* UTF8ToUnicode(const char* str)
{
	int    textlen = 0;
	wchar_t* result;
	textlen = MultiByteToWideChar(CP_UTF8, 0, str, -1, NULL, 0);
	result = (wchar_t*)malloc((textlen + 1) * sizeof(wchar_t));
	memset(result, 0, (textlen + 1) * sizeof(wchar_t));
	MultiByteToWideChar(CP_UTF8, 0, str, -1, (LPWSTR)result, textlen);
	return    result;
}





//��ȡ�ڴ�����
VOID ReadWeChatData(HWND hwndDlg)
{
	//��ȡģ���ַ
	//HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, TRUE, -1);

	//CreateRemoteThread((HANDLE)-1, NULL, 0, (LPTHREAD_START_ROUTINE)ReadData_Thread, hwndDlg, 0, NULL);
	//CreateThread(NULL,0,(LPTHREAD_START_ROUTINE)ReadData_Thread, hwndDlg, 0, NULL);

	//CloseHandle(hProcess);
	HMODULE hModule = GetModuleHandle("WeChatWin.dll");
	CHAR ģ����[0x50] = { 0 };
	sprintf_s(ģ����, "[WeChatWin ���] 0x%08X", DWORD(hModule));
	OutputDebugStringA(ģ����);


	//��ȡģ���ַ
	DWORD WeChatWin_DLL = ȡ΢��ģ���ַ();
	CHAR W_HD[0x50] = { 0 };
	sprintf_s(W_HD, "[ģ���ַ] 0x%08X", WeChatWin_DLL);
	OutputDebugStringA(W_HD);


	DWORD ΢�źŵ�ַ = WeChatWin_DLL + 0x222ED30;
	CHAR ΢�ź�_HD[0x50] = { 0 };
	sprintf_s(΢�ź�_HD, "[΢�źŵ�ַ] 0x%08X", ΢�źŵ�ַ);
	OutputDebugStringA(΢�ź�_HD);


	
	//��ȡ�Լ����̵ľ��
	HANDLE hProcess = GetCurrentProcess();
	
	
	//װ΢��ID�ı���
	CHAR wx_id[0x100] = { 0 };
	INT wx_id_Addr;
	DWORD pWx_id = WeChatWin_DLL + 0x222F020;
	//sprintf_s(wx_id,"s%", *((DWORD*)pWx_id));

	ReadProcessMemory(hProcess, (LPVOID)pWx_id, &wx_id_Addr, 0x4, NULL);
	ReadProcessMemory(hProcess, (LPVOID)wx_id_Addr, wx_id, 0x100, NULL);
	OutputDebugStringA(wx_id);
	SetDlgItemText(hwndDlg,WXID, wx_id);
	


	//΢�ź�
	CHAR Buffer_[30] = { 0 };
	//TCHAR Buffer_[30] = { 0 };
	ReadProcessMemory(hProcess, (LPVOID)΢�źŵ�ַ, Buffer_, 30, NULL);
	OutputDebugStringA(Buffer_);
	SetDlgItemText(hwndDlg, WXACCOUNT, Buffer_);

	
	//΢��ͷ��URL
	CHAR headpic[0x100] = { 0 };
	DWORD pPic = WeChatWin_DLL + 0x222EE94;
	INT pPic_Addr;
	ReadProcessMemory(hProcess, (LPVOID)pPic, &pPic_Addr, 0x4, NULL);
	ReadProcessMemory(hProcess, (LPVOID)pPic_Addr, headpic, 0x100, NULL);
	SetDlgItemText(hwndDlg, HEAD_PIC, headpic);
	OutputDebugStringA(headpic);


	//CloseHandle(hProcess);


}



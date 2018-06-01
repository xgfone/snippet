## 1. Windows 10 关闭 Cortana
打开注册表（regedit）:

在 HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Windows Search 下添加 AllowCortana 选项，值为 0（类型为 DWORD(32)）。


write-host "Download llvm" -ForegroundColor Black -BackgroundColor DarkYellow
curl https://github.com/llvm/llvm-project/releases/download/llvmorg-13.0.0/LLVM-13.0.0-win64.exe -o llvm.exe
7z x llvm.exe -ollvm


write-host "LLVM paths" -ForegroundColor Black -BackgroundColor DarkYellow
write-host "$(get-location)\llvm\bin"
write-host "$(get-location)\llvm\lib\clang\13.0.0\lib\windows"

write-host "Download fd" -ForegroundColor Black -BackgroundColor DarkYellow
Invoke-WebRequest https://github.com/sharkdp/fd/releases/download/v8.2.1/fd-v8.2.1-i686-pc-windows-msvc.zip -OutFile fd.zip
7z x fd.zip -o"C:\Windows"


write-host "Download procdump" -ForegroundColor Black -BackgroundColor DarkYellow
curl "https://download.sysinternals.com/files/Procdump.zip" -o "Procdump.zip"
7z x Procdump.zip -o"C:\Windows"


write-host "Finding files" -ForegroundColor Black -BackgroundColor DarkYellow
fd.exe -HI clang_rt.asan_dynamic-x86_64.dll
fd.exe -HI clang_rt.asan_dll_thunk-x86_64.lib
fd.exe -HI clang_rt.asan-x86_64.lib
fd.exe -HI clang_rt.asan_cxx-x86_64.lib
fd.exe -HI clang.exe
fd.exe -HI lld-link.exe


write-host "Install python dependencies" -ForegroundColor Black -BackgroundColor DarkYellow
$env:PATH="C:\Python39-x64\Scripts;$env:PATH"
py -3.9-64 -m pip install -U pip wheel
py -3.9-64 -m pip install cffi

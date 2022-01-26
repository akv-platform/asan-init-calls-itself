$env:PATH="$(get-location)\bin;$(get-location)\lib\clang\13.0.0\lib\windows;$env:PATH"

$env:PATH="C:\Python36-x64;C:\Python36-x64\Scripts;$env:PATH"
$env:PYTHONHOME="C:\Python36-x64\"
$env:PYTHONPATH="C:\Python36-x64\Lib"

lldb ./src/py_file_run.exe C:\Python39-x64 .\test.py

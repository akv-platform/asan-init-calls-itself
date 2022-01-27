$repoPath =  $MyInvocation.MyCommand.Path | split-path | split-path

try {
    # Temporarily set environment variables
    $prevPath = $env:PATH
    $prevPythonHome = $env:PYTHONHOME
    $prevPythonPath = $env:PYTHONPATH


    $env:PATH="$repoPath\llvm\bin;$repoPath\llvm\lib\clang\13.0.0\lib\windows;$env:PATH"

    $env:PATH="C:\Python36-x64;C:\Python36-x64\Scripts;$env:PATH"
    $env:PYTHONHOME="C:\Python36-x64\"
    $env:PYTHONPATH="C:\Python36-x64\Lib"

    # lldb works with python 3.6 only, thus environment variables above
    lldb ./src/py_file_run.exe C:\Python39-x64 .\test.py

} finally {
    # restore the previous values
    $env:PATH = $prevPath
    $env:PYTHONHOME = $prevPythonHome
    $env:PYTHONPATH = $prevPythonPath
}

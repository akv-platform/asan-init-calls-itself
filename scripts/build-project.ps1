$repoPath =  $MyInvocation.MyCommand.Path | split-path | split-path

$env:PATH="$repoPath\llvm\bin;$env:PATH"
$env:PATH="$repoPath\llvm\lib\clang\13.0.0\lib\windows;$env:PATH"

write-host "Command locations" -ForegroundColor Black -BackgroundColor DarkYellow
get-command clang
get-command lld-link

# stderr to stdout to avoid appveyor crashing on warnings
py -3.9-64 src

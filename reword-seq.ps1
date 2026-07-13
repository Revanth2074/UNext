param($file) (Get-Content $file) -replace "^pick","reword" | Set-Content $file

# البحث عن استخدامات .success في ملفات Frontend
Get-ChildItem -Recurse -Include *.jsx,*.js -Path .\src | 
    Select-String -Pattern '\.success\s*===|response\.success|data\.success|result\.success' | 
    Select-Object -First 100 | 
    ForEach-Object { 
        "$($_.Path):$($_.LineNumber) -> $($_.Line.Trim())" 
    }


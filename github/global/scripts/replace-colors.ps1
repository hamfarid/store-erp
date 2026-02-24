# Script to replace hardcoded Tailwind colors with Gaara brand colors
# This script replaces:
# - bg-blue-* with bg-primary-*
# - text-blue-* with text-primary-*
# - border-blue-* with border-primary-*
# - focus:ring-blue-* with focus:ring-primary-*
# - hover:bg-blue-* with hover:bg-primary-*
# - bg-gray-* with bg-slate-* (neutral)
# - text-gray-* with text-slate-* (neutral)
# - border-gray-* with border-slate-* (neutral)

$files = Get-ChildItem -Path "frontend/src/components" -Include "*.jsx","*.js" -Recurse

$replacements = @(
    # Blue to Primary (Gaara Green)
    @{ old = 'bg-blue-50'; new = 'bg-primary-50' },
    @{ old = 'bg-blue-100'; new = 'bg-primary-100' },
    @{ old = 'bg-blue-200'; new = 'bg-primary-200' },
    @{ old = 'bg-blue-300'; new = 'bg-primary-300' },
    @{ old = 'bg-blue-400'; new = 'bg-primary-400' },
    @{ old = 'bg-blue-500'; new = 'bg-primary-500' },
    @{ old = 'bg-blue-600'; new = 'bg-primary-600' },
    @{ old = 'bg-blue-700'; new = 'bg-primary-700' },
    @{ old = 'bg-blue-800'; new = 'bg-primary-800' },
    @{ old = 'bg-blue-900'; new = 'bg-primary-900' },
    
    @{ old = 'text-blue-50'; new = 'text-primary-50' },
    @{ old = 'text-blue-100'; new = 'text-primary-100' },
    @{ old = 'text-blue-200'; new = 'text-primary-200' },
    @{ old = 'text-blue-300'; new = 'text-primary-300' },
    @{ old = 'text-blue-400'; new = 'text-primary-400' },
    @{ old = 'text-blue-500'; new = 'text-primary-500' },
    @{ old = 'text-blue-600'; new = 'text-primary-600' },
    @{ old = 'text-blue-700'; new = 'text-primary-700' },
    @{ old = 'text-blue-800'; new = 'text-primary-800' },
    @{ old = 'text-blue-900'; new = 'text-primary-900' },
    
    @{ old = 'border-blue-50'; new = 'border-primary-50' },
    @{ old = 'border-blue-100'; new = 'border-primary-100' },
    @{ old = 'border-blue-200'; new = 'border-primary-200' },
    @{ old = 'border-blue-300'; new = 'border-primary-300' },
    @{ old = 'border-blue-400'; new = 'border-primary-400' },
    @{ old = 'border-blue-500'; new = 'border-primary-500' },
    @{ old = 'border-blue-600'; new = 'border-primary-600' },
    @{ old = 'border-blue-700'; new = 'border-primary-700' },
    @{ old = 'border-blue-800'; new = 'border-primary-800' },
    @{ old = 'border-blue-900'; new = 'border-primary-900' },
    
    @{ old = 'focus:ring-blue-50'; new = 'focus:ring-primary-50' },
    @{ old = 'focus:ring-blue-100'; new = 'focus:ring-primary-100' },
    @{ old = 'focus:ring-blue-200'; new = 'focus:ring-primary-200' },
    @{ old = 'focus:ring-blue-300'; new = 'focus:ring-primary-300' },
    @{ old = 'focus:ring-blue-400'; new = 'focus:ring-primary-400' },
    @{ old = 'focus:ring-blue-500'; new = 'focus:ring-primary-500' },
    @{ old = 'focus:ring-blue-600'; new = 'focus:ring-primary-600' },
    @{ old = 'focus:ring-blue-700'; new = 'focus:ring-primary-700' },
    @{ old = 'focus:ring-blue-800'; new = 'focus:ring-primary-800' },
    @{ old = 'focus:ring-blue-900'; new = 'focus:ring-primary-900' },
    
    @{ old = 'hover:bg-blue-50'; new = 'hover:bg-primary-50' },
    @{ old = 'hover:bg-blue-100'; new = 'hover:bg-primary-100' },
    @{ old = 'hover:bg-blue-200'; new = 'hover:bg-primary-200' },
    @{ old = 'hover:bg-blue-300'; new = 'hover:bg-primary-300' },
    @{ old = 'hover:bg-blue-400'; new = 'hover:bg-primary-400' },
    @{ old = 'hover:bg-blue-500'; new = 'hover:bg-primary-500' },
    @{ old = 'hover:bg-blue-600'; new = 'hover:bg-primary-600' },
    @{ old = 'hover:bg-blue-700'; new = 'hover:bg-primary-700' },
    @{ old = 'hover:bg-blue-800'; new = 'hover:bg-primary-800' },
    @{ old = 'hover:bg-blue-900'; new = 'hover:bg-primary-900' },
    
    # Indigo to Secondary (Gaara Forest Green)
    @{ old = 'from-indigo-100'; new = 'from-secondary-100' },
    @{ old = 'to-indigo-100'; new = 'to-secondary-100' }
)

$count = 0
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $originalContent = $content
    
    foreach ($replacement in $replacements) {
        $content = $content -replace [regex]::Escape($replacement.old), $replacement.new
    }
    
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
        $count++
        Write-Host "✅ Updated: $($file.Name)"
    }
}

Write-Host "`n✅ Total files updated: $count"


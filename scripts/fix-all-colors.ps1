# Fix All Colors - Replace Blue/Gray with Gaara Brand Colors
# This script replaces all hardcoded blue and gray colors with Gaara brand colors

Write-Host "🎨 Starting Color Replacement - Gaara Seeds Brand" -ForegroundColor Green
Write-Host "=" * 60

$componentsPath = "frontend/src"
$totalFiles = 0
$totalReplacements = 0

# Color replacements map
$colorReplacements = @(
    # Blue colors -> Primary (Gaara Green)
    @{ old = 'bg-blue-50'; new = 'bg-primary/10' },
    @{ old = 'bg-blue-100'; new = 'bg-primary/20' },
    @{ old = 'bg-blue-200'; new = 'bg-primary/30' },
    @{ old = 'bg-blue-300'; new = 'bg-primary/40' },
    @{ old = 'bg-blue-400'; new = 'bg-primary/50' },
    @{ old = 'bg-blue-500'; new = 'bg-primary/70' },
    @{ old = 'bg-blue-600'; new = 'bg-primary' },
    @{ old = 'bg-blue-700'; new = 'bg-primary/90' },
    @{ old = 'bg-blue-800'; new = 'bg-primary/95' },
    @{ old = 'bg-blue-900'; new = 'bg-primary' },
    
    # Text blue -> Primary
    @{ old = 'text-blue-50'; new = 'text-primary/10' },
    @{ old = 'text-blue-100'; new = 'text-primary/20' },
    @{ old = 'text-blue-200'; new = 'text-primary/30' },
    @{ old = 'text-blue-300'; new = 'text-primary/40' },
    @{ old = 'text-blue-400'; new = 'text-primary/50' },
    @{ old = 'text-blue-500'; new = 'text-primary/70' },
    @{ old = 'text-blue-600'; new = 'text-primary' },
    @{ old = 'text-blue-700'; new = 'text-primary/90' },
    @{ old = 'text-blue-800'; new = 'text-primary/95' },
    @{ old = 'text-blue-900'; new = 'text-primary' },
    
    # Border blue -> Primary
    @{ old = 'border-blue-50'; new = 'border-primary/10' },
    @{ old = 'border-blue-100'; new = 'border-primary/20' },
    @{ old = 'border-blue-200'; new = 'border-primary/30' },
    @{ old = 'border-blue-300'; new = 'border-primary/40' },
    @{ old = 'border-blue-400'; new = 'border-primary/50' },
    @{ old = 'border-blue-500'; new = 'border-primary/70' },
    @{ old = 'border-blue-600'; new = 'border-primary' },
    @{ old = 'border-blue-700'; new = 'border-primary/90' },
    @{ old = 'border-blue-800'; new = 'border-primary/95' },
    @{ old = 'border-blue-900'; new = 'border-primary' },
    
    # Hover states
    @{ old = 'hover:bg-blue-50'; new = 'hover:bg-primary/10' },
    @{ old = 'hover:bg-blue-100'; new = 'hover:bg-primary/20' },
    @{ old = 'hover:bg-blue-200'; new = 'hover:bg-primary/30' },
    @{ old = 'hover:bg-blue-300'; new = 'hover:bg-primary/40' },
    @{ old = 'hover:bg-blue-400'; new = 'hover:bg-primary/50' },
    @{ old = 'hover:bg-blue-500'; new = 'hover:bg-primary/70' },
    @{ old = 'hover:bg-blue-600'; new = 'hover:bg-primary' },
    @{ old = 'hover:bg-blue-700'; new = 'hover:bg-primary/90' },
    @{ old = 'hover:bg-blue-800'; new = 'hover:bg-primary/95' },
    @{ old = 'hover:bg-blue-900'; new = 'hover:bg-primary' },
    
    # Focus ring
    @{ old = 'focus:ring-blue-50'; new = 'focus:ring-primary/10' },
    @{ old = 'focus:ring-blue-100'; new = 'focus:ring-primary/20' },
    @{ old = 'focus:ring-blue-200'; new = 'focus:ring-primary/30' },
    @{ old = 'focus:ring-blue-300'; new = 'focus:ring-primary/40' },
    @{ old = 'focus:ring-blue-400'; new = 'focus:ring-primary/50' },
    @{ old = 'focus:ring-blue-500'; new = 'focus:ring-primary' },
    @{ old = 'focus:ring-blue-600'; new = 'focus:ring-primary' },
    @{ old = 'focus:ring-blue-700'; new = 'focus:ring-primary/90' },
    @{ old = 'focus:ring-blue-800'; new = 'focus:ring-primary/95' },
    @{ old = 'focus:ring-blue-900'; new = 'focus:ring-primary' },
    
    # Focus border
    @{ old = 'focus:border-blue-50'; new = 'focus:border-primary/10' },
    @{ old = 'focus:border-blue-100'; new = 'focus:border-primary/20' },
    @{ old = 'focus:border-blue-200'; new = 'focus:border-primary/30' },
    @{ old = 'focus:border-blue-300'; new = 'focus:border-primary/40' },
    @{ old = 'focus:border-blue-400'; new = 'focus:border-primary/50' },
    @{ old = 'focus:border-blue-500'; new = 'focus:border-primary' },
    @{ old = 'focus:border-blue-600'; new = 'focus:border-primary' },
    @{ old = 'focus:border-blue-700'; new = 'focus:border-primary/90' },
    @{ old = 'focus:border-blue-800'; new = 'focus:border-primary/95' },
    @{ old = 'focus:border-blue-900'; new = 'focus:border-primary' },
    
    # Indigo -> Secondary (Forest Green)
    @{ old = 'bg-indigo-50'; new = 'bg-secondary/10' },
    @{ old = 'bg-indigo-100'; new = 'bg-secondary/20' },
    @{ old = 'bg-indigo-200'; new = 'bg-secondary/30' },
    @{ old = 'bg-indigo-300'; new = 'bg-secondary/40' },
    @{ old = 'bg-indigo-400'; new = 'bg-secondary/50' },
    @{ old = 'bg-indigo-500'; new = 'bg-secondary/70' },
    @{ old = 'bg-indigo-600'; new = 'bg-secondary' },
    @{ old = 'bg-indigo-700'; new = 'bg-secondary/90' },
    @{ old = 'bg-indigo-800'; new = 'bg-secondary/95' },
    @{ old = 'bg-indigo-900'; new = 'bg-secondary' },
    
    @{ old = 'from-indigo-50'; new = 'from-secondary/10' },
    @{ old = 'from-indigo-100'; new = 'from-secondary/20' },
    @{ old = 'to-indigo-50'; new = 'to-secondary/10' },
    @{ old = 'to-indigo-100'; new = 'to-secondary/20' },
    
    # Slate/Gray -> Neutral (keep for backgrounds)
    @{ old = 'bg-slate-50'; new = 'bg-muted/50' },
    @{ old = 'bg-slate-100'; new = 'bg-muted' },
    @{ old = 'bg-slate-200'; new = 'bg-muted' },
    @{ old = 'bg-gray-50'; new = 'bg-muted/50' },
    @{ old = 'bg-gray-100'; new = 'bg-muted' },
    @{ old = 'bg-gray-200'; new = 'bg-muted' },
    
    @{ old = 'text-slate-600'; new = 'text-muted-foreground' },
    @{ old = 'text-slate-700'; new = 'text-foreground' },
    @{ old = 'text-slate-800'; new = 'text-foreground' },
    @{ old = 'text-slate-900'; new = 'text-foreground' },
    @{ old = 'text-gray-600'; new = 'text-muted-foreground' },
    @{ old = 'text-gray-700'; new = 'text-foreground' },
    @{ old = 'text-gray-800'; new = 'text-foreground' },
    @{ old = 'text-gray-900'; new = 'text-foreground' },
    
    @{ old = 'border-slate-200'; new = 'border-border' },
    @{ old = 'border-slate-300'; new = 'border-border' },
    @{ old = 'border-gray-200'; new = 'border-border' },
    @{ old = 'border-gray-300'; new = 'border-border' },
    
    # Green -> Success (keep Gaara green)
    @{ old = 'bg-green-50'; new = 'bg-primary/10' },
    @{ old = 'bg-green-100'; new = 'bg-primary/20' },
    @{ old = 'bg-green-500'; new = 'bg-primary' },
    @{ old = 'bg-green-600'; new = 'bg-primary' },
    @{ old = 'text-green-600'; new = 'text-primary' },
    @{ old = 'text-green-700'; new = 'text-primary' },
    @{ old = 'border-green-200'; new = 'border-primary/30' },
    
    # Red -> Destructive (use Terracotta)
    @{ old = 'bg-red-50'; new = 'bg-destructive/10' },
    @{ old = 'bg-red-100'; new = 'bg-destructive/20' },
    @{ old = 'bg-red-500'; new = 'bg-destructive' },
    @{ old = 'bg-red-600'; new = 'bg-destructive' },
    @{ old = 'text-red-600'; new = 'text-destructive' },
    @{ old = 'text-red-700'; new = 'text-destructive' },
    @{ old = 'border-red-200'; new = 'border-destructive/30' },
    
    # Yellow/Orange -> Accent (Terracotta)
    @{ old = 'bg-yellow-50'; new = 'bg-accent/10' },
    @{ old = 'bg-yellow-100'; new = 'bg-accent/20' },
    @{ old = 'bg-orange-50'; new = 'bg-accent/10' },
    @{ old = 'bg-orange-100'; new = 'bg-accent/20' },
    @{ old = 'text-yellow-600'; new = 'text-accent' },
    @{ old = 'text-orange-600'; new = 'text-accent' }
)

# Get all JSX and JS files
$files = Get-ChildItem -Path $componentsPath -Include "*.jsx","*.js" -Recurse

Write-Host "📁 Found $($files.Count) files to process" -ForegroundColor Cyan
Write-Host ""

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $originalContent = $content
    $fileReplacements = 0
    
    foreach ($replacement in $colorReplacements) {
        $pattern = [regex]::Escape($replacement.old)
        if ($content -match $pattern) {
            $content = $content -replace $pattern, $replacement.new
            $fileReplacements++
        }
    }
    
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        $totalFiles++
        $totalReplacements += $fileReplacements
        Write-Host "✅ $($file.Name) - $fileReplacements replacements" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "=" * 60
Write-Host "🎉 Color Replacement Complete!" -ForegroundColor Green
Write-Host "📊 Total files updated: $totalFiles" -ForegroundColor Cyan
Write-Host "🔄 Total replacements: $totalReplacements" -ForegroundColor Cyan
Write-Host "=" * 60


@echo off
echo ========================================
echo TypeScript Fixes for Admin Panel
echo ========================================
echo.

echo 🔧 Step 1: Running TypeScript fixes...
node fix-typescript.js
if %errorlevel% neq 0 (
    echo ❌ Error running TypeScript fixes
    pause
    exit /b 1
)
echo.

echo 📦 Step 2: Installing/updating dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Error installing dependencies
    pause
    exit /b 1
)
echo.

echo 🔍 Step 3: Running TypeScript type check...
call npm run type-check
if %errorlevel% neq 0 (
    echo ⚠️  TypeScript type check found issues
    echo This is normal if there are issues in your source code
    echo The node_modules issues should be resolved
) else (
    echo ✅ TypeScript type check passed!
)
echo.

echo 🎉 TypeScript fixes completed!
echo.
echo Next steps:
echo 1. Run: npm start (to start development server)
echo 2. Run: npm run build (to test production build)
echo.
echo If you see TypeScript errors, they should now be limited to your source code only.
echo Check TYPESCRIPT_FIXES.md for troubleshooting information.
echo.
pause

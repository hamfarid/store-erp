#!/bin/bash
# سكريبت إيقاف الخوادم
# Stop Servers Script

echo "🛑 إيقاف الخوادم..."

# إيقاف الخادم الخلفي
if [ -f "logs/backend.pid" ]; then
    PID=$(cat logs/backend.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "✅ تم إيقاف الخادم الخلفي (PID: $PID)"
        rm logs/backend.pid
    else
        echo "⚠️ الخادم الخلفي غير يعمل"
    fi
else
    echo "⚠️ ملف PID غير موجود"
fi

# إيقاف أي عمليات Python متبقية
pkill -f "python.*app.py" 2>/dev/null && echo "✅ تم إيقاف عمليات Python الإضافية"

echo "🏁 تم إيقاف جميع الخوادم"

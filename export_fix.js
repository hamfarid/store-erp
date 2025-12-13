
// إصلاح وظائف التصدير في لوحة الإدارة
async function exportDataFixed(type) {
    try {
        showLoading('import-export-result');
        
        const response = await fetch(`${BACKEND_URL}/api/export/integrated`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                type: type,
                format: 'json', // استخدام JSON بدلاً من Excel
                include_relations: true
            })
        });

        const data = await response.json();
        
        if (data.success) {
            // تحويل البيانات إلى CSV
            const csvContent = convertToCSV(data.data);
            downloadCSV(csvContent, `${type}_export_${new Date().toISOString().slice(0,10)}.csv`);
            
            document.getElementById('import-export-result').textContent = 
                `✅ تم تصدير ${data.data.length} سجل بصيغة CSV`;
            document.getElementById('import-export-result').className = 'result success';
        } else {
            document.getElementById('import-export-result').textContent = 
                `❌ خطأ في التصدير: ${data.error}`;
            document.getElementById('import-export-result').className = 'result error';
        }
    } catch (error) {
        document.getElementById('import-export-result').textContent = 
            `❌ خطأ في تصدير البيانات: ${error.message}`;
        document.getElementById('import-export-result').className = 'result error';
    }
}

function convertToCSV(data) {
    if (!data || data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const csvRows = [headers.join(',')];
    
    for (const row of data) {
        const values = headers.map(header => {
            const value = row[header];
            return typeof value === 'string' ? `"${value.replace(/"/g, '""')}"` : value;
        });
        csvRows.push(values.join(','));
    }
    
    return csvRows.join('\n');
}

function downloadCSV(csvContent, filename) {
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

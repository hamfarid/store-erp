#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function cleanConsoleFromFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalLength = content.length;
    
    // إزالة console.log, console.error, console.warn, console.info
    content = content.replace(/console\.(log|error|warn|info|debug)\([^)]*\);?\s*/g, '');
    
    // إزالة الأسطر الفارغة الزائدة
    content = content.replace(/\n\s*\n\s*\n/g, '\n\n');
    
    if (content.length !== originalLength) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ تم تنظيف: ${filePath}`);
      return true;
    }
    return false;
  } catch (error) {
    console.error(`❌ خطأ في معالجة ${filePath}:`, error.message);
    return false;
  }
}

function cleanConsoleFromDirectory(dirPath) {
  let cleanedFiles = 0;
  
  function processDirectory(currentPath) {
    const items = fs.readdirSync(currentPath);
    
    for (const item of items) {
      const fullPath = path.join(currentPath, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory() && !item.startsWith('.') && item !== 'node_modules') {
        processDirectory(fullPath);
      } else if (stat.isFile() && (item.endsWith('.js') || item.endsWith('.jsx'))) {
        if (cleanConsoleFromFile(fullPath)) {
          cleanedFiles++;
        }
      }
    }
  }
  
  processDirectory(dirPath);
  return cleanedFiles;
}

// تشغيل التنظيف
console.log('🧹 بدء تنظيف console.log من الملفات...');
const cleanedCount = cleanConsoleFromDirectory('./src');
console.log(`\n✨ تم الانتهاء! تم تنظيف ${cleanedCount} ملف`);

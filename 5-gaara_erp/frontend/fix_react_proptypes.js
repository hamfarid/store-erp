#!/usr/bin/env node
/**
 * إصلاح PropTypes في مكونات React
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// البحث عن جميع ملفات JSX
function findJSXFiles(dir) {
  const files = [];
  
  function scanDir(currentDir) {
    const items = fs.readdirSync(currentDir);
    
    for (const item of items) {
      const fullPath = path.join(currentDir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        // تجاهل مجلدات معينة
        if (!['node_modules', '.git', 'dist', 'build'].includes(item)) {
          scanDir(fullPath);
        }
      } else if (item.endsWith('.jsx') || item.endsWith('.js')) {
        files.push(fullPath);
      }
    }
  }
  
  scanDir(dir);
  return files;
}

// تحليل مكون React لاستخراج Props
function analyzeComponent(content) {
  const props = new Set();
  
  // البحث عن props في function components
  const functionComponentMatch = content.match(/const\s+(\w+)\s*=\s*\(\s*\{([^}]*)\}\s*\)/);
  if (functionComponentMatch) {
    const propsString = functionComponentMatch[2];
    const propMatches = propsString.match(/\w+/g);
    if (propMatches) {
      propMatches.forEach(prop => props.add(prop));
    }
  }
  
  // البحث عن props.something
  const propUsageMatches = content.match(/props\.(\w+)/g);
  if (propUsageMatches) {
    propUsageMatches.forEach(match => {
      const prop = match.replace('props.', '');
      props.add(prop);
    });
  }
  
  // البحث عن destructured props في function body
  const destructureMatches = content.match(/const\s*\{([^}]+)\}\s*=\s*props/g);
  if (destructureMatches) {
    destructureMatches.forEach(match => {
      const propsString = match.match(/\{([^}]+)\}/)[1];
      const propNames = propsString.split(',').map(p => p.trim().split(':')[0].trim());
      propNames.forEach(prop => props.add(prop));
    });
  }
  
  return Array.from(props);
}

// إنشاء PropTypes definition
function generatePropTypes(componentName, props) {
  if (props.length === 0) return '';
  
  const propTypeLines = props.map(prop => {
    // تخمين نوع البيانات بناءً على اسم الخاصية
    let propType = 'PropTypes.any';
    
    if (prop.includes('id') || prop.includes('Id')) {
      propType = 'PropTypes.oneOfType([PropTypes.string, PropTypes.number])';
    } else if (prop.includes('name') || prop.includes('title') || prop.includes('label')) {
      propType = 'PropTypes.string';
    } else if (prop.includes('count') || prop.includes('amount') || prop.includes('price')) {
      propType = 'PropTypes.number';
    } else if (prop.includes('is') || prop.includes('has') || prop.includes('show')) {
      propType = 'PropTypes.bool';
    } else if (prop.includes('onClick') || prop.includes('onSubmit') || prop.includes('onChange')) {
      propType = 'PropTypes.func';
    } else if (prop.includes('children')) {
      propType = 'PropTypes.node';
    } else if (prop.includes('data') || prop.includes('items') || prop.includes('list')) {
      propType = 'PropTypes.array';
    } else if (prop.includes('config') || prop.includes('settings') || prop.includes('options')) {
      propType = 'PropTypes.object';
    }
    
    return `  ${prop}: ${propType}`;
  });
  
  return `
${componentName}.propTypes = {
${propTypeLines.join(',\n')}
};`;
}

// إصلاح ملف واحد
function fixFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    
    // تحقق من وجود React component
    if (!content.includes('import React') && !content.includes('from \'react\'')) {
      return false;
    }
    
    // تحقق من وجود PropTypes import
    const hasPropTypesImport = content.includes('import PropTypes from \'prop-types\'');
    
    // استخراج اسم المكون
    const componentNameMatch = content.match(/(?:const|function)\s+(\w+)\s*[=(]/);
    if (!componentNameMatch) return false;
    
    const componentName = componentNameMatch[1];
    
    // تحليل Props
    const props = analyzeComponent(content);
    
    if (props.length === 0) {
      console.log(`✅ ${path.basename(filePath)}: No props found`);
      return false;
    }
    
    // تحقق من وجود PropTypes definition
    if (content.includes(`${componentName}.propTypes`)) {
      console.log(`✅ ${path.basename(filePath)}: PropTypes already defined`);
      return false;
    }
    
    let newContent = content;
    
    // إضافة PropTypes import إذا لم يكن موجوداً
    if (!hasPropTypesImport) {
      newContent = newContent.replace(
        /import React[^;]+;/,
        match => `${match}\nimport PropTypes from 'prop-types';`
      );
    }
    
    // إضافة PropTypes definition
    const propTypesDefinition = generatePropTypes(componentName, props);
    
    // البحث عن نهاية المكون لإضافة PropTypes
    const exportMatch = newContent.match(/export\s+default\s+\w+/);
    if (exportMatch) {
      newContent = newContent.replace(
        exportMatch[0],
        `${propTypesDefinition}\n\n${exportMatch[0]}`
      );
    } else {
      // إضافة في نهاية الملف
      newContent += propTypesDefinition;
    }
    
    // كتابة الملف المحدث
    fs.writeFileSync(filePath, newContent, 'utf8');
    
    console.log(`🔧 ${path.basename(filePath)}: Added PropTypes for ${props.length} props`);
    return true;
    
  } catch (error) {
    console.error(`❌ Error fixing ${filePath}: ${error.message}`);
    return false;
  }
}

// الدالة الرئيسية
function main() {
  console.log('🚀 === إصلاح PropTypes في مكونات React ===');
  
  const srcDir = path.join(__dirname, 'src');
  
  if (!fs.existsSync(srcDir)) {
    console.error('❌ مجلد src غير موجود');
    return;
  }
  
  const jsxFiles = findJSXFiles(srcDir);
  console.log(`📁 تم العثور على ${jsxFiles.length} ملف JSX/JS`);
  
  let fixedCount = 0;
  
  for (const file of jsxFiles) {
    if (fixFile(file)) {
      fixedCount++;
    }
  }
  
  console.log(`\n📊 === ملخص النتائج ===`);
  console.log(`✅ الملفات المفحوصة: ${jsxFiles.length}`);
  console.log(`🔧 الملفات المُصلحة: ${fixedCount}`);
  
  if (fixedCount > 0) {
    console.log('🎉 تم إضافة PropTypes بنجاح!');
  } else {
    console.log('✅ جميع الملفات تحتوي على PropTypes بالفعل!');
  }
}

// تشغيل الدالة الرئيسية إذا تم تشغيل الملف مباشرة
if (typeof process !== 'undefined' && [{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/src/utils/logger.js",
	"owner": "eslint",
	"code": {
		"value": "no-undef",
		"target": {
			"$mid": 1,
			"path": "/docs/latest/rules/no-undef",
			"scheme": "https",
			"authority": "eslint.org"
		}
	},
	"severity": 8,
	"message": "'process' is not defined.",
	"source": "eslint",
	"startLineNumber": 46,
	"startColumn": 43,
	"endLineNumber": 46,
	"endColumn": 50,
	"origin": "extHost3"
},{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/src/utils/logger.js",
	"owner": "eslint",
	"code": {
		"value": "no-undef",
		"target": {
			"$mid": 1,
			"path": "/docs/latest/rules/no-undef",
			"scheme": "https",
			"authority": "eslint.org"
		}
	},
	"severity": 8,
	"message": "'process' is not defined.",
	"source": "eslint",
	"startLineNumber": 72,
	"startColumn": 9,
	"endLineNumber": 72,
	"endColumn": 16,
	"origin": "extHost3"
},{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/src/utils/logger.js",
	"owner": "eslint",
	"code": {
		"value": "no-undef",
		"target": {
			"$mid": 1,
			"path": "/docs/latest/rules/no-undef",
			"scheme": "https",
			"authority": "eslint.org"
		}
	},
	"severity": 8,
	"message": "'process' is not defined.",
	"source": "eslint",
	"startLineNumber": 116,
	"startColumn": 9,
	"endLineNumber": 116,
	"endColumn": 16,
	"origin": "extHost3"
},{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/src/utils/logger.js",
	"owner": "eslint",
	"code": {
		"value": "no-prototype-builtins",
		"target": {
			"$mid": 1,
			"path": "/docs/latest/rules/no-prototype-builtins",
			"scheme": "https",
			"authority": "eslint.org"
		}
	},
	"severity": 8,
	"message": "Do not access Object.prototype method 'hasOwnProperty' from target object.",
	"source": "eslint",
	"startLineNumber": 225,
	"startColumn": 21,
	"endLineNumber": 225,
	"endColumn": 35,
	"origin": "extHost3"
},{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/src/utils/logger.js",
	"owner": "eslint",
	"code": {
		"value": "no-unused-vars",
		"target": {
			"$mid": 1,
			"path": "/docs/latest/rules/no-unused-vars",
			"scheme": "https",
			"authority": "eslint.org"
		}
	},
	"severity": 8,
	"message": "'error' is defined but never used.",
	"source": "eslint",
	"startLineNumber": 230,
	"startColumn": 14,
	"endLineNumber": 230,
	"endColumn": 19,
	"tags": [
		1
	],
	"origin": "extHost3"
},{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/src/utils/logger.js",
	"owner": "sonarlint",
	"code": "javascript:S2486",
	"severity": 4,
	"message": "Handle this exception or don't catch it at all.",
	"source": "sonarqube",
	"startLineNumber": 230,
	"startColumn": 7,
	"endLineNumber": 232,
	"endColumn": 6,
	"origin": "extHost3"
},{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/fix_react_proptypes.js",
	"owner": "eslint",
	"code": {
		"value": "no-undef",
		"target": {
			"$mid": 1,
			"path": "/docs/latest/rules/no-undef",
			"scheme": "https",
			"authority": "eslint.org"
		}
	},
	"severity": 8,
	"message": "'process' is not defined.",
	"source": "eslint",
	"startLineNumber": 214,
	"startColumn": 39,
	"endLineNumber": 214,
	"endColumn": 46,
	"origin": "extHost3"
},{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/fix_react_proptypes.js",
	"owner": "eslint",
	"code": {
		"value": "no-undef",
		"target": {
			"$mid": 1,
			"path": "/docs/latest/rules/no-undef",
			"scheme": "https",
			"authority": "eslint.org"
		}
	},
	"severity": 8,
	"message": "'process' is not defined.",
	"source": "eslint",
	"startLineNumber": 214,
	"startColumn": 85,
	"endLineNumber": 214,
	"endColumn": 92,
	"origin": "extHost3"
},{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/src/components/ErrorBoundary.js",
	"owner": "eslint",
	"code": {
		"value": "no-undef",
		"target": {
			"$mid": 1,
			"path": "/docs/latest/rules/no-undef",
			"scheme": "https",
			"authority": "eslint.org"
		}
	},
	"severity": 8,
	"message": "'process' is not defined.",
	"source": "eslint",
	"startLineNumber": 278,
	"startColumn": 64,
	"endLineNumber": 278,
	"endColumn": 71,
	"origin": "extHost3"
},{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/src/services/api.js",
	"owner": "eslint",
	"code": {
		"value": "no-undef",
		"target": {
			"$mid": 1,
			"path": "/docs/latest/rules/no-undef",
			"scheme": "https",
			"authority": "eslint.org"
		}
	},
	"severity": 8,
	"message": "'process' is not defined.",
	"source": "eslint",
	"startLineNumber": 9,
	"startColumn": 57,
	"endLineNumber": 9,
	"endColumn": 64,
	"origin": "extHost3"
},{
	"resource": "/d:/home/ubuntu/store_v1.2/complete_inventory_system/frontend/src/services/apiClient.js",
	"owner": "eslint",
	"code": {
		"value": "no-undef",
		"target": {
			"$mid": 1,
			"path": "/docs/latest/rules/no-undef",
			"scheme": "https",
			"authority": "eslint.org"
		}
	},
	"severity": 8,
	"message": "'process' is not defined.",
	"source": "eslint",
	"startLineNumber": 8,
	"startColumn": 55,
	"endLineNumber": 8,
	"endColumn": 62,
	"origin": "extHost3"
}].argv && import.meta.url === `file://${process.argv[1]}`) {
  main(); 
}

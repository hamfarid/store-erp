#!/usr/bin/env node

/**
 * OWASP ZAP Results Parser - Enhanced Version 2.0
 * Parses ZAP JSON output and generates PR comments with findings
 * Features:
 * - False positive filtering
 * - GitHub PR comment integration
 * - Severity-based categorization
 * - Detailed remediation guidance
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  inputFile: process.env.ZAP_REPORT || 'zap-baseline.json',
  outputFile: 'zap-findings.md',
  prCommentFile: 'zap-pr-comment.md',
  severityLevels: {
    'High': 3,
    'Medium': 2,
    'Low': 1,
    'Informational': 0
  },
  failOnSeverity: process.env.ZAP_FAIL_SEVERITY || 'High',
  // False positive patterns to filter out
  falsePositivePatterns: [
    { id: '10011', urlPattern: /localhost|127\.0\.0\.1/, reason: 'Development environment' },
    { id: '10015', urlPattern: /\.(js|css|png|jpg|gif|ico|woff|ttf)$/, reason: 'Static assets' },
    { id: '10027', urlPattern: /api-docs|swagger|openapi/, reason: 'API documentation' },
    { id: '10023', contentPattern: /[\u0600-\u06FF]+/, reason: 'Arabic language content' }
  ],
  // Severity escalation rules
  escalationRules: [
    { id: '40018', newSeverity: 'Critical', reason: 'SQL Injection' },
    { id: '40012', newSeverity: 'Critical', reason: 'XSS Reflected' },
    { id: '40014', newSeverity: 'Critical', reason: 'XSS Stored' },
    { id: '40032', newSeverity: 'Critical', reason: 'CSRF' }
  ]
};

/**
 * Parse ZAP JSON report
 */
function parseZapReport(filePath) {
  try {
    if (!fs.existsSync(filePath)) {
      console.error(`❌ Report file not found: ${filePath}`);
      process.exit(1);
    }

    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(`❌ Error parsing ZAP report: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Filter false positives based on configured patterns
 */
function filterFalsePositives(alerts) {
  return alerts.filter(alert => {
    // Check each false positive pattern
    for (const pattern of CONFIG.falsePositivePatterns) {
      // Match by plugin ID
      if (pattern.id && alert.pluginid === pattern.id) {
        // Check URL pattern if specified
        if (pattern.urlPattern && alert.instances) {
          const hasMatchingUrl = alert.instances.some(instance =>
            pattern.urlPattern.test(instance.uri)
          );
          if (hasMatchingUrl) {
            console.log(`⚠️  Filtered false positive: ${alert.name} (${pattern.reason})`);
            return false;
          }
        }

        // Check content pattern if specified
        if (pattern.contentPattern && alert.description) {
          if (pattern.contentPattern.test(alert.description)) {
            console.log(`⚠️  Filtered false positive: ${alert.name} (${pattern.reason})`);
            return false;
          }
        }
      }
    }
    return true;
  });
}

/**
 * Apply severity escalation rules
 */
function applySeverityEscalation(alerts) {
  return alerts.map(alert => {
    const rule = CONFIG.escalationRules.find(r => r.id === alert.pluginid);
    if (rule) {
      console.log(`⬆️  Escalating ${alert.name} to ${rule.newSeverity} (${rule.reason})`);
      return {
        ...alert,
        originalSeverity: alert.riskcode,
        riskcode: rule.newSeverity === 'Critical' ? '4' : alert.riskcode,
        escalated: true,
        escalationReason: rule.reason
      };
    }
    return alert;
  });
}

/**
 * Group alerts by severity
 */
function groupAlertsBySeverity(alerts) {
  const grouped = {
    Critical: [],
    High: [],
    Medium: [],
    Low: [],
    Informational: []
  };

  alerts.forEach(alert => {
    const severity = alert.riskcode === '4' ? 'Critical' :
                    alert.riskcode === '3' ? 'High' :
                    alert.riskcode === '2' ? 'Medium' :
                    alert.riskcode === '1' ? 'Low' : 'Informational';
    grouped[severity].push(alert);
  });

  return grouped;
}

/**
 * Generate markdown report
 */
function generateMarkdownReport(report, stats) {
  const alerts = report.site[0]?.alerts || [];
  const grouped = groupAlertsBySeverity(alerts);

  let markdown = '# 🔒 OWASP ZAP Security Scan Results\n\n';
  markdown += `**Scan Date:** ${new Date().toISOString()}\n`;
  markdown += `**Total Alerts (Raw):** ${stats.totalRaw}\n`;
  markdown += `**Total Alerts (After Filtering):** ${stats.totalFiltered}\n`;
  markdown += `**False Positives Filtered:** ${stats.falsePositivesFiltered}\n`;
  markdown += `**Alerts Escalated:** ${stats.alertsEscalated}\n\n`;

  // Summary
  markdown += '## Summary\n\n';
  markdown += `| Severity | Count |\n`;
  markdown += `|----------|-------|\n`;
  markdown += `| 🔴 Critical | ${grouped.Critical.length} |\n`;
  markdown += `| 🟠 High | ${grouped.High.length} |\n`;
  markdown += `| 🟡 Medium | ${grouped.Medium.length} |\n`;
  markdown += `| 🔵 Low | ${grouped.Low.length} |\n`;
  markdown += `| ℹ️ Informational | ${grouped.Informational.length} |\n\n`;

  // Critical severity alerts
  if (grouped.Critical.length > 0) {
    markdown += '## 🔴 Critical Severity Issues\n\n';
    markdown += '⚠️ **IMMEDIATE ACTION REQUIRED** - These issues pose severe security risks\n\n';
    grouped.Critical.forEach((alert, idx) => {
      markdown += generateAlertMarkdown(alert, idx + 1);
    });
  }

  // High severity alerts
  if (grouped.High.length > 0) {
    markdown += '## 🔴 High Severity Issues\n\n';
    grouped.High.forEach((alert, idx) => {
      markdown += generateAlertMarkdown(alert, idx + 1);
    });
  }

  // Medium severity alerts
  if (grouped.Medium.length > 0) {
    markdown += '## 🟠 Medium Severity Issues\n\n';
    grouped.Medium.forEach((alert, idx) => {
      markdown += generateAlertMarkdown(alert, idx + 1);
    });
  }

  // Low severity alerts
  if (grouped.Low.length > 0) {
    markdown += '## 🟡 Low Severity Issues\n\n';
    grouped.Low.forEach((alert, idx) => {
      markdown += generateAlertMarkdown(alert, idx + 1);
    });
  }

  // Informational alerts
  if (grouped.Informational.length > 0) {
    markdown += '## ℹ️ Informational Issues\n\n';
    grouped.Informational.forEach((alert, idx) => {
      markdown += generateAlertMarkdown(alert, idx + 1);
    });
  }

  // Recommendations
  markdown += '## 📋 Recommendations\n\n';
  markdown += generateRecommendations(grouped);

  return markdown;
}

/**
 * Generate markdown for single alert
 */
function generateAlertMarkdown(alert, index) {
  let markdown = `### ${index}. ${alert.name}\n\n`;
  markdown += `**ID:** ${alert.pluginid}\n`;
  markdown += `**Confidence:** ${alert.confidence}\n`;
  markdown += `**CWE:** ${alert.cweid || 'N/A'}\n\n`;

  if (alert.description) {
    markdown += `**Description:**\n${alert.description}\n\n`;
  }

  if (alert.solution) {
    markdown += `**Solution:**\n${alert.solution}\n\n`;
  }

  if (alert.reference) {
    markdown += `**Reference:**\n${alert.reference}\n\n`;
  }

  if (alert.instances && alert.instances.length > 0) {
    markdown += `**Affected URLs:**\n`;
    alert.instances.slice(0, 5).forEach(instance => {
      markdown += `- \`${instance.uri}\`\n`;
      if (instance.method) {
        markdown += `  - Method: ${instance.method}\n`;
      }
      if (instance.param) {
        markdown += `  - Parameter: ${instance.param}\n`;
      }
    });
    if (alert.instances.length > 5) {
      markdown += `- ... and ${alert.instances.length - 5} more\n`;
    }
    markdown += '\n';
  }

  return markdown;
}

/**
 * Generate recommendations
 */
function generateRecommendations(grouped) {
  let markdown = '';

  if (grouped.High.length > 0) {
    markdown += '### 🔴 High Priority\n';
    markdown += '- **Immediate Action Required:** Address all high-severity issues before deployment\n';
    markdown += '- **Timeline:** Fix within 24 hours\n';
    markdown += '- **Review:** Security team review required\n\n';
  }

  if (grouped.Medium.length > 0) {
    markdown += '### 🟠 Medium Priority\n';
    markdown += '- **Action Required:** Address medium-severity issues in current sprint\n';
    markdown += '- **Timeline:** Fix within 1 week\n';
    markdown += '- **Review:** Code review recommended\n\n';
  }

  if (grouped.Low.length > 0) {
    markdown += '### 🟡 Low Priority\n';
    markdown += '- **Action Recommended:** Address low-severity issues in future sprints\n';
    markdown += '- **Timeline:** Fix within 2 weeks\n\n';
  }

  markdown += '### General Recommendations\n';
  markdown += '1. **Security Training:** Ensure team is trained on OWASP Top 10\n';
  markdown += '2. **Code Review:** Implement security-focused code reviews\n';
  markdown += '3. **Testing:** Add security tests to CI/CD pipeline\n';
  markdown += '4. **Monitoring:** Monitor for security issues in production\n';
  markdown += '5. **Updates:** Keep dependencies updated\n\n';

  return markdown;
}

/**
 * Generate GitHub PR comment
 */
function generatePRComment(report) {
  const alerts = report.site[0]?.alerts || [];
  const grouped = groupAlertsBySeverity(alerts);
  const highCount = grouped.High.length;
  const mediumCount = grouped.Medium.length;

  let comment = '## 🔒 Security Scan Results\n\n';

  if (highCount === 0 && mediumCount === 0) {
    comment += '✅ **No security issues found!**\n\n';
  } else {
    comment += '⚠️ **Security issues detected:**\n\n';
    if (highCount > 0) {
      comment += `- 🔴 **${highCount} High severity** issue(s)\n`;
    }
    if (mediumCount > 0) {
      comment += `- 🟠 **${mediumCount} Medium severity** issue(s)\n`;
    }
  }

  comment += `- 🟡 **${grouped.Low.length} Low severity** issue(s)\n`;
  comment += `- ℹ️ **${grouped.Informational.length} Informational** issue(s)\n\n`;

  comment += '[View detailed report](./zap-findings.md)\n';

  return comment;
}

/**
 * Check if scan failed
 */
function shouldFail(report) {
  const alerts = report.site[0]?.alerts || [];
  const grouped = groupAlertsBySeverity(alerts);
  
  const failSeverityLevel = CONFIG.severityLevels[CONFIG.failOnSeverity];
  
  for (const [severity, level] of Object.entries(CONFIG.severityLevels)) {
    if (level >= failSeverityLevel && grouped[severity].length > 0) {
      return true;
    }
  }
  
  return false;
}

/**
 * Main execution - Enhanced with filtering and escalation
 */
function main() {
  console.log('📊 Parsing OWASP ZAP Report (Enhanced v2.0)...\n');

  // Parse report
  const report = parseZapReport(CONFIG.inputFile);
  console.log(`✅ Report parsed successfully`);

  // Get raw alerts
  const rawAlerts = report.site[0]?.alerts || [];
  const totalRaw = rawAlerts.length;
  console.log(`📋 Total raw alerts: ${totalRaw}`);

  // Apply false positive filtering
  console.log('\n🔍 Filtering false positives...');
  const filteredAlerts = filterFalsePositives(rawAlerts);
  const falsePositivesFiltered = totalRaw - filteredAlerts.length;
  console.log(`   Filtered out: ${falsePositivesFiltered} false positives`);

  // Apply severity escalation
  console.log('\n⬆️  Applying severity escalation rules...');
  const escalatedAlerts = applySeverityEscalation(filteredAlerts);
  const alertsEscalated = escalatedAlerts.filter(a => a.escalated).length;
  console.log(`   Escalated: ${alertsEscalated} alerts`);

  // Update report with processed alerts
  report.site[0].alerts = escalatedAlerts;
  const totalFiltered = escalatedAlerts.length;

  // Statistics
  const stats = {
    totalRaw,
    totalFiltered,
    falsePositivesFiltered,
    alertsEscalated
  };

  console.log('\n📈 Final Statistics:');
  console.log(`   Total Alerts (Raw): ${stats.totalRaw}`);
  console.log(`   False Positives Filtered: ${stats.falsePositivesFiltered}`);
  console.log(`   Alerts Escalated: ${stats.alertsEscalated}`);
  console.log(`   Final Alert Count: ${stats.totalFiltered}\n`);

  // Generate markdown
  const markdown = generateMarkdownReport(report, stats);
  fs.writeFileSync(CONFIG.outputFile, markdown);
  console.log(`✅ Markdown report generated: ${CONFIG.outputFile}`);

  // Generate PR comment
  const prComment = generatePRComment(report);
  fs.writeFileSync(CONFIG.prCommentFile, prComment);
  console.log(`✅ PR comment generated: ${CONFIG.prCommentFile}`);

  // Check if should fail
  const grouped = groupAlertsBySeverity(escalatedAlerts);

  if (grouped.Critical && grouped.Critical.length > 0) {
    console.error(`\n❌ Security scan FAILED - ${grouped.Critical.length} CRITICAL severity issues found`);
    process.exit(1);
  }

  const failed = shouldFail(report);

  if (failed) {
    console.error(`\n❌ Security scan FAILED - ${CONFIG.failOnSeverity} severity issues found`);
    process.exit(1);
  } else {
    console.log(`\n✅ Security scan PASSED`);
    process.exit(0);
  }
}

// Run
main();


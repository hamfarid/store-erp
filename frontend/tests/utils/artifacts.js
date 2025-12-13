import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ARTIFACTS_ROOT = path.resolve(__dirname, '..', '..', '..', 'artifacts');

function ensureArtifactsDirs() {
  const dirs = [
    ARTIFACTS_ROOT,
    path.join(ARTIFACTS_ROOT, 'screenshots'),
  ];
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
}

export function artifactPath(name) {
  ensureArtifactsDirs();
  return path.join(ARTIFACTS_ROOT, name);
}

export async function writeJsonArtifact(name, data) {
  const target = artifactPath(name);
  const payload = {
    generatedAt: new Date().toISOString(),
    ...data,
  };
  const json = JSON.stringify(payload, null, 2);
  await fs.promises.writeFile(target, json, 'utf-8');
  return target;
}

export async function saveScreenshot(page, name) {
  ensureArtifactsDirs();
  const safeName = name.replace(/[^a-z0-9-_]+/gi, '_');
  const target = path.join(ARTIFACTS_ROOT, 'screenshots', `${safeName}.png`);
  await page.screenshot({ path: target, fullPage: true });
  return target;
}

export async function runDbSchemaSnapshot() {
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
  const scriptPath = path.resolve(__dirname, '..', '..', '..', 'backend', 'db_schema_snapshot.py');
  return new Promise((resolve) => {
    const child = spawn(pythonCmd, [scriptPath], {
      stdio: 'inherit',
    });
    child.on('close', () => resolve());
    child.on('error', () => resolve());
  });
}


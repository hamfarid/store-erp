import { spawn } from 'node:child_process';
import { existsSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const FRONTEND_PORT = Number(process.env.E2E_FRONTEND_PORT ?? 5505);
const BACKEND_PORT = Number(process.env.E2E_BACKEND_PORT ?? 5506);

const isWindows = process.platform === 'win32';
const npmCmd = isWindows ? 'npm.cmd' : 'npm';

function firstExistingPath(paths) {
  for (const p of paths) {
    if (p && existsSync(p)) return p;
  }
  return null;
}

const configuredPython = (process.env.E2E_PYTHON || '').trim();

const pythonCmd =
  configuredPython ||
  firstExistingPath([
    resolve('.venv/Scripts/python.exe'),
    resolve('.venv311/Scripts/python.exe'),
    resolve('.venv/bin/python'),
  ]) ||
  (isWindows ? 'python' : 'python3');

function prefix(stream, label) {
  stream?.on('data', (chunk) => {
    process.stdout.write(`[${label}] ${chunk.toString()}`);
  });
}

function toSqliteUrl(absolutePath) {
  // SQLAlchemy expects forward slashes even on Windows.
  const posixPath = absolutePath.replaceAll('\\', '/');
  return `sqlite:///${posixPath}`;
}

const backendInstanceDir = resolve('backend', 'instance');
mkdirSync(backendInstanceDir, { recursive: true });
const backendDbUrl = toSqliteUrl(resolve(backendInstanceDir, 'e2e.db'));

function spawnProcess(label, command, args, env) {
  const mergedEnv = { ...process.env, ...env };
  let child;
  try {
    child = spawn(command, args, {
      env: mergedEnv,
      shell: isWindows,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
  } catch (err) {
    console.error(`[${label}] spawn failed`);
    console.error(`[${label}] command: ${String(command)}`);
    console.error(`[${label}] args: ${JSON.stringify(args)}`);
    console.error(`[${label}] err:`, err);
    throw err;
  }

  prefix(child.stdout, label);
  prefix(child.stderr, label);

  child.on('exit', (code, signal) => {
    if (signal) {
      console.error(`[${label}] exited with signal ${signal}`);
      return;
    }
    if (code && code !== 0) {
      console.error(`[${label}] exited with code ${code}`);
      process.exitCode = code;
    }
  });

  return child;
}

const backend = spawnProcess(
  'backend',
  pythonCmd,
  ['backend/wsgi.py'],
  {
    DATABASE_URL: backendDbUrl,
    PORT: String(BACKEND_PORT),
    // Bind IPv4 explicitly to avoid Windows `localhost` resolving to IPv6 (::1)
    // while the Flask dev server is only listening on IPv4.
    HOST: '127.0.0.1',
  }
);

const frontend = spawnProcess(
  'frontend',
  npmCmd,
  ['--prefix', 'frontend', 'run', 'dev'],
  {
    PORT: String(FRONTEND_PORT),
    // Force the frontend to hit the spawned backend via IPv4.
    VITE_API_URL: `http://127.0.0.1:${BACKEND_PORT}`,
    VITE_BACKEND_URL: `http://127.0.0.1:${BACKEND_PORT}`,
  }
);

function shutdown() {
  // Best-effort termination; Playwright will send SIGTERM.
  backend.kill('SIGTERM');
  frontend.kill('SIGTERM');
}

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);

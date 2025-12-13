import { spawn } from 'child_process';
import { promisify } from 'util';
import { exec } from 'child_process';
import process from 'node:process';

const execAsync = promisify(exec);
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

let backendProcess = null;

async function isPortInUse(port) {
  try {
    const { stdout } = await execAsync(`netstat -ano | findstr :${port}`);
    return stdout.includes('LISTENING');
  } catch {
    return false;
  }
}

async function waitForBackend(port, maxAttempts = 60) {
  console.log(`⏳ Waiting for backend to start on port ${port}...`);
  
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const response = await fetch(`http://localhost:${port}/api/health`);
      if (response.ok) {
        console.log(`✅ Backend health check passed! (attempt ${i + 1}/${maxAttempts})`);
        
        // Wait additional time for database initialization
        console.log('⏳ Waiting for database initialization...');
        await sleep(3000);
        
        // Verify auth endpoint is accessible
        try {
          const authTest = await fetch(`http://localhost:${port}/api/auth/status`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
          });
          console.log(`ℹ️ Auth endpoint status: ${authTest.status} ${authTest.statusText}`);
        } catch (authError) {
          console.warn('⚠️ Auth endpoint test failed:', authError.message);
        }
        
        console.log('✅ Backend initialization complete!');
        return true;
      }
    } catch (error) {
      // Backend not ready yet, log progress every 10 attempts
      if ((i + 1) % 10 === 0) {
        console.log(`⏳ Still waiting... (attempt ${i + 1}/${maxAttempts})`);
      }
    }
    await sleep(1000);
  }
  
  console.error('❌ Backend failed to respond after 60 seconds');
  return false;
}

export default async function globalSetup() {
  console.log('🚀 Starting global test setup...');
  
  // Check if backend is already running
  const backendPort = 5002;
  const alreadyRunning = await isPortInUse(backendPort);
  
  if (alreadyRunning) {
    console.log('✅ Backend already running on port 5002');
    // Verify it's responding
    const ready = await waitForBackend(backendPort, 5);
    if (ready) {
      return;
    }
    console.log('⚠️ Port in use but backend not responding. Attempting to start new instance...');
  }
  
  // Start the backend server
  console.log('🐍 Starting Flask backend server...');
  
  const backendPath = process.platform === 'win32' 
    ? '..\\backend'
    : '../backend';
  
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
  
  backendProcess = spawn(pythonCmd, ['app.py'], {
    cwd: backendPath,
    env: {
      ...process.env,
      PORT: '5002',
      FLASK_ENV: 'development',
      PYTHONUNBUFFERED: '1'
    },
    stdio: ['ignore', 'pipe', 'pipe'],
    shell: true,
    detached: false
  });
  
  // Log backend output for debugging
  backendProcess.stdout.on('data', (data) => {
    const output = data.toString();
    if (output.includes('Running on') || output.includes('✅')) {
      console.log(`[Backend] ${output.trim()}`);
    }
  });
  
  backendProcess.stderr.on('data', (data) => {
    const output = data.toString();
    // Only log errors, not warnings
    if (output.includes('ERROR') || output.includes('CRITICAL')) {
      console.error(`[Backend Error] ${output.trim()}`);
    }
  });
  
  backendProcess.on('error', (error) => {
    console.error('❌ Failed to start backend:', error.message);
  });
  
  // Wait for backend to be ready
  const ready = await waitForBackend(backendPort);
  
  if (!ready) {
    console.error('❌ Backend failed to start within timeout period');
    if (backendProcess) {
      backendProcess.kill();
    }
    throw new Error('Backend server failed to start');
  }
  
  // Store the process ID for cleanup
  if (backendProcess && backendProcess.pid) {
    process.env.BACKEND_PID = backendProcess.pid.toString();
  }
  
  console.log('✅ Global setup complete!');
}

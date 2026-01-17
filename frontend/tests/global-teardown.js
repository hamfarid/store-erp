import { execSync } from 'child_process';

export default async function globalTeardown() {
  console.log('🧹 Running global test teardown...');
  
  // Get the backend PID if it was stored
  const backendPid = process.env.BACKEND_PID;
  
  if (backendPid) {
    console.log(`🛑 Stopping backend process (PID: ${backendPid})...`);
    
    try {
      if (process.platform === 'win32') {
        // Windows: kill process tree
        execSync(`taskkill /F /T /PID ${backendPid}`, { stdio: 'ignore' });
      } else {
        // Unix: kill process
        execSync(`kill ${backendPid}`, { stdio: 'ignore' });
      }
      console.log('✅ Backend stopped successfully');
    } catch (error) {
      console.log('⚠️ Backend process may have already stopped');
    }
  }
  
  // Also kill any remaining Python processes running app.py (cleanup)
  try {
    if (process.platform === 'win32') {
      execSync('taskkill /F /IM python.exe /FI "WINDOWTITLE eq app.py*"', { stdio: 'ignore' });
    }
  } catch {
    // Ignore errors - process may not exist
  }
  
  console.log('✅ Teardown complete!');
}

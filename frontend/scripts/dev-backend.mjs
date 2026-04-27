import { execFileSync, spawn } from "child_process";
import { existsSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const backendRoot = join(__dirname, "..", "..", "backend");
const winPython = join(backendRoot, "venv", "Scripts", "python.exe");
const unixPython = join(backendRoot, "venv", "bin", "python");

let python;
if (existsSync(winPython)) {
  python = winPython;
} else if (existsSync(unixPython)) {
  python = unixPython;
} else {
  console.error(
    "No virtualenv found at backend/venv. From the repo root, run: cd backend && python -m venv venv",
  );
  process.exit(1);
}

try {
  execFileSync(python, ["-c", "import uvicorn"], { stdio: "pipe" });
} catch {
  console.error(
    "The backend venv is missing dependencies (e.g. uvicorn).\n" +
      "You may have run `pip install` with global Python. Install into the venv instead:\n" +
      `  cd backend\n` +
      `  ${installHint}\n`,
  );
  process.exit(1);
}

const child = spawn(
  python,
  [
    "-m",
    "uvicorn",
    "app.main:app",
    "--reload",
    "--host",
    "0.0.0.0",
    "--port",
    "8000",
  ],
  { cwd: backendRoot, stdio: "inherit" },
);

child.on("exit", (code) => {
  process.exit(code ?? 0);
});

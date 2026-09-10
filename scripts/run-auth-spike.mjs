// ============================================================
// IMPORT ONLY BUILT-IN MODULES; NEVER INSTALL FROM THIS LAUNCHER.
// ============================================================
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";

// ============================================================
// DERIVE FIXED PATHS FROM THIS FILE, NOT FROM REQUEST PARAMETERS.
// ============================================================
const webDirectory = fileURLToPath(new URL("../apps/web/", import.meta.url));
const nextCli = fileURLToPath(new URL("../node_modules/next/dist/bin/next", import.meta.url));

// ============================================================
// BUILD A LOOPBACK-ONLY PLAN WITHOUT STARTING A SERVER ON IMPORT.
// THIS IS A LOCAL DEVELOPMENT LAUNCHER, NOT A NETWORK FIREWALL.
// ============================================================
export function makeAuthSpikeLaunchPlan(environment, extraArguments) {
  // ========================================================
  // REJECT OVERRIDES, PRODUCTION, AND CI BEFORE SERVER STARTUP.
  // ========================================================
  if (
    extraArguments.length !== 0 ||
    (environment.NODE_ENV !== undefined && environment.NODE_ENV !== "development") ||
    (environment.CI !== undefined && environment.CI !== "" && environment.CI !== "false")
  ) {
    // ====================================================
    // USE A FIXED ERROR WITHOUT ECHOING ENVIRONMENT VALUES.
    // ====================================================
    throw new Error("AUTH_SPIKE_LAUNCH_CONFIGURATION_DENIED");
  }
  // ========================================================
  // BIND EXPLICITLY TO LOCALHOST AND FAIL IF PORT 3000 IS BUSY.
  // ========================================================
  return {
    executable: process.execPath,
    arguments: [nextCli, "dev", "--hostname", "localhost", "--port", "3000"],
    directory: webDirectory,
    environment: {
      ...environment,
      NODE_ENV: "development",
      NEXT_TELEMETRY_DISABLED: "1",
      BETTER_AUTH_TELEMETRY: "0",
      BETTER_AUTH_TELEMETRY_DEBUG: "0",
      AJAS_AUTH_SPIKE_LOOPBACK_LAUNCH: "1",
    },
  };
}

// ============================================================
// RUN ONLY AFTER AN EXPLICIT DEVELOPER COMMAND, NEVER ON IMPORT.
// THIS BATCH DOES NOT CONFIGURE OR ENABLE GOOGLE AUTHENTICATION.
// ============================================================
function main() {
  // ========================================================
  // STOP WITHOUT PRINTING RAW STARTUP EXCEPTIONS.
  // ========================================================
  try {
    // ====================================================
    // REQUIRE THE ALREADY-INSTALLED NEXT.JS EXECUTABLE.
    // ====================================================
    if (!existsSync(nextCli)) {
      throw new Error("AUTH_SPIKE_NEXT_EXECUTABLE_MISSING");
    }
    // ====================================================
    // BUILD THE FIXED PLAN AND LAUNCH WITHOUT A SHELL.
    // ====================================================
    const plan = makeAuthSpikeLaunchPlan(process.env, process.argv.slice(2));
    const result = spawnSync(plan.executable, plan.arguments, {
      cwd: plan.directory,
      env: plan.environment,
      stdio: "inherit",
      shell: false,
    });
    // ====================================================
    // RETURN A FAILURE CODE WHEN THE CHILD CANNOT START.
    // ====================================================
    if (result.error) {
      process.stderr.write("AUTH_SPIKE_SERVER_START_FAILED\n");
      return 1;
    }
    // ====================================================
    // PRESERVE THE ACTUAL SERVER EXIT WITHOUT INVENTING SUCCESS.
    // ====================================================
    return result.status ?? 1;
  } catch {
    // ====================================================
    // NO ENVIRONMENT VALUE OR RAW EXCEPTION ENTERS STDERR.
    // ====================================================
    process.stderr.write("AUTH_SPIKE_LAUNCH_DENIED\n");
    return 1;
  }
}

// ============================================================
// DO NOT EXECUTE MAIN WHEN TESTS IMPORT THE PLAN FUNCTION.
// ============================================================
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exitCode = main();
}

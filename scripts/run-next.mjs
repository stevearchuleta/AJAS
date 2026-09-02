import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const nextCli = fileURLToPath(new URL("../node_modules/next/dist/bin/next", import.meta.url));
const nextArguments = process.argv.slice(2);

const result = spawnSync(process.execPath, [nextCli, ...nextArguments], {
  env: {
    ...process.env,
    NEXT_TELEMETRY_DISABLED: "1",
  },
  stdio: "inherit",
});

if (result.error) {
  throw result.error;
}

process.exit(result.status ?? 1);

import { readFileSync } from "node:fs";

import {
  parseApprovedFactsSnapshot,
  parseSavedPostingFixture,
  parseSourcePolicy,
  parseStage1FixtureCommand,
  runStage1VerticalSlice,
  stablePrettyJson,
} from "../packages/core/src/index.js";

const fixtureRoot = new URL("../tests/fixtures/stage1/", import.meta.url);

function readJson(filename: string): unknown {
  return JSON.parse(readFileSync(new URL(filename, fixtureRoot), "utf8")) as unknown;
}

const result = runStage1VerticalSlice({
  command: parseStage1FixtureCommand(readJson("vertical-slice-command.synthetic.json")),
  facts: parseApprovedFactsSnapshot(readJson("approved-applicant-facts.synthetic.json")),
  policy: parseSourcePolicy(readJson("greenhouse-greenhouse.source-policy.json")),
  fixture: parseSavedPostingFixture(readJson("greenhouse-greenhouse-8073203.saved.json")),
});

process.stdout.write(stablePrettyJson(result));

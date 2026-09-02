import { readFileSync } from "node:fs";

import {
  parseApprovedFactsSnapshot,
  parseSavedPostingFixture,
  parseSourcePolicy,
  parseStage1FixtureCommand,
  type Stage1VerticalSliceInput,
} from "../../packages/core/src/index.js";

const fixtureRoot = new URL("../fixtures/stage1/", import.meta.url);

function readJson(filename: string): unknown {
  return JSON.parse(readFileSync(new URL(filename, fixtureRoot), "utf8")) as unknown;
}

export function loadStage1VerticalSliceInput(): Stage1VerticalSliceInput {
  return {
    command: parseStage1FixtureCommand(readJson("vertical-slice-command.synthetic.json")),
    facts: parseApprovedFactsSnapshot(readJson("approved-applicant-facts.synthetic.json")),
    policy: parseSourcePolicy(readJson("greenhouse-greenhouse.source-policy.json")),
    fixture: parseSavedPostingFixture(readJson("greenhouse-greenhouse-8073203.saved.json")),
  };
}

export function cloneStage1Input(input = loadStage1VerticalSliceInput()): Stage1VerticalSliceInput {
  return structuredClone(input);
}

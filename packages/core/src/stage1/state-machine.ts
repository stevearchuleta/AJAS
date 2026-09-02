import type { SliceState } from "./contracts.js";
import { Stage1ValidationError } from "./contracts.js";

const ALLOWED_TRANSITIONS = new Map<SliceState | null, SliceState>([
  [null, "DISCOVERED"],
  ["DISCOVERED", "SCREENED"],
  ["SCREENED", "SELECTED"],
  ["SELECTED", "PREPARING"],
  ["PREPARING", "READY_FOR_REVIEW"],
]);

export function assertSliceTransition(priorState: SliceState | null, newState: SliceState): void {
  if (ALLOWED_TRANSITIONS.get(priorState) !== newState) {
    throw new Stage1ValidationError(
      "INVALID_STATE_TRANSITION",
      `transition ${priorState ?? "NONE"} -> ${newState} is not allowed`,
    );
  }
}

export function buildSliceStateHistory(): readonly SliceState[] {
  const states: SliceState[] = [];
  let priorState: SliceState | null = null;

  for (const state of [
    "DISCOVERED",
    "SCREENED",
    "SELECTED",
    "PREPARING",
    "READY_FOR_REVIEW",
  ] as const) {
    assertSliceTransition(priorState, state);
    states.push(state);
    priorState = state;
  }

  return states;
}

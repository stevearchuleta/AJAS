export const AUTONOMOUS_TERMINAL_STATE = "READY_FOR_REVIEW" as const;

export const PROHIBITED_EMPLOYER_ACTIONS = Object.freeze([
  "EMPLOYER_AUTHENTICATION",
  "EMPLOYER_FORM_ENTRY",
  "EMPLOYER_FILE_UPLOAD",
  "EMPLOYER_ATTESTATION",
  "EMPLOYER_COMMUNICATION",
  "EMPLOYER_SUBMISSION",
] as const);

export type ProhibitedEmployerAction = (typeof PROHIBITED_EMPLOYER_ACTIONS)[number];

export function isProhibitedEmployerAction(action: string): action is ProhibitedEmployerAction {
  return PROHIBITED_EMPLOYER_ACTIONS.some((prohibitedAction) => prohibitedAction === action);
}

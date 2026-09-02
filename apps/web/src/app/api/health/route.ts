export async function GET() {
  return Response.json({
    service: "ajas-web",
    status: "ok",
    autonomousTerminalState: "READY_FOR_REVIEW",
    employerSystemCapability: false,
  });
}

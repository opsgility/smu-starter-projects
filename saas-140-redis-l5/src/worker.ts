// Lumen Trail event worker — SAAS-140 Lesson 5 starter.
//
// Minimal scaffold. In Lesson 5 the student directs Claude Code to:
//   - Decouple the signup handler via Redis PUBLISH / SUBSCRIBE.
//   - See the "listener down → event lost" failure mode of pub/sub.
//   - Upgrade to Redis Streams with consumer groups so events survive consumer downtime.
//   - Optionally add a pub/sub ping for low-latency hybrid delivery.
//
// Open the exercises in the right pane of the lab for the step-by-step directives.

async function main() {
  console.log("[worker] started — see the SAAS-140 Lesson 5 exercises for the directives to paste into Claude Code");
  await new Promise(() => {});
}

main().catch((err) => {
  console.error("[worker] fatal", err);
  process.exit(1);
});

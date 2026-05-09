/**
 * Lesson 18 — OpenTelemetry initialization stub.
 *
 * TODO (Task 2): uncomment the NodeSDK setup below, import this file at the
 * VERY TOP of src/server.ts (before the McpServer and Express imports — the
 * Node SDK must be started before any instrumented module is required), and
 * confirm spans appear in your local OTel collector / Jaeger.
 *
 * Why import-order matters: @opentelemetry/auto-instrumentations-node patches
 * `http`, `fetch`, `pg`, `better-sqlite3`, etc. by hooking into Node's module
 * loader. Modules that were loaded BEFORE the SDK started running will not be
 * instrumented. Putting `import "./otel.js";` as the first line of server.ts
 * guarantees correct ordering.
 *
 * Reference: the FastMCP 3.0 + OTel pattern this is modeled on, brought to TS.
 */

// import { NodeSDK } from "@opentelemetry/sdk-node";
// import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";
// import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";
// import { trace, type Tracer } from "@opentelemetry/api";

// const SERVICE_NAME = process.env.OTEL_SERVICE_NAME ?? "claude-mcp-lesson18-observability";
// const OTLP_ENDPOINT = process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? "http://localhost:4318";

// const sdk = new NodeSDK({
//   serviceName: SERVICE_NAME,
//   traceExporter: new OTLPTraceExporter({
//     url: `${OTLP_ENDPOINT}/v1/traces`,
//   }),
//   instrumentations: [
//     getNodeAutoInstrumentations({
//       // The fs instrumentation is noisy in dev; skip it.
//       "@opentelemetry/instrumentation-fs": { enabled: false },
//     }),
//   ],
// });

// sdk.start();

// export const tracer: Tracer = trace.getTracer(SERVICE_NAME);

// process.on("SIGTERM", () => {
//   sdk.shutdown().finally(() => process.exit(0));
// });

// export { sdk };

// Until Task 2 is implemented, export a no-op tracer-like shim so server.ts
// can import a stable surface without errors.
export const tracer = {
  startActiveSpan: <T>(_name: string, fn: (span: { end: () => void }) => T): T => {
    return fn({ end: () => undefined });
  },
};

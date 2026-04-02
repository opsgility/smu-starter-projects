// TODO: Task 3 — Implement the MonitoringDashboard class
//
// recordProcessing(documentId, latencyMs, success, error):
//   - Increment documents_processed or documents_failed
//   - Track error category if failure
//   - Add to throughput_window with timestamp
//   - Prune throughput_window to last 60 seconds
//
// recordComponentHealth(component, status, responseTimeMs):
//   - Store: { status, response_time_ms, last_check } per component
//   - status values: "healthy", "degraded", "down"
//
// recordEscalation(escalation):
//   - Push to metrics.escalations
//
// getSnapshot(): return metrics summary
//   - uptime_seconds, total_processed, total_failed, error_rate
//   - avg_latency_ms, throughput_per_minute
//   - errors_by_category, component_health
//   - active_escalations (last 5 min), total_escalations
//
// printDashboard(): formatted console output of getSnapshot()

class MonitoringDashboard {
  constructor() {
    this.metrics = {
      documents_processed: 0,
      documents_failed: 0,
      total_latency_ms: 0,
      errors_by_category: {},
      throughput_window: [],
      component_health: {},
      escalations: []
    };
    this.startTime = Date.now();
    // TODO: initialize additional state as needed
  }

  recordProcessing(documentId, latencyMs, success, error = null) {
    // TODO: implement
  }

  recordComponentHealth(component, status, responseTimeMs) {
    // TODO: implement
    this.metrics.component_health[component] = {
      status,
      response_time_ms: responseTimeMs,
      last_check: new Date().toISOString()
    };
  }

  recordEscalation(escalation) {
    this.metrics.escalations.push(escalation);
  }

  getSnapshot() {
    // TODO: implement
    const total = this.metrics.documents_processed + this.metrics.documents_failed;
    const uptimeMs = Date.now() - this.startTime;

    return {
      uptime_seconds: Math.round(uptimeMs / 1000),
      total_processed: this.metrics.documents_processed,
      total_failed: this.metrics.documents_failed,
      error_rate: total > 0 ? (this.metrics.documents_failed / total * 100).toFixed(1) + "%" : "0%",
      avg_latency_ms: total > 0 ? Math.round(this.metrics.total_latency_ms / total) : 0,
      throughput_per_minute: this.metrics.throughput_window.length,
      errors_by_category: this.metrics.errors_by_category,
      component_health: this.metrics.component_health,
      active_escalations: this.metrics.escalations.filter(
        e => Date.now() - new Date(e.timestamp).getTime() < 300000
      ).length,
      total_escalations: this.metrics.escalations.length
    };
  }

  printDashboard() {
    const snap = this.getSnapshot();
    console.log("\n====== DocStream Monitoring Dashboard ======");
    console.log(`Uptime: ${snap.uptime_seconds}s`);
    console.log(`Processed: ${snap.total_processed} | Failed: ${snap.total_failed} | Error Rate: ${snap.error_rate}`);
    console.log(`Avg Latency: ${snap.avg_latency_ms}ms | Throughput: ${snap.throughput_per_minute}/min`);
    console.log(`\nErrors by Category:`);
    for (const [cat, count] of Object.entries(snap.errors_by_category)) {
      console.log(`  ${cat}: ${count}`);
    }
    console.log(`\nComponent Health:`);
    for (const [comp, health] of Object.entries(snap.component_health)) {
      console.log(`  ${comp}: ${health.status} (${health.response_time_ms}ms)`);
    }
    console.log(`\nEscalations: ${snap.active_escalations} active / ${snap.total_escalations} total`);
    console.log("=============================================\n");
  }
}

module.exports = { MonitoringDashboard };

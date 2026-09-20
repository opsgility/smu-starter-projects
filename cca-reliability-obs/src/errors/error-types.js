// TODO: Task 1 — Define the four error categories and error factory
//
// ErrorCategory: { TRANSIENT, VALIDATION, RESOURCE, FATAL }
//   TRANSIENT: rate limits, network timeouts — auto-retry
//   VALIDATION: bad input, schema mismatch — fix input and retry
//   RESOURCE: missing document, DB down — may need human intervention
//   FATAL: unrecoverable — stop processing, escalate immediately
//
// DocStreamError(category, code, message, context):
//   Properties: category, code, message, context, timestamp, id (unique)
//   toJSON(): returns { id, category, code, message, context, timestamp,
//                       retryable (true for TRANSIENT/VALIDATION), escalate (true for FATAL) }
//
// Errors factory:
//   rateLimited(retryAfter): TRANSIENT, code "RATE_LIMITED"
//   classificationFailed(docId, reason): VALIDATION, code "CLASSIFICATION_FAILED"
//   documentNotFound(docId): RESOURCE, code "DOCUMENT_NOT_FOUND"
//   pipelineCorrupted(stage, reason): FATAL, code "PIPELINE_CORRUPTED"

const ErrorCategory = {
  TRANSIENT: "transient",
  VALIDATION: "validation",
  RESOURCE: "resource",
  FATAL: "fatal"
};

class DocStreamError {
  constructor(category, code, message, context = {}) {
    this.category = category;
    this.code = code;
    this.message = message;
    this.context = context;
    this.timestamp = new Date().toISOString();
    this.id = `err-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    // TODO: add any additional initialization
  }

  toJSON() {
    // TODO: implement
    return {
      id: this.id,
      category: this.category,
      code: this.code,
      message: this.message,
      context: this.context,
      timestamp: this.timestamp,
      retryable: this.category === ErrorCategory.TRANSIENT || this.category === ErrorCategory.VALIDATION,
      escalate: this.category === ErrorCategory.FATAL
    };
  }
}

const Errors = {
  rateLimited: (retryAfter) => new DocStreamError(
    ErrorCategory.TRANSIENT, "RATE_LIMITED",
    `Rate limit exceeded. Retry after ${retryAfter}ms.`,
    { retry_after_ms: retryAfter }
  ),

  classificationFailed: (docId, reason) => new DocStreamError(
    ErrorCategory.VALIDATION, "CLASSIFICATION_FAILED",
    `Failed to classify document ${docId}: ${reason}`,
    { document_id: docId }
  ),

  documentNotFound: (docId) => new DocStreamError(
    ErrorCategory.RESOURCE, "DOCUMENT_NOT_FOUND",
    `Document ${docId} not found in store.`,
    { document_id: docId }
  ),

  pipelineCorrupted: (stage, reason) => new DocStreamError(
    ErrorCategory.FATAL, "PIPELINE_CORRUPTED",
    `Pipeline corruption at ${stage}: ${reason}`,
    { stage }
  )
};

module.exports = { ErrorCategory, DocStreamError, Errors };

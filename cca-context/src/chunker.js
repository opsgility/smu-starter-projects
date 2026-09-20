// TODO: Task 1 — Implement chunkDocument(text, options)
//
// Split a long document into overlapping chunks to avoid losing context at boundaries.
// Options (with defaults):
//   maxChunkSize: 3000 characters per chunk
//   overlapSize: 300 characters of overlap between chunks
//   preserveBoundaries: true — try to split at paragraph boundaries (\n\n)
//
// Each chunk object:
//   { index, text, start_offset, end_offset, has_overlap }
//
// Algorithm:
//   1. Start at position 0
//   2. Set end = min(position + maxChunkSize, text.length)
//   3. If preserveBoundaries and not at end: look for last \n\n before end (must be > 50% through chunk)
//   4. Push chunk with the slice
//   5. Advance: position = end - overlapSize (but prevent infinite loop for tiny docs)

function chunkDocument(text, options = {}) {
  const {
    maxChunkSize = 3000,
    overlapSize = 300,
    preserveBoundaries = true
  } = options;

  const chunks = [];
  let position = 0;

  // TODO: implement chunking loop

  return chunks;
}

module.exports = { chunkDocument };

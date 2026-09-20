// TODO: Task 2 — Implement the DocumentStore class
//
// addDocument(doc): assign next ID, set created_at and status, store in Map, return ID
// getDocument(id): return document or null
// updateDocument(id, updates): merge updates with existing doc, set updated_at, return boolean
// search({ query, category, status, limit }): filter and return up to limit documents
// getPipelineStats(): return { total, byStatus, byCategory }

class DocumentStore {
  constructor() {
    this.documents = new Map();
    this.nextId = 1;
    // TODO: initialize additional state as needed
  }

  addDocument(doc) {
    // TODO: implement
    const id = this.nextId++;
    this.documents.set(id, {
      ...doc,
      id,
      created_at: new Date().toISOString(),
      status: doc.status || "queued"
    });
    return id;
  }

  getDocument(id) {
    return this.documents.get(id) || null;
  }

  updateDocument(id, updates) {
    // TODO: implement — merge updates, set updated_at, return true/false
    const doc = this.documents.get(id);
    if (!doc) return false;
    Object.assign(doc, updates, { updated_at: new Date().toISOString() });
    return true;
  }

  search({ query, category, status, limit = 20 }) {
    // TODO: implement filtering
    let results = Array.from(this.documents.values());
    if (category) results = results.filter(d => d.category === category);
    if (status) results = results.filter(d => d.status === status);
    if (query) {
      const q = query.toLowerCase();
      results = results.filter(d =>
        d.title.toLowerCase().includes(q) || (d.content || "").toLowerCase().includes(q)
      );
    }
    return results.slice(0, limit);
  }

  getPipelineStats() {
    // TODO: implement
    const docs = Array.from(this.documents.values());
    const byStatus = {};
    const byCategory = {};
    for (const d of docs) {
      byStatus[d.status] = (byStatus[d.status] || 0) + 1;
      if (d.category) byCategory[d.category] = (byCategory[d.category] || 0) + 1;
    }
    return { total: docs.length, byStatus, byCategory };
  }
}

module.exports = { DocumentStore };

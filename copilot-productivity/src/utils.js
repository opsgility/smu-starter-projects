// Undocumented utility functions - need JSDoc documentation
function formatDate(d) { const dt = new Date(d); return `${dt.getFullYear()}-${String(dt.getMonth()+1).padStart(2,'0')}-${String(dt.getDate()).padStart(2,'0')}`; }
function truncateText(t, m) { return t.length <= m ? t : t.substring(0, m - 3) + '...'; }
function generateSlug(t) { return t.toLowerCase().trim().replace(/[^\w\s-]/g, '').replace(/[\s_-]+/g, '-').replace(/^-+|-+$/g, ''); }
function formatRelativeTime(d) { const now = new Date(); const diff = now - new Date(d); const days = Math.floor(diff / 86400000); if (days === 0) return 'today'; if (days === 1) return 'yesterday'; if (days < 7) return `${days} days ago`; if (days < 30) return `${Math.floor(days/7)} weeks ago`; return `${Math.floor(days/30)} months ago`; }
function isValidPriority(p) { return ['low','medium','high','critical'].includes(p); }
module.exports = { formatDate, truncateText, generateSlug, formatRelativeTime, isValidPriority };

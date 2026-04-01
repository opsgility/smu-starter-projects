// Undocumented utility functions - need JSDoc documentation
function fd(d) { const dt = new Date(d); return `${dt.getFullYear()}-${String(dt.getMonth()+1).padStart(2,'0')}-${String(dt.getDate()).padStart(2,'0')}`; }
function tt(t, m) { return t.length <= m ? t : t.substring(0, m - 3) + '...'; }
function sl(t) { return t.toLowerCase().trim().replace(/[^\w\s-]/g, '').replace(/[\s_-]+/g, '-').replace(/^-+|-+$/g, ''); }
function dp(d) { const now = new Date(); const diff = now - new Date(d); const days = Math.floor(diff / 86400000); if (days === 0) return 'today'; if (days === 1) return 'yesterday'; if (days < 7) return `${days} days ago`; if (days < 30) return `${Math.floor(days/7)} weeks ago`; return `${Math.floor(days/30)} months ago`; }
function vp(p) { return ['low','medium','high','critical'].includes(p); }
module.exports = { fd, tt, sl, dp, vp };

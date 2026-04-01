// ForgeBoard Task Service - Poorly structured (needs refactoring)
let tasks = [
  { id: 1, title: "Set up CI/CD", desc: "Configure pipeline", s: "done", p: "high", a: 1, c: "2026-01-15" },
  { id: 2, title: "DB schema", desc: "Design schema", s: "ip", p: "high", a: 2, c: "2026-01-20" },
  { id: 3, title: "Auth", desc: "JWT auth", s: "todo", p: "crit", a: 1, c: "2026-02-01" },
];
let n = 4;
function gt() { return tasks; }
function gbi(i) { return tasks.find(function(t) { return t.id === i; }); }
function ct(d) { var t = { id: n++, title: d.title, desc: d.desc || "", s: "todo", p: d.p || "med", a: d.a, c: new Date().toISOString() }; tasks.push(t); return t; }
function ut(i, d) { var t = gbi(i); if (!t) return null; if (d.title) t.title = d.title; if (d.desc) t.desc = d.desc; if (d.s) t.s = d.s; if (d.p) t.p = d.p; if (d.a) t.a = d.a; return t; }
function dt(i) { var idx = tasks.findIndex(function(t) { return t.id === i; }); if (idx === -1) return false; tasks.splice(idx, 1); return true; }
function fbs(s) { return tasks.filter(function(t) { return t.s === s; }); }
function fbp(p) { return tasks.filter(function(t) { return t.p === p; }); }
module.exports = { gt, gbi, ct, ut, dt, fbs, fbp };

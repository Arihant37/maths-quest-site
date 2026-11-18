// node test_practice.js : every generator must give a correct answer for its own question, 500 times each.
const GEN = require("./practice.js");
const levels = JSON.parse(require("fs").readFileSync("levels.json", "utf8")).levels.map((l) => l.level);
let bad = 0;
for (const n of levels) {
  if (!GEN[n]) { console.log("level", n, "has no practice generator"); bad++; continue; }
  for (let i = 0; i < 500; i++) {
    const g = GEN[n]();
    let want;
    const d = g.q.match(/^Is (\d+) divisible by (\d+)\?$/);
    const m = g.q.match(/^(\d+) ([×+−]) (\d+)$/);
    if (d) want = +d[1] % +d[2] === 0 ? "yes" : "no";
    else if (m) want = m[2] === "×" ? m[1] * m[3] : m[2] === "+" ? +m[1] + +m[3] : m[1] - m[3];
    if (want !== g.a || (g.kind === "number" && (!Number.isInteger(g.a) || g.a < 0))) { console.log("WRONG level", n, g, "expected", want); bad++; break; }
  }
}
console.log(bad ? "FAILED" : `all ${levels.length} generators OK`);
process.exit(bad ? 1 : 0);

// Practice sums for each level's trick. GEN[level]() returns { q, a, kind } with a ready-made correct answer.
// kind "number": a is a number. kind "yesno": a is "yes" or "no".
// Every level published on the site needs an entry here (test: node test_practice.js).
const ri = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
const mul = (a, b) => ({ q: `${a} × ${b}`, a: a * b, kind: "number" });
const sub = (a, b) => ({ q: `${a} − ${b}`, a: a - b, kind: "number" });
const add = (a, b) => ({ q: `${a} + ${b}`, a: a + b, kind: "number" });

const GEN = {
  1: () => mul(ri(12, 98), 11),
  2: () => mul(2 * ri(6, 49), 5),
  3: () => mul(2 * ri(5, 49) + 1, 5),
  4: () => mul(ri(12, 99), 9),
  5: () => mul(ri(12, 99), 25),
  6: () => add(ri(2, 7) * 10 + ri(6, 9), ri(20, 69)),
  7: () => sub(1000, ri(101, 999)),
  8: () => sub(10000, ri(1001, 9999)),
  9: () => sub(1000, ri(11, 99) * 10),
  10: () => { const k = ri(2, 9); return sub(k * 1000, ri(1000, k * 1000 - 1)); },
  11: () => { const n = ri(1001, 9999); return { q: `100 − ${(n / 100).toFixed(2)}`, a: (10000 - n) / 100, kind: "number" }; }, // money change with decimals
  12: () => { let a; do a = ri(41, 99); while (a % 10 === 9); let b; do b = ri(11, a - 1); while (b % 10 <= a % 10); return sub(a, b); }, // a must not end in 9, or no b could need borrowing
  13: () => { const n = 10 * ri(1, 9) + 5; return mul(n, n); },
  14: () => { const n = 100 * ri(1, 2) + 10 * ri(0, 9) + 5; return mul(n, n); },
  15: () => { const n = ri(51, 59); return mul(n, n); },
  16: () => { const n = ri(41, 49); return mul(n, n); },
  17: () => { const n = ri(101, 109); return mul(n, n); },
  22: () => mul(ri(101, 109), ri(91, 99)),
  23: () => mul(ri(991, 999), ri(991, 999)),
  24: () => mul(ri(1001, 1009), ri(1001, 1009)),
  25: () => mul(ri(41, 59), ri(41, 59)),
  26: () => mul(ri(201, 209), ri(201, 209)),
  27: () => { const t = ri(1, 9), u = ri(1, 9); return mul(10 * t + u, 10 * t + 10 - u); },
  28: () => { const u = ri(1, 9); return mul(80 + u, 90 - u); },
  29: () => { const p = ri(10, 19), u = ri(1, 9); return mul(10 * p + u, 10 * p + 10 - u); },
  30: () => { const t = ri(1, 9), u = ri(1, 9); return mul(10 * t + u, 10 * (10 - t) + u); },
  31: () => mul(ri(12, 98), 99),
  32: () => mul(ri(101, 998), 999),
  34: () => { let x, y, p, q; do { x = ri(1, 3); y = ri(1, 3); p = ri(1, 3); q = ri(1, 3); } while (x * q + y * p > 9); return mul(10 * x + y, 10 * p + q); },
  35: () => mul(ri(21, 49), ri(12, 39)),
  36: () => mul(ri(50, 99), ri(40, 99)),
  37: () => mul(ri(101, 299), ri(11, 39)),
  38: () => mul(ri(101, 199), ri(101, 299)),
  40: () => { const m = ri(30, 98); return mul(m - 2, m + 2); },
  45: () => {
    let n;
    if (Math.random() < 0.5) n = 9 * ri(112, 1111);
    else do n = ri(1000, 9999); while (n % 9 === 0);
    return { q: `Is ${n} divisible by 9?`, a: n % 9 === 0 ? "yes" : "no", kind: "yesno" };
  },
};
if (typeof module !== "undefined") module.exports = GEN;

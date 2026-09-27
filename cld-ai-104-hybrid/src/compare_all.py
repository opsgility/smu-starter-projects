"""Exercise 3 — compare BM25 / vector / RRF-hybrid / hybrid+rerank on 10 mixed queries."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hybrid import bm25_ranking, vector_ranking, rrf_ranking, hybrid_with_rerank, CHUNKS


QUERIES = json.loads((Path(__file__).resolve().parent.parent / "data" / "queries.json").read_text(encoding="utf-8"))


def hit_at_k(ranking_ids: list[int], expected: str, k: int) -> bool:
    return any(CHUNKS[i]["id"] == expected for i in ranking_ids[:k])


def main() -> int:
    print(f"compare_all: {len(QUERIES)} queries x 4 retrievers, P@5\n")
    print(f"{'query':<35} {'type':<12} {'bm25':<6} {'vec':<6} {'hybrid':<8} {'+rerank':<8}")
    print("-" * 85)

    counters = {"bm25": 0, "vec": 0, "hybrid": 0, "hybrid_rerank": 0}
    per_type = {"synonym": {k: 0 for k in counters}, "exact_code": {k: 0 for k in counters},
                "exact_term": {k: 0 for k in counters}}
    per_type_total = {"synonym": 0, "exact_code": 0, "exact_term": 0}

    for q in QUERIES:
        b = bm25_ranking(q["q"])
        v = vector_ranking(q["q"])
        try:
            h = rrf_ranking(q["q"])
            hr = hybrid_with_rerank(q["q"])
        except NotImplementedError:
            print("TODO RRF not filled"); return 1

        b_hit = hit_at_k(b, q["expected"], 5)
        v_hit = hit_at_k(v, q["expected"], 5)
        h_hit = hit_at_k(h, q["expected"], 5)
        hr_hit = hit_at_k(hr, q["expected"], 5)
        for name, hit in [("bm25", b_hit), ("vec", v_hit), ("hybrid", h_hit), ("hybrid_rerank", hr_hit)]:
            if hit:
                counters[name] += 1
                per_type[q["type"]][name] += 1
        per_type_total[q["type"]] += 1

        print(f"{q['q'][:34]:<35} {q['type']:<12} {'✓' if b_hit else '✗':<6} {'✓' if v_hit else '✗':<6} "
              f"{'✓' if h_hit else '✗':<8} {'✓' if hr_hit else '✗':<8}")

    n = len(QUERIES)
    print(f"\nOverall P@5:")
    for name, hits in counters.items():
        print(f"  {name:<16}: {hits}/{n} ({100*hits/n:.0f}%)")

    print(f"\nBy query type:")
    for t, tot in per_type_total.items():
        row = f"  {t:<12} (n={tot}):"
        for name in counters:
            row += f"  {name}={per_type[t][name]}/{tot}"
        print(row)

    return 0


if __name__ == "__main__":
    sys.exit(main())

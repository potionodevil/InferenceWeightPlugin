"""Score free-text answers to the held-out test questions (data/test_questions.jsonl).

Rule: an answer is correct if it contains an accepted alias of every gold part after
normalization (case, curly quotes, hyphens and dashes, thousands separators; numbers match on
digit boundaries; aliases starting with "re:" are regular expressions). Verbatim questions need
the full normalized quote; token recall of the quote is reported too.

Answers file: JSONL, one {"qid": ..., "answer": ...} per line. Missing qids count as wrong.

    python score_answers.py answers.jsonl
    python score_answers.py --selftest    # gold short answers, empty answers, a wrong-entity swap
"""
import argparse
import difflib
import json
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(HERE, "data", "test_questions.jsonl")
TYPES = ["direct", "para", "twohop", "reverse", "verbatim"]


def norm(s):
    s = s.lower().replace("’", "'").replace("‘", "'")
    s = re.sub(r"(?<=\d),(?=\d{3})", "", s)            # 1,840 -> 1840
    s = re.sub(r"[\-‐-―/]", " ", s)                     # hyphens, dashes -> space
    s = re.sub(r"(?<!\d)\.|\.(?!\d)", " ", s)          # keep decimal points only
    s = re.sub(r"[^a-z0-9.&' ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def alias_match(alias, text_n):
    if alias.startswith("re:"):
        return re.search(alias[3:], text_n) is not None
    a = norm(alias)
    pat = r"(?<![a-z0-9])" + re.escape(a)
    if re.fullmatch(r"[0-9.]+", a):
        pat += r"(?![0-9])"
    return re.search(pat, text_n) is not None


def score_groups(answer, groups):
    t = norm(answer)
    return all(any(alias_match(a, t) for a in g) for g in groups)


def norm_words(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("’", "'")).split()


def verbatim_scores(answer, quote):
    a, q = norm_words(answer), norm_words(quote)
    exact = " ".join(q) in " ".join(a)
    sm = difflib.SequenceMatcher(None, q, a, autojunk=False)
    lcs = sum(b.size for b in sm.get_matching_blocks())
    return exact, lcs / max(1, len(q))


def score_item(item, answer):
    if item["type"] == "verbatim":
        exact, rec = verbatim_scores(answer, item["quote"])
        return {"correct": bool(exact), "token_recall": round(rec, 4)}
    return {"correct": bool(score_groups(answer, item["groups"]))}


def load_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def evaluate(items, answers):
    by = defaultdict(list)
    recall = []
    for it in items:
        r = score_item(it, answers.get(it["qid"], ""))
        by[("all", it["type"])].append(r["correct"])
        by[(it["doc"], it["type"])].append(r["correct"])
        by[("all", "overall")].append(r["correct"])
        by[(it["doc"], "overall")].append(r["correct"])
        if "token_recall" in r:
            recall.append(r["token_recall"])
    return by, (sum(recall) / len(recall) if recall else None)


def report(by, recall, title):
    docs = sorted({d for d, _ in by if d != "all"}) + ["all"]
    cols = TYPES + ["overall"]
    print(f"\n{title}\n| doc | " + " | ".join(f"{c} (n={len(by[('all', c)])})" for c in cols) + " |")
    print("|---|" + "---|" * len(cols))
    for d in docs:
        cells = [f"{100 * sum(by[(d, c)]) / len(by[(d, c)]):.1f}" if by[(d, c)] else "-" for c in cols]
        print(f"| {d} | " + " | ".join(cells) + " |")
    if recall is not None:
        print(f"verbatim token recall: {100 * recall:.1f}")


def selftest(items):
    gold = {it["qid"]: it.get("short") or it["groups"][0][0] for it in items}
    report(*evaluate(items, gold), "gold short answers (expect 100)")
    report(*evaluate(items, {}), "empty answers (expect 0)")
    # wrong entity: answer each question with the gold answer of the next question of the same doc
    swap, prev = {}, {}
    for it in items:
        if it["doc"] in prev:
            swap[it["qid"]] = gold[prev[it["doc"]]]
        prev[it["doc"]] = it["qid"]
    report(*evaluate(items, swap), "neighbouring gold answer (direct and para questions of one fact share the answer)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("answers", nargs="?")
    ap.add_argument("--tests", default=TESTS)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    items = load_jsonl(a.tests)
    if a.selftest:
        selftest(items)
        return
    if not a.answers:
        ap.error("give an answers JSONL file or --selftest")
    answers = {r["qid"]: r["answer"] for r in load_jsonl(a.answers)}
    report(*evaluate(items, answers), f"{a.answers}: % correct")


if __name__ == "__main__":
    main()

"""Rank accounts from a CSV. Every rank carries its top-3 reasons. Weights live in weights.yaml."""
import csv, math, pathlib, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
W = yaml.safe_load((ROOT / "scoring/weights.yaml").read_text())
REG = {"healthcare", "legal", "fintech"}
def score(r):
    parts = {}
    users = float(r["flow_users"]) if r.get("flow_users") else 0.0
    emp = float(r["employees"]) if r.get("employees") else 0.0
    if users and emp: parts["penetration"] = W["penetration"] * min(users / emp, 0.5) * 2
    if users: parts["absolute_users"] = W["absolute_users"] * math.log10(users)
    if r.get("has_team_plan") == "false": parts["no_team_plan"] = W["no_team_plan"]
    if r.get("sso_enabled") == "false": parts["no_sso"] = W["no_sso"]
    if r.get("industry") in REG: parts["regulated_industry"] = W["regulated_industry"]
    if r.get("signals"): parts["signal"] = W["signal"]
    reasons = sorted(parts, key=parts.get, reverse=True)[:3]
    return round(sum(parts.values()), 2), reasons
if __name__ == "__main__":
    src = pathlib.Path(sys.argv[1]); rows = list(csv.DictReader(src.open()))
    for r in rows:
        s, why = score(r); r["score"], r["reasons"] = s, ";".join(why)
    rows.sort(key=lambda r: -r["score"])
    n = len(rows)
    for i, r in enumerate(rows): r["tier"] = "A" if i < n * 0.3 else "B" if i < n * 0.6 else "C"
    out = src.with_name(src.stem + "_ranked.csv")
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("wrote", out)

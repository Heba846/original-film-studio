#!/usr/bin/env python3
"""Validate edition20/budget_ledger.json against edition20/flow_jobs.json.

Exit 0 = plan within caps (prints whether spending may start); exit 1 = violation.
Entry schema (append one per Flow generation actually run):
  {"date": "2026-11-05", "job_id": "F01", "pool": "primary|retake|supporting_image",
   "model": "<exact Flow model name>", "outputs": 1, "credits_charged": 10,
   "result_files": ["public/flow/F01.mp4"], "verdict": "approved|rejected|pending"}
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
L = json.loads((ROOT / "edition20/budget_ledger.json").read_text())
J = json.loads((ROOT / "edition20/flow_jobs.json").read_text())["jobs"]
err, warn = [], []
cap, pools, pr = L["cap_credits"], L["pools"], L["pricing"]

if sum(pools.values()) != cap: err.append(f"pools sum {sum(pools.values())} != cap {cap}")
if pr["outputs_per_prompt"] != 1: warn.append("outputs_per_prompt != 1: every job costs more than planned")
per_job = pr["credits_per_output"] * pr["outputs_per_prompt"]
planned_primary = per_job * len(J)
if planned_primary > pools["primary"]:
    err.append(f"planned primary {planned_primary} > pool {pools['primary']}")
ids = [j["job_id"] for j in J]
if len(set(ids)) != len(ids): err.append("duplicate job ids")
# cross-check with the manifest: every job placed on the timeline is budgeted, every budgeted job is placed
M = json.loads((ROOT / "edition20/media_manifest.json").read_text())
flow_shots = {s["shot_id"] for s in M["shots"] if s["kind"] == "flow_job"}
used = {c["shot"] for cuts in M["segment_cuts"].values() for c in cuts if c["shot"] in flow_shots or c["shot"].startswith("F")}
unbudgeted = sorted(used - set(ids))
unplaced = sorted(set(ids) - used)
if unbudgeted: err.append(f"timeline uses unbudgeted jobs: {unbudgeted}")
if unplaced: err.append(f"budgeted jobs never placed: {unplaced}")
if flow_shots != set(ids): err.append("manifest flow_job shots differ from flow_jobs.json")
for b in L.get("batches", []):
    n = sum(1 for j in J if j["batch"] == b["batch"])
    if b.get("jobs") is not None and b["jobs"] != n: err.append(f"batch {b['batch']} lists {b['jobs']} jobs, flow_jobs has {n}")

spent = {"primary": 0, "retake": 0, "supporting_image": 0}
models = set()
for e in L["entries"]:
    if e["pool"] not in spent: err.append(f"unknown pool {e['pool']}"); continue
    spent[e["pool"]] += e["credits_charged"]
    models.add(e["model"])
    if pr["model_name_in_flow"] and e["model"] != pr["model_name_in_flow"] and not e["model"].startswith("(not recorded"):
        err.append(f"{e['job_id']}: model '{e['model']}' differs from pinned '{pr['model_name_in_flow']}' (no auto-upgrade)")
    if e["credits_charged"] != e["outputs"] * pr["credits_per_output"] and not (e["credits_charged"] == 0 and ("refunded" in e.get("verdict", "") or "0 credits" in e.get("verdict", ""))):
        err.append(f"{e['job_id']}: charged {e['credits_charged']} != outputs x price")
    if e["pool"] == "primary" and e["job_id"] not in ids:
        err.append(f"{e['job_id']}: primary spend on a job not in flow_jobs.json")
prim = spent["primary"] + spent["supporting_image"]
planned_retake = sum(r["credits"] for r in L.get("planned_retakes", []))
if spent["retake"] + planned_retake > pools["retakes"]: err.append(f"retakes spent+planned {spent['retake']+planned_retake} > {pools['retakes']}")
total = sum(spent.values())
if prim > pools["primary"]: err.append(f"primary+supporting {prim} > {pools['primary']}")
if spent["retake"] > pools["retakes"]: err.append(f"retakes {spent['retake']} > {pools['retakes']}")
reserve_floor = 0 if L["reserve_released_by_owner"] else pools["reserve_unspent"]
if total > cap - reserve_floor: err.append(f"total {total} breaks into the reserve")
if total > cap: err.append(f"total {total} > cap {cap}")
if len({m for m in models if not m.startswith("(not recorded")}) > 1: err.append(f"more than one model used: {sorted(models)}")

may_spend = pr["confirmed_in_flow_ui"] and pr["model_name_in_flow"] and not err and L.get("flow_status", {}).get("state") not in ("BLOCKED", "VIDEO_UNVERIFIED", "STILL_REVIEW_GATE")
b1 = [j for j in J if j["batch"] == 1]
print(f"Cap {cap} | pools primary {pools['primary']} / retakes {pools['retakes']} / reserve {pools['reserve_unspent']}")
print(f"Price assumed {pr['credits_per_output']} cr/output x {pr['outputs_per_prompt']} output/prompt "
      f"({'CONFIRMED' if pr['confirmed_in_flow_ui'] else 'NOT CONFIRMED in Flow'}; model: {pr['model_name_in_flow'] or 'not recorded'})")
print(f"Planned primary: {len(J)} jobs = {planned_primary} cr | Batch 1: {len(b1)} jobs = {per_job*len(b1)} cr | "
      f"timeline uses {len(used)} jobs, all budgeted: {not unbudgeted}")
print(f"Spent: primary {spent['primary']} + supporting {spent['supporting_image']} + retakes {spent['retake']} = {total} | remaining {cap-total} (of which reserve {pools['reserve_unspent']})")
print(f"Planned retakes: {planned_retake} cr ({', '.join(r['job_id'] for r in L.get('planned_retakes', []))}) of the {pools['retakes']} cr retake pool")
for w in warn: print("WARN:", w)
for e in err: print("ERROR:", e)
acct = L.get("account", {}); obs = L.get("account_observations", [])
if obs:
    floor = acct.get("minimum_untouched_account_credits", 0)
    print(f"Account panel (observed): {obs[-1]['balance_credits']} cr; per-job ledger total {total} cr; "
          f"UI net reduction {acct.get('original_balance_credits', 0) - obs[-1]['balance_credits']} cr -> {L.get('reconciliation', {}).get('status', '')[:14]}")
    if obs[-1]["balance_credits"] < floor: err.append(f"account balance below the {floor}-credit floor")
if L.get("flow_status", {}).get("state") in ("BLOCKED", "VIDEO_UNVERIFIED", "STILL_REVIEW_GATE"): print("FLOW:", L["flow_status"]["detail"])
print("PLAN VALID" if not err else "PLAN INVALID", "| spending authorized by ledger:", "YES" if may_spend else ("NO (" + L["flow_status"].get("state", "") + ": " + L["flow_status"].get("detail", "")[:70] + ")" if L.get("flow_status", {}).get("state") in ("BLOCKED", "VIDEO_UNVERIFIED", "STILL_REVIEW_GATE") else "NO (confirm model + price in Flow first)"))
sys.exit(1 if err else 0)

import pathlib, subprocess, sys, tempfile, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(tempfile.mkdtemp()) / "retrieval.yaml"
subprocess.run([sys.executable, str(ROOT / "scripts/retrieve.py"), str(ROOT / "inputs/questions/approver-core.md"), str(OUT)], check=True)
R = {q["id"]: [c["id"] for c in q["claims_retrieved"]] for q in yaml.safe_load(OUT.read_text(encoding="utf-8"))}
LIB = {r["id"]: r for r in yaml.safe_load((ROOT / "claims/library.yaml").read_text(encoding="utf-8"))}
def test_every_question_has_a_row():
    assert len(R) >= 30
def test_sso_found():  # the miss from the Phase 1 brief
    assert {"saml_sso_growth_enterprise", "sso_saml_enforcement"} <= set(R["q01"])
def test_scim_found():
    assert "scim_provisioning_supported" in R["q02"]
def test_soc2_report_found():
    assert "soc2_type_ii_report" in R["q12"]
def test_residency_found():
    assert "no_data_residency_outside_us" in R["q16"]
def test_both_sides_of_notetaker_baa_conflict():
    assert {"notetaker_works_alongside_baa", "security_notetaker_disabled_baa"} <= set(R["q29"])
def test_no_competitor_claims():
    assert not [c for ids in R.values() for c in ids if LIB[c]["source_id"].startswith(("comp_", "ms_"))]

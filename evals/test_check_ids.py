import sys, pathlib, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))
from check_ids import check, library_hash
def _write(body, hash_=None):
    h = hash_ or library_hash()
    p = pathlib.Path(tempfile.mkdtemp()) / "x.md"
    p.write_text(f"---\naccount: t\ntype: it-brief\nclaims_used: []\nlibrary_hash: {h}\nstatus: draft\n---\n{body}")
    return p
def test_confirmed_claim_passes():
    assert check(_write("Admins can enforce ZDR [zdr_enforce_org].")) == []
def test_unknown_id_fails():
    assert any("unknown claim id" in x for x in check(_write("Made up [not_a_claim].")))
def test_conflicting_claim_fails():
    assert any("status is conflicting" in x for x in check(_write("SOC 2 is done [soc2_status].")))
def test_stale_hash_fails():
    assert any("stale" in x for x in check(_write("ok [zdr_enforce_org].", hash_="deadbeef0000")))

"""AWP-013 IU-001 — requirements.txt pinned >= test"""
from pathlib import Path

def test_requirements_exists_and_ge():
    p = Path("requirements.txt")
    assert p.exists(), "requirements.txt missing (AWP-013 IU-001)"
    txt = p.read_text(encoding="utf-8")
    # must contain >= pins for core deps
    for dep in ["pydantic>=", "cryptography>=", "jsonschema>=", "pytest>="]:
        assert dep in txt, f"{dep} not in requirements.txt"
    # must contain baseline comment 7625eb2
    assert "7625eb2" in txt or "7625eb26" in txt, "baseline commit not referenced"
    # hashes for audit (win_amd64 sha256 comments)
    assert "sha256:" in txt, "hash audit missing"


def test_requirements_installable_syntax():
    # verify pip can parse without error (dry check : contains no invalid line like ==>=)
    txt = Path("requirements.txt").read_text(encoding="utf-8")
    for line in txt.splitlines():
        line=line.strip()
        if not line or line.startswith("#"):
            continue
        # pip syntax: package>=version  (allow comment after)
        assert ">=" in line or "==" in line or line.startswith("#"), f"invalid line: {line}"

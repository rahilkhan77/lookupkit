from pathlib import Path

WEB = Path(__file__).resolve().parents[2] / "web"


def test_required_pages_exist():
    required = [
        "app/page.tsx",
        "app/pricing/page.tsx",
        "app/catalog/page.tsx",
        "app/about/page.tsx",
        "app/contact/page.tsx",
        "app/compare/page.tsx",
        "app/docs/page.tsx",
        "app/playground/page.tsx",
        "app/login/page.tsx",
        "app/signup/page.tsx",
        "app/legal/privacy/page.tsx",
        "app/legal/terms/page.tsx",
        "app/legal/dpa/page.tsx",
        "app/legal/layout.tsx",
        "app/dashboard/page.tsx",
        "middleware.ts",
    ]
    missing = [p for p in required if not (WEB / p).exists()]
    assert missing == []


def test_landing_h1_and_cta():
    landing = (WEB / "app/page.tsx").read_text()
    form = (WEB / "components/WaitlistForm.tsx").read_text()
    assert "Phone, email, IP." in landing
    assert "That’s the kit." in landing or "That's the kit." in landing
    assert "Join the waitlist" in form


def test_legal_draft_banner():
    text = (WEB / "app/legal/layout.tsx").read_text()
    assert "DRAFT" in text

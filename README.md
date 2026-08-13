# Lookupkit

Phone, email, and IP verification for developers. **Lookupkit** is a Keystone product by [Excentia](https://excentia.site), founded by Rahil Khan.

This is not a 1Lookup visual clone. The kit is three lookups, honest `meta.provider` values, and HTTP 501 for skip-trace / people search / transcription — no fabricated person data.

## What’s in the MVP

| Surface | Behavior |
| --- | --- |
| `POST /v1/email` | Syntax, **live DNS MX**, disposable domains. MillionVerifier only if `MILLIONVERIFIER_API_KEY` is set. |
| `POST /v1/phone` | [libphonenumber](https://github.com/daviddrysdale/python-phonenumbers). Carrier is `unknown` when unknown — never a placeholder like “Example Wireless”. Twilio Lookup only if `TWILIO_*` is set. |
| `POST /v1/ip` | [ip-api.com](http://ip-api.com) for public IPs. Private/loopback classified locally. MaxMind only if `MAXMIND_LICENSE_KEY` **and** `MAXMIND_ACCOUNT_ID` are set (web service; we do not download GeoLite databases or accept vendor ToS). |
| Skip-trace / people / transcription | `501 unavailable` |
| Auth | Email/password, bcrypt, httpOnly `lk_session` cookie. `/dashboard/*` is gated. Landing, docs, and pricing are public. |
| Keys | `lk_live_` / `lk_test_`. Hashed at rest. Credits + usage log. |
| Billing | Starter $99 / 20k, Growth $299 / 85k, Pro $799 / 250k, Enterprise $1999 / 1M. Stripe **test** keys only unless `STRIPE_LIVE=1`. No charges without keys. |

## Layout

```
apps/api   FastAPI
apps/web   Next.js App Router (Keystone UI)
docker-compose.yml   Postgres + Redis + api + web
```

SQLite is the default when `DATABASE_URL` is unset. Redis is optional.

## Local run (SQLite)

```bash
cp .env.example .env   # fill SESSION_SECRET; leave vendor keys empty

# API
cd apps/api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Web (another terminal)
cd apps/web
npm install
API_URL=http://localhost:8000 npm run dev
```

Open http://localhost:3000 — the Next.js app proxies `/v1`, `/auth`, `/account`, and `/billing` to the API so the session cookie stays on one origin.

## Docker Compose (Postgres + Redis)

```bash
docker compose up --build
```

- Web: http://localhost:3000
- API: http://localhost:8000
- API docs: http://localhost:8000/docs

## Environment

See `.env.example`. Do not commit secrets.

- Adapters **stay off** when their keys are missing.
- `STRIPE_SECRET_KEY` must be `sk_test_…`. An `sk_live_` key is refused unless `STRIPE_LIVE=1`.
- This repo does not buy domains or sign vendor terms of service.

## Tests

```bash
cd apps/api && pytest -q
```

CI (GitHub Actions) runs API tests and a Next.js production build.

## Brand

Lookupkit / Keystone. Parent: Excentia. Founder: Rahil Khan.

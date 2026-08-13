# Lookupkit

Lookupkit.ai — phone, email, IP verification API (Excentia).

A small, dependency-light HTTP API for validating and classifying phone numbers,
email addresses, and IP addresses. All verification is deterministic and runs
offline (no third-party network calls), which keeps local development and tests
fast and reproducible.

## Requirements

- Node.js >= 20 (Node 22 recommended)
- npm

## Getting started

```bash
npm ci          # install dependencies from the lockfile
npm run dev     # start the dev server with hot reload on http://localhost:3000
```

For a production-style run:

```bash
npm run build   # compile TypeScript to dist/
npm start       # run the compiled server
```

## Scripts

| Script              | Description                                  |
| ------------------- | -------------------------------------------- |
| `npm run dev`       | Start the API with hot reload (`tsx watch`). |
| `npm run build`     | Compile TypeScript into `dist/`.             |
| `npm start`         | Run the compiled server from `dist/`.        |
| `npm run typecheck` | Type-check without emitting.                 |
| `npm run lint`      | Lint the codebase with ESLint.               |
| `npm test`          | Run the Vitest test suite.                   |

The server listens on `PORT` (default `3000`).

## API

### `GET /health`

Health check. Returns `{ "status": "ok", ... }`.

### `POST /v1/verify/phone`

Body: `{ "phone": "+14155552671", "country": "US" }` (`country` is an optional
ISO code used to interpret national-format numbers).

```json
{
  "input": "+14155552671",
  "valid": true,
  "e164": "+14155552671",
  "country": "US",
  "type": "FIXED_LINE_OR_MOBILE",
  "nationalNumber": "4155552671"
}
```

### `POST /v1/verify/email`

Body: `{ "email": "alice@example.com" }`

```json
{
  "input": "alice@example.com",
  "valid": true,
  "normalized": "alice@example.com",
  "local": "alice",
  "domain": "example.com",
  "disposable": false
}
```

### `POST /v1/verify/ip`

Body: `{ "ip": "8.8.8.8" }`

```json
{ "input": "8.8.8.8", "valid": true, "version": 4, "scope": "public" }
```

All endpoints also accept the same fields as query parameters.

## Project layout

```
src/
  app.ts            Express app wiring
  index.ts          Server entry point
  routes/verify.ts  Verification route handlers
  lib/              Verification logic (phone, email, ip)
```

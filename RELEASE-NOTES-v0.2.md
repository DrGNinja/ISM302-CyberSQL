# v0.2 Self-Contained Release Candidate

## Changes from v0.1
- Removed all CDN references from application code.
- Changed SQLite runtime paths to repository-local `vendor/sql.js/` assets.
- Added `.nojekyll` for static GitHub Pages deployment.
- Retained the audited nine-table synthetic cybersecurity SQLite database.
- Added formal GitHub Pages and pre-publication acceptance testing documentation.
- Pinned intended sql.js runtime to 1.14.2.

## Audit performed in build workspace
- Nine expected SQLite tables: PASS.
- `PRAGMA foreign_keys=ON` in audit connection: PASS.
- `PRAGMA foreign_key_check`: PASS (0 violations).
- Application source scan for external HTTP/HTTPS runtime references: PASS (none in application code).
- Application paths point to local `vendor/sql.js/sql-wasm.js` and `.wasm`: PASS.

## Open release-candidate dependency
The build workspace could not retrieve external binary assets because outbound DNS/download access was unavailable. Therefore the official `sql-wasm.js` and `sql-wasm.wasm` 1.14.2 files are not falsely represented as included.

Before GitHub Pages testing, obtain the two official sql.js 1.14.2 distribution files and place them in `vendor/sql.js/`. Then execute `ACCEPTANCE-TEST.md` in full.

This release candidate must not be promoted to v1.0 or linked in Canvas until the acceptance test passes.

## Runtime dependency resolved
The official sql.js v1.14.2 WebAssembly distribution was integrated into `vendor/sql.js/`.

SHA-256:
- `sql-wasm.js`: `f1c84000dbc856c9d87f4f3aabc4d3654bd436165db4be3da13751db3a9c20d7`
- `sql-wasm.wasm`: `38c14f6e379210bc942bdc4ebca44e7bfdb4318ecc1c72ca666a28fdce96670a`
- `cybersql.db`: `8c5c7f3a7654d8ef049865484da7290b91cac1d8a095459947edeffad22f7008`

Automated package audit completed before packaging: SQLite foreign keys enabled in audit connection, `PRAGMA foreign_key_check` returned no rows, nine application tables present, and no application CDN/runtime network references remain.

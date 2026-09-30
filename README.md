# ISM 302 CyberSQL Lab — v0.2 Self-Contained Release Candidate

Browser-based SQLite learning lab for ISM 302 using synthetic cybersecurity data only.

## Student deployment
The intended deployment is GitHub Pages. Students open one web link; they do not install SQLite, Python, VS Code, extensions, or a local database, and they do not need a GitHub account.

All runtime assets must be stored in this repository:
- `index.html`
- `cybersql.db`
- `vendor/sql.js/sql-wasm.js`
- `vendor/sql.js/sql-wasm.wasm`

The application loads the master database into browser memory. Student changes affect only that browser session; reloading/resetting restores the repository copy.

## Required vendor runtime
v0.2 is pinned to **sql.js 1.14.2 (MIT)**. The two official distribution files must be present in `vendor/sql.js/`:
- `sql-wasm.js`
- `sql-wasm.wasm`

Source: official sql.js 1.14.2 distribution/release. Do not substitute a different version without re-running acceptance testing.

## GitHub Pages
1. Upload the complete folder contents to the repository root.
2. Settings → Pages → Deploy from a branch.
3. Select `main` and `/ (root)`.
4. Wait for the Pages URL.
5. Test the URL in an InPrivate/Incognito window before linking it in Canvas.

## Local instructor testing
Because the app fetches the database and WASM assets, serve the folder through HTTP:

```bash
python -m http.server 8000
```

Open `http://localhost:8000`.

## Learning areas in this release candidate
- SQL missions: SELECT, WHERE, NULL, aggregates, GROUP BY/HAVING, JOIN, RBAC, incident correlation
- Schema inspection and many-to-many design exercise
- ERD interpretation exercise
- Controlled SQL-injection defense simulation emphasizing parameterized queries
- Final synthetic incident investigation

## Data safety
All usernames, hostnames, training vulnerability IDs, and events are synthetic. IPv4 addresses use documentation ranges, including 192.0.2.0/24, 198.51.100.0/24, and 203.0.113.0/24.

## Release status
This is a **release candidate**, not yet the student v1.0 release. Publish to Canvas only after every applicable item in `ACCEPTANCE-TEST.md` passes on the GitHub Pages URL.

# ISM 302 CyberSQL v0.2 — Pre-Publication Acceptance Test

Record tester, date, browser/version, device, and GitHub Pages URL.

## Deployment
- [ ] GitHub Pages loads over HTTPS.
- [ ] No GitHub login is required.
- [ ] No software installation or file download is required.
- [ ] Browser developer Network panel shows no runtime dependency on a CDN or other third-party host.
- [ ] `vendor/sql.js/sql-wasm.js` loads from the same GitHub Pages origin.
- [ ] `vendor/sql.js/sql-wasm.wasm` loads from the same GitHub Pages origin.
- [ ] `cybersql.db` loads from the same GitHub Pages origin.

## SQLite integrity
Run in SQL Missions/editor where applicable:

```sql
SELECT sqlite_version();
```
- [ ] Returns an SQLite version.

```sql
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
```
- [ ] Returns exactly the nine application tables.

```sql
PRAGMA foreign_keys;
```
- [ ] Returns `1`.

```sql
PRAGMA foreign_key_check;
```
- [ ] Returns no violation rows.

## Functional tests
- [ ] All 8 SQL missions execute.
- [ ] Each model query produces its audited expected result.
- [ ] Invalid SQL returns an understandable SQLite error and the lab remains usable.
- [ ] Schema challenge validates correctly.
- [ ] ERD challenge validates correctly.
- [ ] ERD relationships match the physical schema.
- [ ] RBAC mission results match source records.
- [ ] Injection Defense shows unsafe concatenation only as a controlled training demonstration.
- [ ] Injection Defense shows parameter binding as the remediation.
- [ ] Final incident clues are recoverable from database records.

## Isolation/reset behavior
- [ ] A data-changing statement changes only the current in-memory browser database.
- [ ] Reload/reset restores the pristine repository database.
- [ ] A second browser/incognito session is unaffected by changes in the first session.

## Data/privacy audit
- [ ] No real student/person names.
- [ ] No Lynn credentials or secrets.
- [ ] No Lynn operational IP addresses or production system identifiers.
- [ ] All scenario identities and security events are synthetic.
- [ ] Documentation-range IP addressing is retained.

## Browser/accessibility check
- [ ] Chrome/Windows.
- [ ] Edge/Windows.
- [ ] Safari/macOS or iPadOS/iOS when available.
- [ ] Narrow/mobile layout does not clip essential controls.
- [ ] Keyboard navigation reaches tabs, editor actions, schema/ERD controls, and injection controls.
- [ ] Visible focus and readable feedback are present.

## External-machine test
- [ ] Tested from a device that did not build the project.
- [ ] Tested while not signed into the repository owner’s GitHub account.

## Release decision
- [ ] PASS — approved to promote to v1.0/student release.
- [ ] HOLD — defects documented and corrected before publication.

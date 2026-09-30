import sqlite3, pathlib
p=pathlib.Path('/mnt/data/ism302-cybersql/cybersql.db')
if p.exists(): p.unlink()
c=sqlite3.connect(p); c.execute('PRAGMA foreign_keys=ON')
c.executescript('''
CREATE TABLE departments(department_id INTEGER PRIMARY KEY, department_name TEXT NOT NULL UNIQUE, business_unit TEXT NOT NULL, risk_level TEXT NOT NULL CHECK(risk_level IN ('Low','Moderate','High')));
CREATE TABLE roles(role_id INTEGER PRIMARY KEY, role_name TEXT NOT NULL UNIQUE, access_level INTEGER NOT NULL CHECK(access_level BETWEEN 1 AND 5), privileged INTEGER NOT NULL CHECK(privileged IN(0,1)));
CREATE TABLE users(user_id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, department_id INTEGER NOT NULL, account_status TEXT NOT NULL CHECK(account_status IN('ACTIVE','DISABLED','LOCKED')), mfa_enabled INTEGER NOT NULL CHECK(mfa_enabled IN(0,1)), created_date TEXT NOT NULL, last_password_change TEXT, FOREIGN KEY(department_id) REFERENCES departments(department_id));
CREATE TABLE user_roles(user_id INTEGER NOT NULL, role_id INTEGER NOT NULL, assigned_date TEXT NOT NULL, PRIMARY KEY(user_id,role_id), FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(role_id) REFERENCES roles(role_id));
CREATE TABLE devices(device_id INTEGER PRIMARY KEY, hostname TEXT NOT NULL UNIQUE, device_type TEXT NOT NULL, operating_system TEXT NOT NULL, department_id INTEGER NOT NULL, ip_address TEXT NOT NULL UNIQUE, patch_status TEXT NOT NULL CHECK(patch_status IN('CURRENT','DUE','OVERDUE')), risk_score INTEGER NOT NULL CHECK(risk_score BETWEEN 0 AND 100), FOREIGN KEY(department_id) REFERENCES departments(department_id));
CREATE TABLE login_events(event_id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, device_id INTEGER, login_timestamp TEXT NOT NULL, source_ip TEXT NOT NULL, source_region TEXT NOT NULL, login_status TEXT NOT NULL CHECK(login_status IN('SUCCESS','FAILED')), failure_reason TEXT, authentication_method TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(device_id) REFERENCES devices(device_id));
CREATE TABLE security_events(event_id INTEGER PRIMARY KEY, device_id INTEGER NOT NULL, event_timestamp TEXT NOT NULL, event_type TEXT NOT NULL, severity TEXT NOT NULL CHECK(severity IN('Low','Medium','High','Critical')), source_ip TEXT NOT NULL, destination_ip TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN('OPEN','CLOSED','INVESTIGATING')), FOREIGN KEY(device_id) REFERENCES devices(device_id));
CREATE TABLE incidents(incident_id INTEGER PRIMARY KEY, security_event_id INTEGER NOT NULL UNIQUE, incident_type TEXT NOT NULL, severity TEXT NOT NULL, opened_date TEXT NOT NULL, closed_date TEXT, status TEXT NOT NULL CHECK(status IN('OPEN','CLOSED','INVESTIGATING')), FOREIGN KEY(security_event_id) REFERENCES security_events(event_id));
CREATE TABLE vulnerabilities(vulnerability_id INTEGER PRIMARY KEY, device_id INTEGER NOT NULL, training_vuln_id TEXT NOT NULL, severity TEXT NOT NULL, risk_score REAL NOT NULL CHECK(risk_score BETWEEN 0 AND 10), discovered_date TEXT NOT NULL, patched INTEGER NOT NULL CHECK(patched IN(0,1)), FOREIGN KEY(device_id) REFERENCES devices(device_id));
''')
c.executemany('INSERT INTO departments VALUES(?,?,?,?)',[(1,'Security Operations','Technology','High'),(2,'Data Analytics','Technology','Moderate'),(3,'Finance','Business','High'),(4,'Human Resources','Business','Moderate'),(5,'Operations','Business','Moderate')])
c.executemany('INSERT INTO roles VALUES(?,?,?,?)',[(1,'Standard User',1,0),(2,'Data Analyst',2,0),(3,'SOC Analyst',3,0),(4,'Database Administrator',5,1),(5,'Security Administrator',5,1),(6,'Finance Manager',3,0)])
users=[(101,'usr_a17',1,'ACTIVE',1,'2025-01-12','2026-08-10'),(102,'usr_b42',2,'ACTIVE',1,'2025-03-04','2026-07-19'),(103,'usr_c08',3,'ACTIVE',1,'2024-11-20','2026-09-01'),(104,'usr_d31',1,'ACTIVE',0,'2025-07-09','2026-03-15'),(105,'usr_e55',4,'DISABLED',1,'2024-05-16','2026-01-10'),(106,'usr_f26',5,'ACTIVE',1,'2025-09-22',None),(107,'svc_db01',1,'ACTIVE',0,'2024-02-01','2025-12-20'),(108,'usr_g63',2,'LOCKED',1,'2026-01-08','2026-08-28')]
c.executemany('INSERT INTO users VALUES(?,?,?,?,?,?,?)',users)
c.executemany('INSERT INTO user_roles VALUES(?,?,?)',[(101,3,'2025-01-12'),(102,2,'2025-03-04'),(103,6,'2024-11-20'),(104,5,'2025-07-09'),(105,1,'2024-05-16'),(106,1,'2025-09-22'),(107,4,'2024-02-01'),(108,2,'2026-01-08')])
dev=[(201,'SOC-WS-01','Workstation','Windows 11',1,'192.0.2.11','CURRENT',22),(202,'DATA-WS-02','Workstation','Windows 11',2,'192.0.2.21','DUE',48),(203,'FIN-SRV-01','Server','Linux',3,'192.0.2.31','OVERDUE',91),(204,'HR-WS-04','Workstation','Windows 11',4,'192.0.2.41','CURRENT',28),(205,'OPS-LT-03','Laptop','macOS',5,'192.0.2.51','DUE',57),(206,'DB-SRV-01','Server','Linux',1,'192.0.2.61','OVERDUE',88)]
c.executemany('INSERT INTO devices VALUES(?,?,?,?,?,?,?,?)',dev)
logins=[]; eid=1001
# normal logins
for uid,did,ip,ts in [(101,201,'198.51.100.10','2026-09-29 09:02:00'),(102,202,'198.51.100.20','2026-09-29 09:11:00'),(103,203,'198.51.100.30','2026-09-29 08:45:00'),(106,205,'198.51.100.50','2026-09-29 10:03:00')]:
 logins.append((eid,uid,did,ts,ip,'US-FL','SUCCESS',None,'MFA')); eid+=1
# planted incident: 5 failures then success for privileged usr_d31 from documentation IP
for minute in range(5):
 logins.append((eid,104,206,f'2026-09-30 02:{9+minute:02d}:00','203.0.113.77','External','FAILED','INVALID_PASSWORD','PASSWORD')); eid+=1
logins.append((eid,104,206,'2026-09-30 02:14:00','203.0.113.77','External','SUCCESS',None,'PASSWORD')); eid+=1
# disabled account attempt
logins.append((eid,105,204,'2026-09-30 03:05:00','203.0.113.88','External','FAILED','ACCOUNT_DISABLED','PASSWORD'))
c.executemany('INSERT INTO login_events VALUES(?,?,?,?,?,?,?,?,?)',logins)
c.executemany('INSERT INTO security_events VALUES(?,?,?,?,?,?,?,?)',[(2001,206,'2026-09-30 02:16:00','PRIVILEGED_LOGIN_ANOMALY','Critical','203.0.113.77','192.0.2.61','INVESTIGATING'),(2002,203,'2026-09-30 02:22:00','UNUSUAL_CONNECTION','High','203.0.113.77','192.0.2.31','OPEN'),(2003,202,'2026-09-29 15:20:00','MALWARE_BLOCKED','Medium','198.51.100.44','192.0.2.21','CLOSED')])
c.executemany('INSERT INTO incidents VALUES(?,?,?,?,?,?,?)',[(3001,2001,'Suspected Account Compromise','Critical','2026-09-30 02:18:00',None,'INVESTIGATING'),(3002,2002,'Suspicious Network Activity','High','2026-09-30 02:25:00',None,'OPEN')])
c.executemany('INSERT INTO vulnerabilities VALUES(?,?,?,?,?,?,?)',[(4001,206,'TRAIN-VULN-001','Critical',9.4,'2026-09-10',0),(4002,206,'TRAIN-VULN-002','High',8.1,'2026-09-12',0),(4003,203,'TRAIN-VULN-003','High',7.8,'2026-09-15',0),(4004,202,'TRAIN-VULN-004','Medium',5.6,'2026-09-20',1)])
c.commit()
print('SQLite',sqlite3.sqlite_version)
print('fk',c.execute('PRAGMA foreign_keys').fetchone()[0], 'fk_check', c.execute('PRAGMA foreign_key_check').fetchall())
print('tables',c.execute("select count(*) from sqlite_master where type='table'").fetchone()[0])
print('incident',c.execute("SELECT u.username, sum(l.login_status='FAILED') failed, sum(l.login_status='SUCCESS') success FROM login_events l JOIN users u USING(user_id) WHERE l.source_ip='203.0.113.77' GROUP BY u.username").fetchall())
c.close()

# Flask Login API — Quick Deploy

1. Create a GitHub repo and push these files.
2. Create a remote MySQL database (use any free provider or your own). Note down host, user, password, and database name.
3. On Render: New → Web Service → Connect your repo.
4. Under Environment, set env vars:
   - DB_HOST
   - DB_USER
   - DB_PASSWORD
   - DB_NAME
   
5. Deploy. After successful deploy you will have a URL like `https://flask-login-api.onrender.com`.
6. Test endpoints:
   - POST `/signup` — JSON: `{ "name":"Aarti", "email":"aarti@example.com", "password":"pass" }`
   - POST `/login` — JSON: `{ "email":"aarti@example.com", "password":"pass" }`
   - POST `/send-otp` — JSON: `{  "email":"aarti@example.com"" }`
   - POST ` /verify-otp` — JSON: `{ "email":"aarti@example.com", "otp": "123456" }`
   
   - POST /send-otp — JSON: { "email": "aarti@example.com" }
   - POST /verify-otp — JSON: { "email": "aarti@example.com", "otp": "123456" }


If your chosen DB provider gives you a `port` separate from host, include it in `DB_HOST` like `host:port`.

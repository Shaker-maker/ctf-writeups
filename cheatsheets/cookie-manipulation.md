# Cookie Manipulation & Exploitation Cheat Sheet

## 📌 What are HTTP Cookies?

HTTP cookies are small pieces of data stored by the browser and sent with every HTTP request to the same domain. They're commonly used for:
- Session management (login state)
- Personalization (user preferences)
- Tracking (analytics, ads)

**Security Risk:** Cookies can be inspected, modified, and stolen if not properly secured.

---

## 🔍 Cookie Inspection Methods

### Method 1: Browser Console
```javascript
// View all cookies
document.cookie

// Split cookies for readability
document.cookie.split(';').forEach(c => console.log(c.trim()))

// Find specific cookie
document.cookie.split(';').find(c => c.includes('session'))

// Get cookie value
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
getCookie('sessionID')
```

### Method 2: DevTools Application/Storage Tab
**Chrome:**
1. Press F12 → Application tab
2. Expand "Cookies" in left sidebar
3. Click on domain
4. View/edit cookies in table

**Firefox:**
1. Press F12 → Storage tab
2. Expand "Cookies"
3. Click on domain
4. View/edit cookies

### Method 3: Network Tab
1. F12 → Network tab
2. Reload page
3. Click on any request
4. Check "Cookies" section in Headers
5. See "Request Cookies" and "Response Cookies"

### Method 4: Command Line (cURL)
```bash
# View response cookies
curl -v http://example.com 2>&1 | grep -i 'set-cookie'

# Send cookies with request
curl -b "session=abc123" http://example.com

# Save cookies to file
curl -c cookies.txt http://example.com

# Use saved cookies
curl -b cookies.txt http://example.com
```

### Method 5: Python
```python
import requests

# Get cookies from response
response = requests.get('http://example.com')
print(response.cookies)

# Access specific cookie
session_cookie = response.cookies.get('session')

# Send cookies with request
cookies = {'session': 'abc123'}
response = requests.get('http://example.com', cookies=cookies)
```

---

## 🍪 Cookie Attributes & Security Flags

### Cookie Attributes

```
Set-Cookie: name=value; Domain=example.com; Path=/; Expires=Wed, 09 Jun 2021 10:18:14 GMT; HttpOnly; Secure; SameSite=Strict
```

| Attribute | Purpose | Security Impact |
|-----------|---------|-----------------|
| `Domain` | Which domain receives cookie | Broader domains = more exposure |
| `Path` | Which paths receive cookie | `/` = all paths |
| `Expires` | When cookie expires | Longer = more risk if stolen |
| `Max-Age` | Seconds until expiration | Alternative to Expires |
| `HttpOnly` | Prevents JavaScript access | ✅ Protects against XSS |
| `Secure` | Only sent over HTTPS | ✅ Protects against sniffing |
| `SameSite` | Cross-site request control | ✅ Protects against CSRF |

### Security Flags Explained

**HttpOnly:**
```javascript
// With HttpOnly: document.cookie won't show this cookie
// Without HttpOnly: Vulnerable to XSS attacks
document.cookie // Won't include HttpOnly cookies
```

**Secure:**
```
// Only transmitted over HTTPS connections
// HTTP requests won't include Secure cookies
```

**SameSite:**
```
Strict  - Never sent in cross-site requests
Lax     - Sent on top-level navigation (clicking links)
None    - Always sent (requires Secure flag)
```

---

## 🎯 Cookie Manipulation Techniques

### 1. Reading Cookies

**Browser Console:**
```javascript
document.cookie
```

**Python:**
```python
import requests
r = requests.get('http://example.com')
print(r.cookies)
```

**cURL:**
```bash
curl -v http://example.com 2>&1 | grep 'Set-Cookie'
```

---

### 2. Setting/Modifying Cookies

**Browser Console:**
```javascript
// Set a cookie
document.cookie = "username=admin"

// Set with attributes
document.cookie = "session=abc123; path=/; max-age=3600"

// Set multiple cookies
document.cookie = "role=admin"
document.cookie = "isAuthenticated=true"
```

**Python:**
```python
import requests

cookies = {'session': 'modified_value'}
r = requests.get('http://example.com', cookies=cookies)
```

**cURL:**
```bash
curl -b "session=abc123;role=admin" http://example.com
```

**Browser Extensions:**
- EditThisCookie (Chrome)
- Cookie-Editor (Chrome/Firefox)
- Cookie Quick Manager (Firefox)

---

### 3. Deleting Cookies

**Browser Console:**
```javascript
// Delete by setting expiration to past
document.cookie = "username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"

// Delete all cookies (loops through)
document.cookie.split(";").forEach(function(c) {
    document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
});
```

**DevTools:**
1. Application/Storage → Cookies
2. Right-click cookie → Delete
3. Or click "Clear all cookies"

---

## 🔓 Common Cookie Vulnerabilities

### 1. Insecure Direct Object Reference (IDOR) via Cookies

**Vulnerable Cookie:**
```
userId=123
```

**Exploit:**
```javascript
// Change to another user's ID
document.cookie = "userId=124"
// Refresh page - might access other user's data
```

**Testing:**
1. Note your user ID in cookies
2. Change it to another ID
3. Check if you can access other users' data

---

### 2. Role/Privilege Escalation

**Vulnerable Cookies:**
```
isAdmin=false
role=user
privilege=0
access_level=guest
```

**Exploits:**
```javascript
document.cookie = "isAdmin=true"
document.cookie = "role=admin"
document.cookie = "privilege=1"
document.cookie = "access_level=admin"
```

**Testing:**
1. Look for role-related cookies
2. Try changing to admin/elevated roles
3. Test if restrictions are bypassed

---

### 3. Session Fixation

**Attack:**
1. Attacker gets a valid session ID
2. Tricks victim into using that session ID
3. Victim logs in with attacker's session
4. Attacker now has authenticated session

**Example:**
```javascript
// Attacker sets their session ID in victim's browser
document.cookie = "PHPSESSID=attacker_session_id"
```

---

### 4. Sensitive Data in Cookies

**Common Sensitive Data:**
- Passwords (even hashed)
- Personal information
- API keys
- Flags (in CTFs!)

**Detection:**
```javascript
// Look for suspicious cookie names
document.cookie.split(';').forEach(c => {
    if (c.includes('password') || c.includes('secret') || c.includes('key')) {
        console.log('Suspicious cookie:', c);
    }
})
```

---

### 5. Encoded/Obfuscated Cookies

**Common Encodings:**

#### Base64
```javascript
// Decode Base64 in browser
atob("dXNlcm5hbWU9YWRtaW4=")
// Output: username=admin

// Encode
btoa("username=admin")
```

```bash
# Decode in terminal
echo "dXNlcm5hbWU9YWRtaW4=" | base64 -d

# Encode
echo "username=admin" | base64
```

#### Hex
```javascript
// Decode hex
function hexToString(hex) {
    return hex.match(/.{1,2}/g)
        .map(byte => String.fromCharCode(parseInt(byte, 16)))
        .join('');
}
hexToString("61646d696e")
// Output: admin
```

#### URL Encoding
```javascript
// Decode
decodeURIComponent("username%3Dadmin")
// Output: username=admin

// Encode
encodeURIComponent("username=admin")
```

#### JWT (JSON Web Tokens)
```javascript
// JWT structure: header.payload.signature
// Decode payload (Base64)
const jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.signature"
const payload = jwt.split('.')[1]
JSON.parse(atob(payload))
```

---

## 🛠️ Cookie Exploitation Workflow

### Step 1: Reconnaissance
```javascript
// View all cookies
console.table(document.cookie.split(';').map(c => {
    const [name, value] = c.trim().split('=');
    return {name, value};
}))

// Check for common vulnerable patterns
const vulnPatterns = ['admin', 'role', 'user', 'id', 'privilege', 'access'];
document.cookie.split(';').forEach(c => {
    vulnPatterns.forEach(pattern => {
        if (c.toLowerCase().includes(pattern)) {
            console.log('Potentially vulnerable cookie:', c);
        }
    });
});
```

### Step 2: Identify Encoding
```javascript
function identifyEncoding(value) {
    // Base64 check
    if (/^[A-Za-z0-9+/]*={0,2}$/.test(value)) {
        try {
            console.log('Possible Base64:', atob(value));
        } catch(e) {}
    }
    
    // Hex check
    if (/^[0-9a-fA-F]+$/.test(value)) {
        console.log('Possible Hex');
    }
    
    // JWT check
    if (value.split('.').length === 3) {
        console.log('Possible JWT');
        try {
            const payload = JSON.parse(atob(value.split('.')[1]));
            console.log('JWT Payload:', payload);
        } catch(e) {}
    }
}

// Test all cookie values
document.cookie.split(';').forEach(c => {
    const value = c.trim().split('=')[1];
    identifyEncoding(value);
});
```

### Step 3: Modification Testing
```javascript
// Save original cookies
const originalCookies = document.cookie;

// Test privilege escalation
const testCookies = [
    "isAdmin=true",
    "role=admin",
    "privilege=9999",
    "access_level=administrator"
];

testCookies.forEach(cookie => {
    document.cookie = cookie;
    console.log('Testing:', cookie);
    // Refresh or make request to test
});

// Restore original
// (requires saving individual cookies properly)
```

### Step 4: Automated Scanning
```python
import requests
from base64 import b64decode

url = "http://example.com"
response = requests.get(url)

# Analyze cookies
for cookie_name, cookie_value in response.cookies.items():
    print(f"\n[*] Cookie: {cookie_name} = {cookie_value}")
    
    # Try Base64 decode
    try:
        decoded = b64decode(cookie_value).decode('utf-8')
        print(f"[+] Base64 decoded: {decoded}")
    except:
        pass
    
    # Check for common vulnerabilities
    vuln_keywords = ['admin', 'role', 'user', 'id', 'privilege']
    if any(keyword in cookie_name.lower() for keyword in vuln_keywords):
        print(f"[!] Potentially vulnerable cookie detected!")
```

---

## 🎯 CTF-Specific Cookie Techniques

### 1. Flag in Cookie Value
```javascript
// Check all cookies for flag pattern
document.cookie.split(';').forEach(c => {
    const [name, value] = c.trim().split('=');
    if (value.match(/[a-zA-Z0-9_]{20,}/)) {
        console.log('Possible flag in:', name);
        console.log('Value:', value);
        // Try decoding
        try { console.log('Base64:', atob(value)); } catch(e) {}
    }
});
```

### 2. Multi-level Encoding
```javascript
// URL → Base64 → Hex
let encoded = "48656c6c6f"; // Hex
let step1 = hexToString(encoded); // "Hello"
let step2 = atob(step1); // Decode if it's Base64
let step3 = decodeURIComponent(step2); // URL decode
```

### 3. Cookie Modification for Access
```javascript
// Common CTF patterns
document.cookie = "authenticated=1"
document.cookie = "admin=true"
document.cookie = "debug=1"
document.cookie = "showFlag=true"
```

### 4. Sequential Cookie Testing
```python
import requests

url = "http://ctf-challenge.com"

# Test different user IDs
for user_id in range(1, 100):
    cookies = {'userId': str(user_id)}
    r = requests.get(url, cookies=cookies)
    if 'flag{' in r.text:
        print(f"[+] Flag found with userId={user_id}")
        print(r.text)
        break
```

---

## 🔒 Defense & Prevention

### Secure Cookie Implementation

```javascript
// BAD - Insecure cookies
document.cookie = "session=abc123"
document.cookie = "role=admin"
document.cookie = "userId=42"

// GOOD - Secure cookies (server-side)
Set-Cookie: session=random_secure_token; HttpOnly; Secure; SameSite=Strict; Max-Age=3600
```

### Best Practices

**1. Use HttpOnly Flag**
```
Set-Cookie: session=token; HttpOnly
```
Prevents JavaScript access (XSS protection)

**2. Use Secure Flag**
```
Set-Cookie: session=token; Secure
```
Only transmitted over HTTPS

**3. Use SameSite Attribute**
```
Set-Cookie: session=token; SameSite=Strict
```
Prevents CSRF attacks

**4. Short Expiration Times**
```
Set-Cookie: session=token; Max-Age=3600
```
Limits exposure window

**5. Validate Server-Side**
```python
# Never trust cookie values
user_id = request.cookies.get('userId')
# Validate against database
user = db.get_user(user_id)
if not user or user.session != request.cookies.get('session'):
    return "Unauthorized"
```

**6. Encrypt Sensitive Data**
```python
# Don't store plaintext
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
encrypted_data = f.encrypt(b"sensitive_data")
# Store encrypted_data in cookie
```

**7. Use Cryptographically Secure Session IDs**
```python
import secrets
session_id = secrets.token_urlsafe(32)
```

---

## 🛠️ Tools for Cookie Analysis

### Browser Extensions
- **EditThisCookie** - Edit cookies easily
- **Cookie-Editor** - Manage cookies
- **Cookie Quick Manager** - Firefox extension

### Command Line Tools
```bash
# cURL
curl -v http://example.com

# HTTPie
http http://example.com

# wget
wget --save-cookies cookies.txt http://example.com
```

### Python Libraries
```python
# requests
import requests
r = requests.get('http://example.com')
print(r.cookies)

# http.cookiejar
import http.cookiejar
import urllib.request
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
```

### Burp Suite
1. Proxy → HTTP History
2. Find request
3. View cookies in Request/Response tabs
4. Repeater → Modify cookies
5. Intruder → Fuzz cookie values

---

## 📚 Quick Reference

### Common Cookie Exploits

| Vulnerability | Cookie Example | Exploit |
|--------------|----------------|---------|
| Privilege Escalation | `role=user` | Change to `role=admin` |
| IDOR | `userId=123` | Change to `userId=124` |
| Auth Bypass | `authenticated=false` | Change to `authenticated=true` |
| Sensitive Data | `password=hash` | Decode/crack the hash |
| Session Fixation | `PHPSESSID=xyz` | Set known session ID |

### Encoding Detection

| Pattern | Likely Encoding |
|---------|----------------|
| `dGVzdA==` | Base64 (ends with =) |
| `74657374` | Hex (only 0-9a-f) |
| `test%20data` | URL encoding (%XX) |
| `eyJhbGc...` | JWT (starts with eyJ) |
| `a:2:{s:4:"name"...` | PHP Serialized |

### Common Decoders

```bash
# Base64
echo "base64string" | base64 -d

# Hex
echo "68656c6c6f" | xxd -r -p

# URL
python3 -c "import urllib.parse; print(urllib.parse.unquote('hello%20world'))"

# JWT
echo "payload_part" | base64 -d
```

---

## 🔗 Resources

### Documentation
- [MDN - HTTP Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [RFC 6265 - HTTP State Management](https://tools.ietf.org/html/rfc6265)
- [OWASP - Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)

### Security Guides
- [OWASP - Testing for Cookies](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/02-Testing_for_Cookies_Attributes)
- [Cookie Security Best Practices](https://owasp.org/www-community/controls/SecureCookieAttribute)

### Tools
- [CyberChef](https://gchq.github.io/CyberChef/) - Encoding/decoding
- [JWT.io](https://jwt.io/) - JWT decoder
- [Burp Suite](https://portswigger.net/burp) - Cookie manipulation

---

**Last Updated:** February 6 2026

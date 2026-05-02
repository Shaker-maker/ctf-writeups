
```markdown
# Timeline Forensics 1 - Disk Analysis

**Platform:** PicoCTF
**Category:** Forensics / Disk Analysis  
**Difficulty:** Medium  
**Date Solved:** 2026-05-02  
**Author:** shaker  

---

## 📋 Challenge Description

A disk image is provided where an attacker used anti-forensics techniques to hide activity.

We must reconstruct the timeline and identify suspicious behavior.

---

## 🔍 Initial Reconnaissance

### First Observations
- Disk image provided
- Goal: reconstruct file system activity timeline

### Tools Used
- Sleuth Kit (`fls`, `mactime`, `icat`)
- Spreadsheet tool

---

## 🎯 Vulnerability Identification

**Goal:** Detect anti-forensics activity via timeline anomalies

---

## 🚀 Exploitation Process

### Step 1: Generate Body File
```bash
fls -r -m / disk_image > bodyfile.txt


### Step 2: Build a Timeline

mactime -b bodyfile.txt -d > timeline.csv


### Step 3: Analyze the Timeline

Open CSV in spreadsheet tool
Filter for MACB events
Look for suspicious activity

Key Finding:

Unexpected creation of .bash_history
Indicates history tampering (anti-forensics)

### Step 4: Suspicious File

Found /etc/chat
Not a normal system file


### Step 5: Extract the FIle
icat disk_image <inode_number>

Output:

Base64 encoded string

### Step 6: Decode the Flag

echo "<base64_string>" | base64 -d



💡 Solution

Decoded output reveals the flag.


📖 Key Learnings
MAC timeline helps reconstruct attacker behavior
.bash_history manipulation indicates anti-forensics
inode extraction is key in disk forensics
🏷️ Tags

#forensics #sleuthkit #timeline #disk-analysis

← Back to Main Index



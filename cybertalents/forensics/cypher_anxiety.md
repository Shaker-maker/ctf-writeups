# Cypher Anxiety - Forensics Challenge

**Platform:** CyberTalents  
**Category:** Forensics / Network Analysis  
**Difficulty:** Medium  
**Date Solved:** 2026-05-02  
**Author:** shaker  

---

## 📋 Challenge Description

An image was leaked from a baby store. The manager needs to identify the image to take action against the responsible employee.

The flag is the **MD5 hash of the leaked image**.

**Files Provided:** ZIP containing PCAP file

---

## 🔍 Initial Reconnaissance

### First Observations
- Extracted ZIP file contained a `.pcap`
- Opened in Wireshark
- Found communication between:
  - 192.168.1.6
  - 192.168.1.100

### Tools Used
- Wireshark
- netcat
- cryptcat

---

## 🎯 Vulnerability Identification

**Suspected Issue:** Encrypted traffic via cryptcat

### Why I Suspected This
- Packet stream contained plaintext chat
- Mention of:
  - cryptcat
  - password: `P@ssawordaya`
  - port: `7070`

---

## 🚀 Exploitation Process

### Step 1: Filter Traffic
tcp.port == 7070




### Step 2: Extract Stream
- Follow TCP Stream in Wireshark
- Save as RAW → `encrypted`

### Step 3: Decrypt Traffic

Terminal 1:
```bash
cryptcat -l -k P@ssawordaya -p 7070 > decrypted


Terminal 2:
nc localhost 7070 < encrypted


💡 Solution

Verify File

file decrypted

Generate Flag

md5sum decrypted

🏁 Flag
3beef06be834f3151309037dde4714ec

📖 Key Learnings

TCP streams can hide file transfers
Always use RAW when extracting binary data
MD5 is used for file fingerprinting
🏷️ Tags

#forensics #pcap #cryptcat #network

← Back to Main Index

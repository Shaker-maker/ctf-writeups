# Digital Forensics Cheat Sheet

## 📌 What is Digital Forensics?

Digital forensics involves analyzing digital artifacts to extract hidden information, recover deleted data, identify file types, detect steganography, and investigate security incidents.

**Common CTF Forensics Categories:**
- File analysis and repair
- Steganography (hidden data)
- Memory dumps
- Network packet analysis
- Disk image analysis
- Metadata extraction

---

## 🔍 File Signature Analysis (Magic Bytes)

### What are Magic Bytes?

Magic bytes (file signatures) are specific byte sequences at the beginning of files that identify the file type. The operating system uses these to determine how to handle the file.

### Common File Signatures

| File Type | Magic Bytes (Hex) | Magic Bytes (ASCII) | Offset |
|-----------|-------------------|---------------------|--------|
| **Images** | | | |
| JPEG | `FF D8 FF` | `ÿØÿ` | 0 |
| PNG | `89 50 4E 47 0D 0A 1A 0A` | `.PNG....` | 0 |
| GIF (87a) | `47 49 46 38 37 61` | `GIF87a` | 0 |
| GIF (89a) | `47 49 46 38 39 61` | `GIF89a` | 0 |
| BMP | `42 4D` | `BM` | 0 |
| TIFF (LE) | `49 49 2A 00` | `II*.` | 0 |
| TIFF (BE) | `4D 4D 00 2A` | `MM.*` | 0 |
| ICO | `00 00 01 00` | `....` | 0 |
| **Documents** | | | |
| PDF | `25 50 44 46` | `%PDF` | 0 |
| PostScript | `25 21 50 53` | `%!PS` | 0 |
| RTF | `7B 5C 72 74 66 31` | `{\rtf1` | 0 |
| DOC | `D0 CF 11 E0 A1 B1 1A E1` | `Ðϱà¡±..` | 0 |
| DOCX/XLSX/PPTX | `50 4B 03 04` | `PK..` | 0 |
| **Archives** | | | |
| ZIP | `50 4B 03 04` | `PK..` | 0 |
| RAR | `52 61 72 21 1A 07` | `Rar!..` | 0 |
| 7z | `37 7A BC AF 27 1C` | `7z¼¯'.` | 0 |
| TAR | `75 73 74 61 72` | `ustar` | 257 |
| GZIP | `1F 8B` | `..` | 0 |
| **Executables** | | | |
| EXE (DOS) | `4D 5A` | `MZ` | 0 |
| ELF | `7F 45 4C 46` | `.ELF` | 0 |
| Mach-O | `FE ED FA CE` | `þíúÎ` | 0 |
| **Audio/Video** | | | |
| MP3 (ID3v2) | `49 44 33` | `ID3` | 0 |
| MP3 | `FF FB` or `FF F3` | `ÿû` | 0 |
| MP4 | `00 00 00 [size] 66 74 79 70` | `....ftyp` | 0 |
| AVI | `52 49 46 46 [size] 41 56 49 20` | `RIFF[...]AVI ` | 0 |
| WAV | `52 49 46 46 [size] 57 41 56 45` | `RIFF[...]WAVE` | 0 |
| **Other** | | | |
| SQLite | `53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33 00` | `SQLite format 3.` | 0 |
| Java Class | `CA FE BA BE` | `Êþº¾` | 0 |

### Checking File Signatures

```bash
# Quick file type check
file filename

# View hex dump (first 32 bytes)
xxd -l 32 filename

# View just magic bytes
head -c 16 filename | xxd

# Search for specific signature
xxd filename | grep "ff d8 ff"
```

---

## 🛠️ Essential Forensics Tools

### File Analysis Tools

#### `file` - Identify File Type
```bash
# Basic usage
file suspicious_file

# Be verbose
file -v suspicious_file

# Check multiple files
file *

# Exclude specific file types from output
file * | grep -v "text"
```

#### `strings` - Extract Printable Text
```bash
# Basic extraction
strings filename

# Minimum string length (e.g., 8 characters)
strings -n 8 filename

# Show offset of strings
strings -t x filename  # Hex offset
strings -t d filename  # Decimal offset

# Extract strings from all sections
strings -a filename

# Encoding options
strings -e s filename  # 7-bit ASCII
strings -e S filename  # 8-bit ASCII
strings -e l filename  # 16-bit little-endian
strings -e b filename  # 16-bit big-endian

# Common CTF usage
strings filename | grep -i "flag"
strings filename | grep -i "password"
strings filename | grep "CTF{"
```

#### `xxd` - Hex Dump
```bash
# Full hex dump
xxd filename

# First N bytes
xxd -l 256 filename

# Specific range (skip 100 bytes, show next 50)
xxd -s 100 -l 50 filename

# Plain hex output (no formatting)
xxd -p filename

# Reverse hex dump (hex to binary)
xxd -r hexdump.txt output.bin

# Custom columns
xxd -c 32 filename  # 32 bytes per line
```

#### `hexedit` - Interactive Hex Editor
```bash
# Open file
hexedit filename

# Common operations:
# - Arrow keys: Navigate
# - Type hex values: Edit
# - Ctrl+X or F2: Save
# - Ctrl+C: Exit without saving
# - Tab: Toggle ASCII/Hex
# - /: Search
```

#### `exiftool` - Metadata Extraction
```bash
# Basic metadata
exiftool image.jpg

# All metadata (including duplicate tags)
exiftool -a image.jpg

# Specific tags
exiftool -Comment -Author image.jpg

# Remove all metadata
exiftool -all= image.jpg

# Extract embedded files
exiftool -b -ThumbnailImage image.jpg > thumbnail.jpg

# Recursively process directory
exiftool -r /path/to/images/

# Output to CSV
exiftool -csv *.jpg > metadata.csv
```

#### `binwalk` - Find Embedded Files
```bash
# Scan for embedded files
binwalk filename

# Extract found files
binwalk -e filename

# Extract with specific depth
binwalk -e -M filename

# Scan for specific signatures
binwalk --signature filename

# Calculate entropy (detect encryption/compression)
binwalk -E filename

# Display results with offset
binwalk -B filename
```

---

## 🖼️ Image Forensics

### Image Analysis Tools

#### `identify` (ImageMagick)
```bash
# Basic info
identify image.jpg

# Verbose output
identify -verbose image.jpg

# Check for hidden data in image dimensions
identify -format "%w x %h" image.jpg
```

#### `pngcheck` - PNG Validation
```bash
# Check PNG integrity
pngcheck image.png

# Verbose output
pngcheck -v image.png

# Check all chunks
pngcheck -c image.png
```

#### `steghide` - Steganography Detection
```bash
# Extract hidden data (with password)
steghide extract -sf image.jpg -p password

# Extract without password
steghide extract -sf image.jpg

# Get info about hidden data
steghide info image.jpg

# Embed data
steghide embed -cf cover.jpg -ef secret.txt -p password
```

#### `zsteg` - PNG/BMP Steganography
```bash
# Analyze PNG/BMP
zsteg image.png

# All detection methods
zsteg -a image.png

# Extract specific channel
zsteg -E 'b1,rgb,lsb,xy' image.png

# Brute force common formats
zsteg --all image.png
```

#### `stegsolve` - Advanced Image Analysis
```bash
# Launch GUI
stegsolve image.png

# Features:
# - Cycle through color planes
# - XOR images
# - Extract LSB data
# - Analyze bit planes
# - Stereo view
```

### LSB (Least Significant Bit) Analysis

```python
#!/usr/bin/env python3
from PIL import Image

# Extract LSB from image
def extract_lsb(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    
    bits = []
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            # Extract LSB from each color channel
            if isinstance(pixel, tuple):
                for value in pixel[:3]:  # RGB only
                    bits.append(str(value & 1))
            else:
                bits.append(str(pixel & 1))
    
    # Convert bits to bytes
    byte_array = []
    for i in range(0, len(bits), 8):
        byte = ''.join(bits[i:i+8])
        byte_array.append(chr(int(byte, 2)))
    
    return ''.join(byte_array)

# Usage
hidden_data = extract_lsb('image.png')
print(hidden_data)
```

---

## 📄 PDF Forensics

### PDF Analysis

```bash
# Extract metadata
exiftool document.pdf

# Extract text
pdftotext document.pdf output.txt

# Extract images
pdfimages document.pdf output_prefix

# Info about PDF structure
pdfinfo document.pdf

# Detailed PDF structure
pdftk document.pdf dump_data

# Search for JavaScript
pdf-parser -s javascript document.pdf

# Extract streams
qpdf --stream-data=uncompress input.pdf output.pdf
```

---

## 🗜️ Archive Forensics

### Working with Archives

```bash
# ZIP
unzip archive.zip
unzip -l archive.zip          # List contents
unzip -P password archive.zip # With password
zipinfo archive.zip           # Detailed info

# RAR
unrar x archive.rar
unrar l archive.rar           # List contents

# 7z
7z x archive.7z
7z l archive.7z               # List contents

# TAR
tar -xvf archive.tar
tar -tf archive.tar           # List contents
tar -xzvf archive.tar.gz      # Extract gzipped tar

# Check for password-protected archives
7z l archive.zip | grep -i encrypted
```

### Brute Force Archives

```bash
# fcrackzip (ZIP passwords)
fcrackzip -D -p /usr/share/wordlists/rockyou.txt archive.zip
fcrackzip -b -c a -l 1-10 archive.zip  # Brute force

# John the Ripper (various formats)
zip2john archive.zip > hash.txt
john hash.txt

# hashcat
hashcat -m 17200 hash.txt wordlist.txt  # ZIP
hashcat -m 13600 hash.txt wordlist.txt  # RAR
```

---

## 💾 Memory Forensics

### Volatility Framework

```bash
# Identify OS profile
volatility -f memory.dmp imageinfo

# List processes
volatility -f memory.dmp --profile=Win7SP1x64 pslist

# Dump process
volatility -f memory.dmp --profile=Win7SP1x64 procdump -p 1234 -D output/

# Network connections
volatility -f memory.dmp --profile=Win7SP1x64 netscan

# Command history
volatility -f memory.dmp --profile=Win7SP1x64 cmdscan
volatility -f memory.dmp --profile=Win7SP1x64 consoles

# Extract files
volatility -f memory.dmp --profile=Win7SP1x64 filescan
volatility -f memory.dmp --profile=Win7SP1x64 dumpfiles -Q 0x000000007e410890 -D output/

# Registry hives
volatility -f memory.dmp --profile=Win7SP1x64 hivelist
volatility -f memory.dmp --profile=Win7SP1x64 printkey -K "Software\Microsoft\Windows\CurrentVersion\Run"
```

---

## 🌐 Network Forensics

### Wireshark / tshark

```bash
# Read pcap file
wireshark capture.pcap

# Command-line analysis
tshark -r capture.pcap

# Filter HTTP traffic
tshark -r capture.pcap -Y "http"

# Extract HTTP objects
tshark -r capture.pcap --export-objects http,output_dir/

# Follow TCP stream
tshark -r capture.pcap -z follow,tcp,ascii,0

# Statistics
tshark -r capture.pcap -q -z io,phs  # Protocol hierarchy
tshark -r capture.pcap -q -z conv,ip # Conversations

# Extract specific fields
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e tcp.port

# Filter examples
tshark -r capture.pcap -Y "tcp.port == 80"
tshark -r capture.pcap -Y "http.request.method == GET"
tshark -r capture.pcap -Y "dns"
```

### Network Miner

```bash
# GUI tool for PCAP analysis
networkminer capture.pcap

# Extracts:
# - Files transferred
# - Images
# - Credentials
# - DNS queries
# - Sessions
```

---

## 🔧 File Carving & Recovery

### Foremost - File Carving

```bash
# Carve files from disk image
foremost -i disk.img -o output/

# Specify file types
foremost -t jpg,png,pdf -i disk.img -o output/

# Configuration file
foremost -c /etc/foremost.conf -i disk.img -o output/
```

### Scalpel - Advanced Carving

```bash
# Edit config first
nano /etc/scalpel/scalpel.conf

# Run scalpel
scalpel disk.img -o output/

# Preview mode (don't extract)
scalpel -p disk.img -o output/
```

### PhotoRec - File Recovery

```bash
# Interactive mode
photorec disk.img

# Features:
# - Recovers 400+ file formats
# - Works on damaged filesystems
# - Can recover from formatted drives
```

---

## 📊 Data Analysis & Conversion

### Base64 Encoding/Decoding

```bash
# Encode
echo "secret data" | base64

# Decode
echo "c2VjcmV0IGRhdGE=" | base64 -d

# From file
base64 file.txt > encoded.txt
base64 -d encoded.txt > decoded.txt

# Python
python3 -c "import base64; print(base64.b64decode(b'c2VjcmV0IGRhdGE=').decode())"
```

### Hex Encoding/Decoding

```bash
# Text to hex
echo "hello" | xxd -p

# Hex to text
echo "68656c6c6f" | xxd -r -p

# Python
python3 -c "print(bytes.fromhex('68656c6c6f').decode())"
```

### Binary/ASCII Conversion

```python
# Binary to ASCII
binary = "01110000 01101001 01100011 01101111"
ascii_text = ''.join(chr(int(b, 2)) for b in binary.split())
print(ascii_text)  # "pico"

# ASCII to binary
text = "pico"
binary = ' '.join(format(ord(c), '08b') for c in text)
print(binary)  # "01110000 01101001 01100011 01101111"
```

### QR Code Analysis

```bash
# Decode QR code from image
zbarimg qrcode.png

# Batch processing
zbarimg *.png

# Python
from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('qrcode.png')
result = decode(img)
print(result[0].data.decode())
```

---

## 🔐 Password & Hash Analysis

### Hash Identification

```bash
# hash-identifier
hash-identifier

# hashid
hashid 'hash_here'

# Common hash types
# MD5: 32 hex characters
# SHA1: 40 hex characters
# SHA256: 64 hex characters
# bcrypt: $2a$, $2b$, $2y$ prefix
```

### Cracking Tools

```bash
# John the Ripper
john hashes.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
john --show hashes.txt

# Hashcat
hashcat -m 0 hashes.txt rockyou.txt  # MD5
hashcat -m 1000 hashes.txt rockyou.txt  # NTLM
hashcat -m 1800 hashes.txt rockyou.txt  # SHA512

# Online tools
# - CrackStation
# - MD5Decrypt
# - HashKiller
```

---

## 🎯 CTF-Specific Techniques

### Common CTF Forensics Patterns

**1. Hidden Data in Images**
```bash
# Check for appended data
tail -c 1000 image.jpg | strings

# Compare file size vs expected
identify -verbose image.jpg | grep filesize
```

**2. Metadata Hiding**
```bash
exiftool image.jpg | grep -i "comment\|description\|usercomment"
```

**3. Multiple Files Concatenated**
```bash
binwalk -e suspicious_file
foremost -i suspicious_file -o output/
```

**4. Modified Extensions**
```bash
# Always check actual file type
file *
```

**5. Base64 in Comments**
```bash
strings file | grep -E '^[A-Za-z0-9+/=]{20,}$' | base64 -d
```

### Forensics Workflow

```
1. File Identification
   ↓
   file filename
   xxd filename | head

2. String Extraction
   ↓
   strings filename | grep -i flag

3. Metadata Analysis
   ↓
   exiftool filename

4. Signature Analysis
   ↓
   binwalk filename

5. Embedded File Extraction
   ↓
   binwalk -e filename
   foremost -i filename

6. Steganography Check
   ↓
   steghide info filename
   zsteg filename

7. Manual Analysis
   ↓
   hexedit filename
   stegsolve filename
```

---

## 📚 Quick Reference

### Common Commands Cheat Sheet

```bash
# File analysis
file filename
strings filename | grep flag
xxd filename | head
exiftool filename
binwalk -e filename

# Image forensics
steghide extract -sf image.jpg
zsteg image.png
stegsolve image.png

# Archive analysis
unzip -l archive.zip
7z l archive.7z
tar -tf archive.tar

# Network analysis
wireshark capture.pcap
tshark -r capture.pcap -Y "http"

# Encoding
echo "data" | base64
echo "ZGF0YQ==" | base64 -d
echo "68656c6c6f" | xxd -r -p

# Password cracking
john hashes.txt
hashcat -m 0 hashes.txt rockyou.txt
```

---

## 🔗 Resources

### Documentation
- [File Signatures Table](https://www.garykessler.net/library/file_sigs.html)
- [Forensics Wiki](https://forensicswiki.xyz/)
- [DFIR Training](https://www.dfir.training/)

### Tools
- [Autopsy](https://www.sleuthkit.org/autopsy/) - Digital forensics platform
- [Volatility](https://www.volatilityfoundation.org/) - Memory forensics
- [Wireshark](https://www.wireshark.org/) - Network analysis
- [Binwalk](https://github.com/ReFirmLabs/binwalk) - Firmware analysis
- [ExifTool](https://exiftool.org/) - Metadata extraction

### CTF Resources
- [CTF Field Guide - Forensics](https://trailofbits.github.io/ctf/forensics/)
- [Digital Forensics CTF Tools](https://github.com/apsdehal/awesome-ctf#forensics)

---

**Last Updated:** February 9, 2026

# File Corruption Challenge - PicoCTF

**Platform:** PicoCTF  
**Category:** Forensics  
**Difficulty:** Easy  
**Date Solved:** February 9, 2026  

---

## 📋 Challenge Description

This file seems broken... or is it? Maybe a couple of bytes could make all the difference. Can you figure out how to bring it back to life?

**Files Provided:** `file` (corrupted image file)

---

## 🔍 Initial Reconnaissance

### First Observations
- Downloaded file has no file extension
- File appears to be corrupted or unreadable
- Challenge hint: "a couple of bytes could make all the difference"

### Tools Used
- `file` - File type identification
- `cat` - View file contents
- `strings` - Extract printable strings
- `exiftool` - Metadata analysis
- `xxd` - Hex dump viewer
- `hexedit` - Hex editor

### Initial Investigation

**Step 1: Check file type**
```bash
file file
```

**Result:**
```
file: data
```

The file is recognized as generic "data" - not identified as any specific format.

**Step 2: View raw contents**
```bash
cat file
```

**Output:**
```
\x��JFIF��C ▒▒ $.' ",#(7),01444'9=82<.342��C ▒2!!22222222222222222222222222222222222222222222222222�� "�� ���}!1AQa"q2��#B��R��$3br� ...
```

**Observation:** The file contains `JFIF` string, which is a JPEG File Interchange Format marker. This suggests it's a corrupted JPEG image.

**Step 3: Extract strings**
```bash
strings file
```

**Key findings:**
- `JFIF` - JPEG identifier
- `$.' ",#(7),01444'9=82<.342` - JPEG quantization table data
- Various other JPEG-related markers

**Step 4: Check metadata**
```bash
exiftool file
```

**Result:**
```
Error : Unknown file type
```

ExifTool cannot identify the file type, confirming corruption.

---

## 🎯 Vulnerability Identification

**Suspected Issue:** Corrupted File Signature (Magic Bytes)

### Why I Suspected This

1. **JFIF string present** - File contains JPEG data internally
2. **File type unrecognized** - Signature likely corrupted
3. **Challenge hint** - "a couple of bytes" suggests magic byte corruption
4. **ExifTool error** - Cannot identify file type

### File Signatures (Magic Bytes)

Every file type has a unique "magic number" at the beginning:

| File Type | Magic Bytes (Hex) | Magic Bytes (ASCII) |
|-----------|-------------------|---------------------|
| JPEG | `FF D8 FF` | Non-printable |
| PNG | `89 50 4E 47` | `.PNG` |
| GIF | `47 49 46 38` | `GIF8` |
| PDF | `25 50 44 46` | `%PDF` |
| ZIP | `50 4B 03 04` | `PK..` |

---

## 🚀 Exploitation Process

### Investigation: Hex Dump Analysis

**Command:**
```bash
xxd file | head
```

**Output:**
```
00000000: 5c78 ffe0 0010 4a46 4946 0001 0100 0001  \x....JFIF......
00000010: 0001 0000 ffdb 0043 0008 0606 0706 0508  .......C........
00000020: 0707 0709 0908 0a0c 140d 0c0b 0b0c 1912  ................
00000030: 130f 141d 1a1f 1e1d 1a1c 1c20 242e 2720  ........... $.' 
00000040: 222c 231c 1c28 3729 2c30 3134 3434 1f27  ",#..(7),01444.'
00000050: 393d 3832 3c2e 3334 32ff db00 4301 0909  9=82<.342...C...
```

### Critical Discovery! 🔍

**First two bytes:** `5C 78`

Looking up ASCII values:
- `5C` = `\` (backslash)
- `78` = `x`

**This is literally the text `\x` instead of actual hex bytes!**

**Correct JPEG signature should be:** `FF D8 FF E0`

**Current file starts with:** `5C 78 FF E0` (`\x` followed by valid JPEG data)

### Root Cause

Someone (or something) replaced the actual hex bytes with their ASCII representation:
- Expected: `FF D8` (actual bytes)
- Got: `\x` (text characters representing hex notation)

This is why the file won't open - the magic bytes are literal text instead of binary data!

---

## 💡 Solution

### Method 1: Using printf and dd (Clean Approach)

```bash
# Replace first 2 bytes with correct JPEG signature, keep rest of file
printf '\xff\xd8' | cat - <(dd if=file bs=1 skip=2) > fixed.jpg
```

**Explanation:**
- `printf '\xff\xd8'` - Output correct JPEG magic bytes
- `dd if=file bs=1 skip=2` - Read original file from byte 3 onwards
- Combine them into `fixed.jpg`


### Method 2: Using hexedit (Interactive)

**Step 1: Open in hex editor**
```bash
hexedit file
```

**Step 2: Navigate and edit**
- Cursor starts at first byte (`5C`)
- Type `FF` - replaces `5C` with `FF`
- Type `D8` - replaces `78` with `D8`

**Step 3: Save changes**
- Press `Ctrl + X` (or `F2`) to save
- Press `Y` to confirm
- File is now fixed!

**Step 4: Verify the fix**
```bash
file file
```

**Should output:**
```
file: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, ...
```

### Verification

```bash
# Check file type
file fixed.jpg
# Output: fixed.jpg: JPEG image data, JFIF standard...

# Check with exiftool
exiftool fixed.jpg
# Should show proper JPEG metadata

# Open the image
xdg-open fixed.jpg
```

### Extracting the Flag

**The image displays text with the flag!**

**Option 1: Visual inspection**
- Open the image
- Read the flag directly

**Option 2: OCR (Optical Character Recognition)**
```bash
# Install tesseract if needed
sudo apt install tesseract-ocr

# Extract text from image
tesseract fixed.jpg output.txt

# View extracted text
cat output.txt
```

### Flag
```
picoCTF{r3st0r1ng_th3_by73s_31cc795d}
```

---

## 📖 Key Learnings

### Technical Concepts

**File Signatures (Magic Bytes):**
- Every file type has a unique identifier at the beginning
- Operating systems use these to determine file type
- Corruption of these bytes makes files unreadable
- File extensions are just hints - magic bytes are authoritative

**JPEG File Structure:**
```
FF D8        - Start of Image (SOI)
FF E0        - JFIF marker
4A 46 49 46  - "JFIF" in ASCII
...          - Image data
FF D9        - End of Image (EOI)
```

**Hex vs ASCII Representation:**
- `FF D8` (hex) = actual binary bytes (255, 216)
- `\x` (ASCII) = text characters representing hex notation (92, 120)
- The file had the **text** `\x` instead of the **bytes** it represents

**Common File Signatures:**
```
JPEG: FF D8 FF
PNG:  89 50 4E 47 0D 0A 1A 0A
GIF:  47 49 46 38 (37|39) 61    (GIF87a or GIF89a)
PDF:  25 50 44 46                (%PDF)
ZIP:  50 4B 03 04                (PK..)
EXE:  4D 5A                      (MZ)
```

### Forensics Techniques Learned

1. **File Type Identification**
   - Use `file` command for quick identification
   - Check file signatures with hex editors
   - Extract strings to find embedded identifiers

2. **Hex Analysis**
   - `xxd` for hex dump viewing
   - `hexedit` for interactive hex editing
   - Understanding hex vs ASCII representation

3. **File Repair**
   - Identify correct magic bytes
   - Replace corrupted bytes
   - Verify repair with multiple tools

4. **Data Extraction**
   - Visual inspection
   - OCR for text extraction
   - Metadata analysis

### Tools Comparison

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `file` | Identify file type | First step in analysis |
| `strings` | Extract printable text | Find embedded data/hints |
| `xxd` | View hex dump | Analyze file structure |
| `hexedit` | Edit hex values | Repair corrupted files |
| `exiftool` | View metadata | Extract hidden information |
| `binwalk` | Find embedded files | Steganography/hidden data |

---



## 🎓 Recommendations for Similar Challenges

**When encountering corrupted files:**

1. **Check file type**
   ```bash
   file suspicious_file
   ```

2. **If type is unknown, examine hex dump**
   ```bash
   xxd suspicious_file | head -n 20
   ```

3. **Look for recognizable patterns**
   - JFIF → JPEG
   - PNG → PNG image
   - %PDF → PDF document
   - PK → ZIP archive

4. **Compare with known good signatures**
   - Research correct magic bytes for suspected file type
   - Use online resources like [Wikipedia - List of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures)

5. **Extract strings for clues**
   ```bash
   strings suspicious_file | head -n 50
   ```

6. **Check metadata if possible**
   ```bash
   exiftool suspicious_file
   ```

7. **Repair and verify**
   - Fix magic bytes
   - Verify with `file` command
   - Try opening the file

**Red Flags Indicating Magic Byte Corruption:**

- File won't open despite having correct extension
- `file` command returns "data" instead of specific type
- Hex dump shows text characters where binary is expected
- ExifTool returns "Unknown file type" error
- Strings reveal file type markers (JFIF, PNG, etc.)

---

## 💻 Useful Commands Reference

### File Analysis
```bash
# Identify file type
file filename

# Extract strings
strings filename

# Hex dump (first 20 lines)
xxd filename | head -n 20

# Metadata
exiftool filename

# Search for embedded files
binwalk filename
```

### Hex Editing
```bash
# Interactive hex editor
hexedit filename

# View specific bytes
xxd -l 32 filename  # First 32 bytes

# Search for hex pattern
xxd filename | grep "ff d8"
```

### File Repair
```bash
# Replace first N bytes
printf '\xff\xd8' | cat - <(dd if=file bs=1 skip=2) > fixed.jpg

# Copy from specific offset
dd if=input.bin of=output.bin bs=1 skip=10
```

### Text Extraction
```bash
# OCR from image
tesseract image.jpg output.txt

# Extract text from PDF
pdftotext document.pdf

# Strings with minimum length
strings -n 8 filename
```

---

## 🔗 References & Resources

### Documentation
- [JPEG File Format - Wikipedia](https://en.wikipedia.org/wiki/JPEG)
- [List of File Signatures](https://en.wikipedia.org/wiki/List_of_file_signatures)
- [JFIF Specification](https://www.w3.org/Graphics/JPEG/jfif3.pdf)

### Forensics Resources
- [Digital Forensics - File Signatures](https://www.garykessler.net/library/file_sigs.html)
- [Forensics Wiki - File Formats](https://forensicswiki.xyz/wiki/index.php?title=File_Formats)

### Tools
- [xxd Man Page](https://linux.die.net/man/1/xxd)
- [Hexedit](https://github.com/pixel/hexedit)
- [ExifTool](https://exiftool.org/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Binwalk](https://github.com/ReFirmLabs/binwalk)

---

## 🏷️ Tags

`#forensics` `#file-corruption` `#magic-bytes` `#jpeg` `#hex-editing` `#file-signatures` `#picoctf` `#easy`

---

**[← Back to Main Index](../../README.md)**

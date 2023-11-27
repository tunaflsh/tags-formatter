# Tags Formatter

## Overview
This script processes KoroTagger output and formats it for YouTube timestamps.

## Usage
```
tagsformat.py [-h] [-o OUTPUT] [-s [SECONDS]] [-w [LENGTH] | -nw] [filename]
```

### Positional Arguments:
- `filename`: Specifies the file containing tags. If not provided, the script uses clipboard content.

### Options:
- `-h`, `--help`: Show this help message and exit.
- `-o OUTPUT`, `--output OUTPUT`: Specify the output file for formatted timestamps. Defaults to modifying the input file in place.
- `-s [SECONDS]`, `--auto-section [SECONDS]`: Enable automatic sectioning when a time gap of specified seconds is reached. Default is 180 seconds.
- `-w [LENGTH]`, `--wrap [LENGTH]`: Wrap text at specified character length. Default is 50 characters.
- `-nw`, `--no-wrap`: Disable text wrapping.

## Features
- Handles lines without tags as section headings, which can be empty. This is compatible with both KoroTagger output and pre-formatted tags.
- Reformats pre-formatted files to fix inconsistencies.
- Allows customization of formats through constants in the script.

## Customization
Modify these constants in the script to adjust formats:

```python
HEADER = "*· · • • • ✤  TIMESTAMPS  ✤ • • • · ·*"
SECTION_FORMAT = "*[{}]*"
SECTION_INDENT = ("ㅤ┏", "ㅤ┣", "ㅤ┗")
WRAP_INDENT = ("ㅤ┃ㅤㅤㅤ↝ ", "ㅤ ㅤㅤㅤ↝ ")
TAG_FORMAT = "{prefix}{time} {text}"
```

## Examples

### Input File
```
Section 1
start 0m0s
middle 0m10s
end 0m20s

second start 0m30s
Very long text that will be wrapped at 50 characters. 0m40s
second end 0m50s
```

### Result
```
*· · • • • ✤  TIMESTAMPS  ✤ • • • · ·*
*[Section 1]*
ㅤ┏00:00 start
ㅤ┣00:10 middle
ㅤ┗00:20 end
*[]*
ㅤ┏00:30 second start
ㅤ┣00:40 Very long text that will be wrapped at 50
ㅤ┃ㅤㅤㅤ↝ characters.
ㅤ┗00:50 second final end
```

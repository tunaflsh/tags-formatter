# Tags Formatter

## Overview

This script processes [KoroTagger](https://563563.xyz/korotagger/) output and formats it for YouTube timestamps.

## Usage

```python console
tagsformat.py [-h] [-o OUTPUT] [-s [SECONDS]] [-w [LENGTH] | -nw] [filename]
```

### Positional Arguments

- `filename`: Specifies the file containing tags. If not provided, the script uses clipboard content.

### Options

- `-h`, `--help`: Show the help message and exit.
- `-o OUTPUT`, `--output OUTPUT`: Specify the output file for formatted timestamps. Defaults to modifying the input file in place.
- `-s [SECONDS]`, `--auto-section [SECONDS]`: Enable automatic sectioning when a time gap of specified seconds is reached. Default is 180 seconds.
- `-w [LENGTH]`, `--wrap [LENGTH]`: Wrap text at specified character length. Default is 50 characters.
- `-nw`, `--no-wrap`: Disable text wrapping.

## Features

- [x] Handles lines without tags as section headings, which can be empty.
- [x] Automatically splits the tags into sections based on specified time gaps.
- [x] Allows customization of formats through constants in the script.
- [ ] Reformats pre-formatted files to fix inconsistencies.

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

```text
Section 1
start 0m0s
middle 0m10s
end 0m20s

second start 0m30s
Very long text that will be wrapped at 50 characters. 0m40s
second end 0m50s
```

### Result

```text
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

## Similar Projects

- [korotaggertool](https://github.com/kylemsguy/korotaggertool) is a web-based tags editor by [kylemsguy](https://github.com/kylemsguy)

## Acknowledgements

- [KoroTagger](https://github.com/Yarn/korotagger) is a Discord bot to tag live streams. See manual [here](https://563563.xyz/korotagger/).

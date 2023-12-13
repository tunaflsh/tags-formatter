# Tags Formatter

`tagsformat.py` formats [KoroTagger](https://563563.xyz/korotagger/) output ~~or YouTube timestamps~~ in a customizable way. It then returns the formatted text to the console and clipboard.

## Usage

```python console
tagsformat.py [-h] [-s [SECONDS]] [-w [LENGTH] | -nw] input
```

### Positional Arguments

- `input` - file containing timestamps

### Options

- `-h`, `--help` - show the help message and exit
- `-s [SECONDS]`, `--auto-section [SECONDS]` - enable automatic sectioning when a time gap of specified seconds is reached. Default: 180
- `-w [LENGTH]`, `--wrap [LENGTH]` - wrap text at specified character length. Default: 50
- `-nw`, `--no-wrap` - disable text wrapping

## Input File

To specify a section heading, add `# heading` on a new line by itself or `#` for a blank heading. If auto-sectioning `-s` is enabled, those sections will have no heading.

## Custom Formats

Modify these constants in the script to adjust formats:

```python
HEADER = "*· · • • • ✤  TIMESTAMPS  ✤ • • • · ·*"
SECTION_FORMAT = "*[{}]*"
SECTION_INDENT = ("ㅤ┏", "ㅤ┣", "ㅤ┗")
WRAP_INDENT = ("ㅤ┃ㅤㅤㅤ↝ ", "ㅤ ㅤㅤㅤ↝ ")
TAG_FORMAT = "{prefix}{time} {text}"
```

## Examples

```console
$ cat input.txt
# Section 1
start 0m0s
middle 0m10s
end 0m20s
#
second start 0m30s
Very long text that will be wrapped at 50 characters. 0m40s
second end 0m50s
```

```console
$ python tagsformat.py input.txt
*· · • • • ✤  TIMESTAMPS  ✤ • • • · ·*
*[Section 1]*
ㅤ┏00:00 start
ㅤ┣00:10 middle
ㅤ┗00:20 end

ㅤ┏00:30 second start
ㅤ┣00:40 Very long text that will be wrapped at 50
ㅤ┃ㅤㅤㅤ↝ characters.
ㅤ┗00:50 second final end
```

## TODO

- [ ] support YouTube timestamps as input.

## Similar Projects

- [korotaggertool](https://github.com/kylemsguy/korotaggertool) is a web-based tags editor.

## Acknowledgements

- [KoroTagger](https://github.com/Yarn/korotagger) is a Discord bot to tag live streams. See manual [here](https://563563.xyz/korotagger/).

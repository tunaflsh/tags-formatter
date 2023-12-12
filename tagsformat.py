#!/usr/bin/env python
"""
Licensed under the MIT License.
Source: https://github.com/tunaflsh/tags-formatter
"""
import argparse
import io
import re
import textwrap
from itertools import pairwise

import pyperclip

HEADER = "*· · • • • ✤  TIMESTAMPS  ✤ • • • · ·*\n"
SECTION_FORMAT = "\n*[{}]*"
SECTION_INDENT = (
    "ㅤ┣",  # start
    "ㅤ┣",  # middle
    "ㅤ┗",  # end
)
WRAP_INDENT = (
    "ㅤ┃ㅤㅤㅤ↝ ",  # start & middle
    "ㅤ ㅤㅤㅤ↝ ",  # end
)
TAG_FORMAT = "{section_indent}{time} {text}"


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="This script formats KoroTagger output or YouTube timestamps in a"
    "\ncustomizable way. It then returns the formatted text and copies it to"
    "\nthe clipboard.",
    epilog="To customize the formats, adjust the constants in the script:"
    "\n"
    "\n```"
    '\nHEADER = "*· · • • • ✤  TIMESTAMPS  ✤ • • • · ·*"'
    '\nSECTION_FORMAT = "*[{}]*"'
    '\nSECTION_INDENT = ("ㅤ┏", "ㅤ┣", "ㅤ┗")'
    '\nWRAP_INDENT = ("ㅤ┃ㅤㅤㅤ↝ ", "ㅤ ㅤㅤㅤ↝ ")'
    '\nTAG_FORMAT = "{section_indent}{time} {text}"'
    "\n```"
    "\n"
    "\nTo specify a section heading, add `# heading` on a line by"
    "\nitself or `#` for a blank heading:"
    "\n"
    "\n```"
    "\n$ cat input.txt"
    "\n# Section 1"
    "\ntext 0m0s"
    "\ntext 0m10s"
    "\ntext 0m20s"
    "\n#"
    "\ntext 0m30s"
    "\nvery long text that will be wrapped at 50 characters. 0m40s"
    "\ntext 0m50s"
    "\n```"
    "\n"
    "\nThen run the script:"
    "\n"
    "\n```"
    "\n$ python tagsformat.py input.txt"
    "\n*· · • • • ✤  TIMESTAMPS  ✤ • • • · ·*"
    "\n*[Section 1]*"
    "\nㅤ┏00:00 start"
    "\nㅤ┣00:10 middle"
    "\nㅤ┗00:20 end"
    "\n"
    "\nㅤ┏00:30 second start"
    "\nㅤ┣00:40 Very long text that will be wrapped at 50"
    "\nㅤ┃ㅤㅤㅤ↝ characters."
    "\nㅤ┗00:50 second final end"
    "\n```",
)
parser.add_argument("input", help="file containing timestamps")
parser.add_argument(
    "-s",
    "--auto-section",
    nargs="?",
    const=180,
    type=int,
    help="enable automatic sectioning when a time gap of specified seconds"
    " is reached. Default: 180",
    metavar="SECONDS",
    dest="sec",
)
wrap_group = parser.add_mutually_exclusive_group()
wrap_group.add_argument(
    "-w",
    "--wrap",
    nargs="?",
    const=50,
    default=50,
    type=int,
    help="wrap text at specified character length. Default: 50",
    metavar="LENGTH",
)
wrap_group.add_argument(
    "-nw",
    "--no-wrap",
    action="store_const",
    const=None,
    help="disable text wrapping",
    dest="wrap",
)
args = parser.parse_args()

buffer = io.StringIO()
wrapper = textwrap.TextWrapper(width=args.wrap) if args.wrap else None

korotags_header = re.compile(
    r"https?://\S+ \S+ \d{1,2}, \d{4} \d{1,2}:\d{2} [AP]M \d+ tags? \(\d+\.?\d+/min\)",
)
korotags_pattern = re.compile(
    r"(?P<text>.*) (?:(?P<h>\d+)h)?(?:(?P<m>\d+)m)?(?P<s>\d+)s",
)

with open(args.input, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()
    # Skip empty lines at the start of the file
    for i, line in enumerate(lines):
        if line:
            break
    del lines[:i]
    # Skip header text from Korotagger
    if lines[0] == "Tags" and korotags_header.fullmatch(lines[1]):
        del lines[:2]
    elif korotags_header.fullmatch(lines[0]):
        del lines[0]
    # Add blank heading to start the first section
    if korotags_pattern.fullmatch(line) and args.sec:
        lines.insert(0, "#")
    # Drop the trailing empty lines
    for i, line in enumerate(lines[::-1]):
        if line:
            break
    if i:
        del lines[-i:]
    # Add blank section to end the last section
    lines.append("#")


print(HEADER, file=buffer)

heading_pattern = re.compile(r"\#\s*(?: (.*?))?\s*")


def heading_or_tag():
    for line in lines:
        if heading := heading_pattern.fullmatch(line):
            yield heading, None
        elif tag := korotags_pattern.fullmatch(line):
            text, h, m, s = tag.groups()
            h = int(h or 0)
            m = int(m or 0)
            s = int(s)
            yield None, (text, h, m, s)
        else:
            # write any non-tag lines as-is
            buffer.write(line)


START, MIDDLE, END = 0, 1, 2
pos = START


for (heading, tag), (heading1, tag1) in pairwise(heading_or_tag()):
    end = "\n"

    if heading:
        # Current line is a section heading
        heading = heading.group(1)
        print(SECTION_FORMAT.format(heading) if heading else "", file=buffer)
        pos = START
        continue
    if heading1:
        # Current tag ends a section
        pos = END
    if tag and tag1:
        text, h, m, s = tag
        _, h1, m1, s1 = tag1
        if args.sec and args.sec <= (h1 - h) * 3600 + (m1 - m) * 60 + (s1 - s):
            # Insert a blank section heading
            pos = END
            end = "\n\n"

    # Format tag
    time = bool(h) * f"{h}:" + f"{m:02}:{s:02}"
    tag = TAG_FORMAT.format(section_indent=SECTION_INDENT[pos], time=time, text=text)
    if wrapper:
        wrapper.subsequent_indent = WRAP_INDENT[pos == END]
        tag = wrapper.fill(tag)
    print(tag, file=buffer, end=end)

    # START  (0) -> MIDDLE (1)
    # MIDDLE (1) -> MIDDLE (1)
    # END    (2) -> START  (0)
    pos = pos < END


# Copy to clipboard
buffer_value = buffer.getvalue()
pyperclip.copy(buffer_value)
print(buffer_value)

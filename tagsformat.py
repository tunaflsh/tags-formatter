#!/usr/bin/env python
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
TAG_FORMAT = "{indent}{time} {text}"


parser = argparse.ArgumentParser(
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="This script processes KoroTagger output and formats it for YouTube"
    "\ntimestamps.",
    epilog="A line without tags — but is immediately followed by one — is considered"
    "\na section heading and can be empty. This will be detected in"
    "\nKoroTagger output as well as in already formatted tags. In the"
    "\nlatter case, the file will be reformatted to fix any inconsistencies."
    "\n"
    "\nTo customize the formats, adjust the constants in the script."
    "\n"
    "\nExample constants"
    "\n-----------------------------------------------------------------"
    '\nHEADER = "*· · • • • ✤  TIMESTAMPS  ✤ • • • · ·*"'
    '\nSECTION_FORMAT = "*[{}]*"'
    '\nSECTION_INDENT = ("ㅤ┏", "ㅤ┣", "ㅤ┗")'
    '\nWRAP_INDENT = ("ㅤ┃ㅤㅤㅤ↝ ", "ㅤ ㅤㅤㅤ↝ ")'
    '\nTAG_FORMAT = "{indent}{time} {text}"'
    "\n"
    "\nExample input file"
    "\n-----------------------------------------------------------------"
    "\nSection 1"
    "\nstart 0m0s"
    "\nmiddle 0m10s"
    "\nend 0m20s"
    "\n"
    "\nsecond start 0m30s"
    "\nVery long text that will be wrapped at 50 characters. 0m40s"
    "\nsecond end 0m50s"
    "\n"
    "\nResult"
    "\n-----------------------------------------------------------------"
    "\n*· · • • • ✤  TIMESTAMPS  ✤ • • • · ·*"
    "\n*[Section 1]*"
    "\nㅤ┏00:00 start"
    "\nㅤ┣00:10 middle"
    "\nㅤ┗00:20 end"
    "\n*[]*"
    "\nㅤ┏00:30 second start"
    "\nㅤ┣00:40 Very long text that will be wrapped at 50"
    "\nㅤ┃ㅤㅤㅤ↝ characters."
    "\nㅤ┗00:50 second final end",
)
parser.add_argument(
    "filename",
    nargs="?",
    help="Specifies the file containing tags. If not provided, the script"
    " uses clipboard content.",
)
parser.add_argument(
    "-h",
    "--help",
    action="help",
    help="Show this help message and exit.",
)
parser.add_argument(
    "-o",
    "--output",
    default=None,
    help="Specify the output file for formatted timestamps. Defaults to"
    " modifying the input file in place.",
)
parser.add_argument(
    "-s",
    "--auto-section",
    nargs="?",
    const=180,
    type=int,
    help="Enable automatic sectioning when a time gap of specified seconds"
    " is reached. Default is 180 seconds.",
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
    help="Wrap text at specified character length. Default is 50 characters.",
    metavar="LENGTH",
)
wrap_group.add_argument(
    "-nw",
    "--no-wrap",
    action="store_const",
    const=None,
    help="Disable text wrapping.",
    dest="wrap",
)
args = parser.parse_args()

buffer = io.StringIO()
wrapper = textwrap.TextWrapper(width=args.wrap) if args.wrap else None
korotags = re.compile(
    r"(?P<text>.*) (?:(?P<h>\d+)h)?(?:(?P<m>\d+)m)?(?P<s>\d+)s\n?",
)


with open(args.filename, "r") if args.filename else io.StringIO(pyperclip.paste()) as f:
    input_lines = []
    while (line := f.readline()) == "\n":
        pass
    # Skip header text from Korotagger
    if line == "Tags\n":
        line = f.readline()
    if not re.fullmatch(
        r"https?://\S+"
        r" \S+ \d{1,2}, \d{4} \d{1,2}:\d{2} [AP]M"
        r" \d+ tags? \(\d+\.?\d+/min\)\n",
        line,
    ):
        if korotags.fullmatch(line):
            input_lines.append("\n")
        input_lines.append(line)
    input_lines.extend(f.readlines())
    while input_lines[-1] == "\n":
        input_lines.pop()
    input_lines.append("\n")


print(HEADER, file=buffer)

START, MIDDLE, END = 0, 1, 2
pos = START
section_counter = 0

for curr, succ in pairwise(
    match.groups() if (match := korotags.fullmatch(line)) else line
    for line in input_lines
):
    match curr, succ:
        case str(text), str():
            # Current line is non-tag
            buffer.write(text)
            continue
        case str(text), tuple():
            # Current line is a section heading
            section_counter += 1
            print(
                SECTION_FORMAT.format(
                    text.strip()
                    # Auto sectioning enabled
                    or bool(args.sec) * f"Section {section_counter}"
                ),
                file=buffer,
            )
            pos = START  # Next line starts a section
            continue
        case (text, h, m, s), str():
            # Current tag ends a section
            insert_section = False
            pos = END
        case (text, h, m, s), (_, h_, m_, s_) if (
            args.sec  # Auto sectioning enabled
            and (  # Time gap reached
                (int(h_ or 0) - int(h or 0)) * 3600
                + (int(m_ or 0) - int(m or 0)) * 60
                + (int(s_) - int(s))
                >= args.sec
            )
        ):
            # Insert a new section immediately after the current tag
            insert_section = True
            pos = END
        case tuple(), tuple():
            # Current tag is at the start or in the middle of a section
            insert_section = False

    # Format tag
    h, m, s = int(h or 0), int(m or 0), int(s)
    time = bool(h) * f"{h}:" + f"{m:02}:{s:02}"
    tag = TAG_FORMAT.format(indent=SECTION_INDENT[pos], time=time, text=text)
    if wrapper:
        wrapper.subsequent_indent = WRAP_INDENT[pos == END]
        tag = wrapper.fill(tag)
    print(tag, file=buffer)

    # Add section heading
    if insert_section:
        section_counter += 1
        print(SECTION_FORMAT.format(f"Section {section_counter}"), file=buffer)

    # START  (0) -> MIDDLE (1)
    # MIDDLE (1) -> MIDDLE (1)
    # END    (2) -> START  (0)
    pos = pos < END


# Copy to clipboard
pyperclip.copy(buffer.getvalue())

# Write to file
if filename := args.output or args.filename:
    with open(filename, "w") as f:
        f.write(buffer.getvalue())

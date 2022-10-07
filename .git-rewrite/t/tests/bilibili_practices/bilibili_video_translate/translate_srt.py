src = "en_.srt"
final_srt = "zh_translated.srt"

import srt

wrap_limit = 20

source_srt = open(src, "r",encoding="utf-8").read()

ssrt = srt.parse(source_srt)

from web_translator import translator
import math

def wrapLine(line):
    lines = [line[x*wrap_limit:(x+1)*wrap_limit] for x in range(math.ceil(len(line)/wrap_limit))]
    return "\n".join(lines)

def fixline(line):
    notEndings = ["。","，"]
    for x in notEndings:
        if line.endswith(x): return line[:-1]
    return line

new_ssrt = []
for line in ssrt:
    # print(line)
    start = line.start
    end = line.end # timedelta.
    content = line.content
    index = line.index

    unwrapped_content = content.replace("\n"," ")
    result = translator(unwrapped_content)
    result = fixline(result)
    print(result)
    line.content = result
    new_ssrt.append(line)
    # wrapped = wrapLine(result)
    # print(wrapped)
    # print(start, end, content, index)

final_content = srt.compose(new_ssrt)
with open(final_srt,"w+",encoding="utf-8") as f:
    f.write(final_content)
from load_demo_data import dat2 as data

# the data is indeed unstructured.
# split the data with newline.
# we need to check the line number.

# shall we really strip out the trailing white space, causing potential unwanted merges?
# preserve at most one white space in the end? or forcing one white space instead?

# first we want line by line presentation. make sure we get the right array!
# CRLF -> LF should be done before this step. it does not affect readability or structure.

# since we do not have the 'keyword' based highlighter, we can only do line-wise highlighting.

# where's the crlf -> lf ?
data = data.replace("\r\n", "\n")
# the original data, shall be used as reference. save it somewhere, like database.

linewise = data.split("\n")  # there won't be "\n" in the line.

# it goes without saying that a media guy sure need some search skills.

def removeDuplicates(line, chars=[" ", "\t"], maxConsecutiveLength=1):
    for char in chars:
        minUnallowedConsecutiveLength = maxConsecutiveLength + 1
        while True:
            if char * minUnallowedConsecutiveLength in line:
                line = line.replace(
                    char * minUnallowedConsecutiveLength, char * maxConsecutiveLength
                )
            else:
                break
    return line


def stripChars(line, chars=[" ", "\t"]):
    while True:
        flag = False
        for char in chars:
            if line.startswith(char) or line.endswith(char):
                line = line.strip(char)
                flag = True
        if not flag:
            break
    return line


def standardLineCleaner(line):
    line = removeDuplicates(line)
    line = stripChars(line)
    return line


char_per_group = 30
group_per_conv_group = 3
step_group_for_conv = 2  # instead of 1. just to make sure these conv groups overlap.

assert step_group_for_conv >= 1
assert (
    step_group_for_conv <= group_per_conv_group
)  # at least there is no gap, though when equal there will be no overlapping.
assert group_per_conv_group >= 1
assert char_per_group >= 1
# rule to add space: if there's "-" ending, remove the "-" then directly concat with another line.
# if not, then make sure there's one space between two lines.
# create char index to line index mapping.

newContent = ""
newContentCharIndexToLineIndexDict = {}

alphabets = "abcdefghijklmnopqrstuvwxyz"
alphabets += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
import string
english_punctuation = string.punctuation

for lineNumber, line in enumerate(linewise):
    line_cleaned = standardLineCleaner(line)
    # for zero length line (after cleaned), we skip without doing anything.
    if len(line_cleaned) == 0:
        continue
    # print("{}:".format(lineNumber), line_cleaned)
    # this process will never decrease the length of the line.
    # i guess the symbol is different somehow. the hyphen is not avaliable on keyboard.
    if line_cleaned.endswith("-") or line_cleaned.endswith("‐"):
        line_cleaned = line_cleaned[:-1]
    elif line_cleaned[-1] in alphabets+english_punctuation:
        line_cleaned += " "
    # we shall get the length again, cause we have processed this thing.
    lineCleanedLength = len(line_cleaned)
    newContentLength = len(newContent)
    mDict = {newContentLength + index: lineNumber for index in range(lineCleanedLength)}
    newContent += line_cleaned
    newContentCharIndexToLineIndexDict.update(mDict) # this shall be the most memory intensive object. delete it after use.

# now, how to do convolution, or the windowed conv-like excerpt creation?
# print("MAX KEY:", max(list(newContentCharIndexToLineIndexDict.keys())))
# MAX KEY: 85783
# which is smaller than:
# KeyError: 85830
# so it is obvious that we need the smaller 'endIndex', by using min(endIndex, newContentLength)
# breakpoint()

newContentLength = len(newContent)
startIndex = 0
listOfCleanedMergedConvGroupWithLineIndexMapping = []
# maybe you want to merge the fetched 'cleanedMergedConvGroup' according to 'lineIndexMapping', but that's another story.
# you can use the mathlib, from pyjom.
# i think the mathlib should be embedded to lazero. pyjom's mathlib can be grabbed from there.
while True:
    if startIndex >= newContentLength:  # does not break? wtf?
        break
    endIndexOffset = group_per_conv_group * char_per_group
    endIndex = startIndex + endIndexOffset
    endIndex = min(endIndex, newContentLength - 1)
    if endIndex <= startIndex:  # failsafe.
        continue
    # the append process.
    lineIndexStart = newContentCharIndexToLineIndexDict[
        startIndex
    ]  # maybe not just one line?
    lineIndexEnd = newContentCharIndexToLineIndexDict[endIndex]  # key error? wtf?
    lineIndicesTuple = (lineIndexStart, lineIndexEnd)
    mElem = {
        "conv_group_merged": newContent[startIndex:endIndex],
        "line_range": lineIndicesTuple,
    }
    listOfCleanedMergedConvGroupWithLineIndexMapping.append(
        mElem
    )  # this shall be the thing that we need. just maybe.
    # add to startIndex.
    startIndex += step_group_for_conv * char_per_group

# we decide to join lines with space no matter what. afterwards we use standard cleaner to remove duplicate spaces.

del newContentCharIndexToLineIndexDict # maybe we should not delete this, to create more accurate highlights, determine boudaries with whitespace?
# but it is way too cumbersome, and not necessary. we can compute this.

# when extracted merged conv groups are next to each other, highlight the conv group with the highest score and other hits use secondary colors. for single conv group without neighbors, directly highlight it with primary color.

if __name__ == "__main__":
    # a typical test. we check this manually.
    from lazero.utils.logger import sprint

    the_final_one = listOfCleanedMergedConvGroupWithLineIndexMapping[-1]
    print("CONTENT EXCERPT:")
    sprint(the_final_one["conv_group_merged"])
    start, end = the_final_one["line_range"]
    myLines = linewise[start : end + 1]  # this is inclusive!
    # shall we only change the text color?
    for line in myLines:
        print(line)
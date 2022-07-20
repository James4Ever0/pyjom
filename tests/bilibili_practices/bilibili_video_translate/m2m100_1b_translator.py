from functional_dl_translator_1b_deepspeed import get_response as m2m100_zte_translator # this shit could consume much computational resource.
# advice you to do it with json.

def fixline(line):
    notEndings = ["。","，"]
    for x in notEndings:
        if line.endswith(x): return line[:-1]
    return line

def zh_to_en_translator(text,needFixLine=True):
    result = m2m100_zte_translator(text)[0] # shit.
    if needFixLine: result = fixline(result)
    return result
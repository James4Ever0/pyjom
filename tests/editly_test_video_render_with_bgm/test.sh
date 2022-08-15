# run in headless linux machine! test both xvfp specs?
# xvfb-run -s "-ac -screen 0 1280x1024x24" editly test.json5 --fast # this will suffice. json5 will specify all specs?
xvfb-run -s "-ac -screen 0 1920x1080x24" editly test.json5 --fast # this will suffice. json5 will specify all specs? this 'fast' setting definitely reduced the output resolution

# without --keep-source-audio, will we not hear anything from the source video?

# json5: json for humans
# this much likely to bring python dict and json objects into a single readable format.
git ls-files --other --modified --exclude-standard | grep -E ".py\$" | cat | xargs -iabc black abc
# find | grep -E ".py\$" | xargs -iabc black abc
# this only format changed files.

#format medialang files.
git ls-files --other --modified --exclude-standard | grep -E ".mdl\$" | cat | xargs -iabc python3 -m pyjom.medialang -f abc
git ls-files --other --modified --exclude-standard | grep -E ".media\$" | cat | xargs -iabc python3 -m pyjom.medialang -f abc
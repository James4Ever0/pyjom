import pygame

# pillow can also do that
# https://plainenglish.io/blog/generating-text-on-image-with-python-eefe4430fe77

textContent = "".join(["中","ぁ"]+[f"{index+1}" for index in range(100)]) # will see [100] at the end of text if successful.

# pygame.font.get_fonts()
# install your font to system please? but why all lower case font names?

fontName = "notosans"
fontSize = 20

font = pygame.font.SysFont(fontName,fontSize)

output = "test_render.png"


import pygame

textContent = "".join([f"{index+1}" for index in range(100)]) # will see [100] at the end of text if successful.

# pygame.font.get_fonts()
# install your font to system please? but why all lower case font names?

fontName = "notosans"
fontSize = 20

font = pygame.font.SysFont(fontName,fontSize)


import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
black, white = pygame.Color('black'), pygame.Color('white')

# pillow can also do that
# https://plainenglish.io/blog/generating-text-on-image-with-python-eefe4430fe77

textContent = "".join(["中","ぁ"]+[f"{index+1}" for index in range(100)]) # will see [100] at the end of text if successful.

# pygame.font.get_fonts()
# install your font to system please? but why all lower case font names?

fontName = "notosans"
fontSize = 20

font = pygame.font.SysFont(fontName,fontSize)

output_name = "test_render.png"

word_surface = font.render(textContent, False, black)
word_width, word_height = word_surface.get_size()
size = 
image.fill(white)
image.blit(word_surface,(0,0))
pygame.image.save(image,output_name)
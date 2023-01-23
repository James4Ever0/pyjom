import os

# https://github.com/ntasfi/PyGame-Learning-Environment/issues/26
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
pygame.init()
black, white = pygame.Color('black'), pygame.Color('white')

# pillow can also do that
# https://plainenglish.io/blog/generating-text-on-image-with-python-eefe4430fe77

textContent = "".join(["中","ぁ"]+[f"[{index+1}]" for index in range(100)]) # will see [100] at the end of text if successful.

# pygame.font.get_fonts()
# install your font to system please? but why all lower case font names?

# fontName = "notosans"
# this font is bad.
fontSize = 40

# font = pygame.font.SysFont(fontName,fontSize)
# fontPath = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf" # shit this fails.
fontPath = "./get_and_merge_fonts/GoNotoCurrent.ttf"
# use some kind of super large merged notofont.

font = pygame.font.Font(fontPath, fontSize)

output_name = "test_render.png"

word_surface = font.render(textContent, False, black)
word_width, word_height = word_surface.get_size()
margin=20
SIZE=(word_width+margin*2, word_height+margin*2)
image = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
image.fill(white)
image.blit(word_surface,(margin,margin))
pygame.display.update()
pygame.image.save(image,output_name)

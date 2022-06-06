import pygame
import io
try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

class Image(object):
    def __init__(self, pos, url=None, file_path=None, scale=None):
        pygame.init()
        self.original_pos = pos
        self.pos = pos

        if file_path is not None:
            self.image = pygame.image.load(file_path)
        else:
            self.image = self._image_url_to_loadable(url)

        if scale is not None:
            self.image = pygame.transform.scale(self.image, scale)

    def _image_url_to_loadable(self, image_url):
        '''
        converts url to file object
        :param image_url: image url
        :return: image file
        '''
        image_str = urlopen(image_url).read()
        image_file = io.BytesIO(image_str)
        image = pygame.image.load(image_file)

        image = pygame.transform.scale(image, (image.get_height()*2, image.get_width()*2))
        return image

    def draw(self, screen):
        '''
        :param screen: screen to display the image
        :return: None
        '''
        screen.blit(self.image, self.pos)

    def update_pos(self, direction):
        '''
        :param direction: direction the position should be update to
        :return: None
        '''
        if direction == "up":
            self.pos = (self.pos[0] + 16, self.pos[1] - 7)
        elif direction == "down":
            self.pos = (self.pos[0] - 16, self.pos[1] + 7)
        else:
            self.pos = (self.pos[0], self.pos[1] + 15)


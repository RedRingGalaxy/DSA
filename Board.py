import pygame as pg
from pygame import gfxdraw as pgfx
import string, time

class TreeNode(pg.sprite.Sprite):

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.left = None
        self.right = None
        self.size = 50

        self.image = None
        self.rect = None

        if data != None:
            self.__buildImage(self.size)

    @property
    def Size(self):
        return self.size

    @Size.setter
    def Size(self, value):
        self.size = value
        if self.data != None:
            self.__buildImage(self.size)

    def __buildImage(self, SIZE):

        BGCOLOR = (255, 80, 77)
        FGCOLOR = (255,255,255)

        font = pg.font.SysFont("Segoe UI", int( SIZE * 0.4 ))
        font.set_bold(True)
        text = font.render(str(self.data),True,FGCOLOR,BGCOLOR)
        text_rect = text.get_rect()

        if text_rect.width > self.size:
            self.size = text_rect.width + 10
        else:
            self.size = SIZE

        surf = pg.Surface([self.size, self.size])
        surf.fill((0,0,0))
        surf.set_colorkey((0,0,0))
        surf_rect = surf.get_rect()

        p = surf_rect.center

        pgfx.filled_circle(surf, p[0], p[1], self.size//2 - 2, BGCOLOR)
        
        text_rect.center = surf_rect.center
        surf.blit(text,text_rect)

        self.image = surf
        self.rect = self.image.get_rect()

class TreeBoard(pg.sprite.Sprite):
    '''
    '''
    def __init__(self, tree):
        
        super().__init__()

        self.image =  None
        self.rect = None

        self.x = 0
        self.y = 0

        self.active = False

        self.BGCOLOR = (255, 80, 77)

        if tree != None:
            self.NormalizeNodes(tree)
            h = self.GetHeight(tree)

            size = ((pow(2, h-1) * 2)) * tree.Size
            
            surf = pg.Surface([size, size])
            surf.set_colorkey((0,0,0))

            self.UpdatePos(tree, (pow(2, h-1) * 2) - 1, 0, 1)

            self.drawTree(surf, tree)

            self.image = surf
            self.rect = self.image.get_rect()
            self.imagesize = (self.rect.width, self.rect.height)

            self.Zoom = 100

    def event_handler(self, e):
        pos = pg.mouse.get_pos()

        if e.type == pg.MOUSEBUTTONDOWN: 
                '''
                1. If mouse inside the tree board then set the board status as active.

                '''
                if (pos[0] > self.x and pos[0] < (self.x + self.rect.w) and 
                    pos[1] > self.y and pos[1] < (self.y + self.rect.h)):
                    self.__prevpos = pg.mouse.get_pos()
                    
                    if e.button == 1: # Left Mouse Button ( Mouse Wheel = 2, Mouse Right = 3)
                        self.active = True

                    if e.button == 4: # Scroll UP
                        self.Zoom += 10

                    if e.button == 5: # Scroll Down
                        self.Zoom -= 10
                    

        if e.type == pg.MOUSEBUTTONUP:

            if self.active and  e.button == 1:
                x, y = pg.mouse.get_pos()
                if self.__prevpos[0] - x > 0:
                    self.ScrollRight(self.__prevpos[0] - x)
                else:
                    self.ScrollLeft(self.__prevpos[0] - x)

                if self.__prevpos[1] - y > 0:
                    self.ScrollUp(self.__prevpos[1] - y)
                else:
                    self.ScrollDown(self.__prevpos[1] - y)

                self.active = False

    def NormalizeNodes(self, root) -> None:
        '''
        Resize the nodes in the tree to the maximum size of the node in the tree.
        '''
        temp = root
        msize = self.FindeMaxSize(root)
        self.UpdateSize(root, msize)

    def FindeMaxSize(self, root) -> int:
        '''
        Return the maximum size of the node in the tree.
        '''
        if root == None:
            return 0

        msize = max(self.FindeMaxSize(root.left), self.FindeMaxSize(root.right))

        return max(msize, root.Size)

    def UpdateSize(self, root, msize) -> None:
        if root == None:
            return
        root.Size = msize
        self.UpdateSize(root.left, msize)
        self.UpdateSize(root.right, msize)

    def GetHeight(self, root) -> int:
        if root == None:
            return 0

        return 1 + max(self.GetHeight(root.left), self.GetHeight(root.right))

    def drawTree(self, screen, root) -> pg.Rect:
        '''
        drawTree ( screen , root ) -> return root.rect.center
        type(screen) -> Surface
        type(root) -> TreeNode

        '''
        if root == None:
            return None

        this = root.rect.center
        left = self.drawTree(screen, root.left)
        right = self.drawTree(screen, root.right)

        if left != None:
            pg.draw.line(screen,self.BGCOLOR, [this[0], this[1]], [left[0], left[1]], 5)
            screen.blit(root.left.image, root.left.rect)

        if right != None:
            pg.draw.line(screen,self.BGCOLOR, [this[0], this[1]], [right[0], right[1]], 5)
            screen.blit(root.right.image, root.right.rect)

        screen.blit(root.image, root.rect)

        return root.rect.center

    def UpdatePos(self, root, ln, strt, level) -> None:
        if root == None:
            return None
      
        x1 = (ln / pow(2 , level)) + strt
        y1 = level

        root.rect.x = (int(x1) * root.rect.width)
        root.rect.y = y1 * root.rect.width

        self.UpdatePos(root.left, ln, strt, level + 1)
        self.UpdatePos(root.right, ln, x1, level + 1)

    def ScrollLeft(self, x) -> None:
        if self.rect.x > 0:
            self.rect.x = self.rect.x + x if self.rect.x + x > 0 else 0

    def ScrollRight(self, x) -> None:
        if self.rect.x < self.imagesize[0] - self.rect.w:
            self.rect.x = self.rect.x + x if self.rect.x + x <= (self.imagesize[0] - self.rect.w) else self.imagesize[0] - self.rect.w 

    def ScrollUp(self, y) -> None:
        if self.rect.y < self.imagesize[1] - self.rect.h:
            self.rect.y = self.rect.y + y if self.rect.y + y <= (self.imagesize[1] - self.rect.h) else self.imagesize[1] - self.rect.y

    def ScrollDown(self, y) -> None:
        if self.rect.y > 0:
            self.rect.y = self.rect.y + y if self.rect.y + y > 0 else 0

    def ZoomView(self, zpercent) -> pg.sprite:
        '''
        Zoom ( zoom_percentage) -> return sprite_image
        type( zoom_percentage ) -> int
        '''
        # Resize the origianl sprite image to the Zoom percentage.
        # The maximum size of the result image will Original image size.
        # The minimum size of the result image will be width of the rect.
        
        # Zoom == 0 then Original size else scale image to Zoom 

        if self.Zoom + zpercent >= 100:
            self.Zoom = 100
        elif self.Zoom + zpercent <= 10:
            self.Zoom = 10
        else:
            self.Zoom += zpercent

        rct = self.image.get_rect()

        div = ( self.Zoom / 100 )

        if div <= 0:
            div = 1

        w = rct.w // div
        h = rct.h // div
        
        if w < self.rect.w and h < self.rect.h:
            _, _, w, h = self.rect        

        tw =  int((rct.w - w))
        th = int((rct.h - h))
        w = self.rect.w if rct.w + tw < self.rect.w else rct.w + tw
        h = self.rect.h if rct.h + th < self.rect.h else rct.h + th
        self.imagesize = (w,h)

        # Reset the position to fit in the box ( width and height )
        if self.rect.x < 0 or self.rect.x > self.imagesize[0]:
            self.rect.x = 0
        elif (self.rect.w + self.rect.x > self.imagesize[0]): #self.rect.w - self.rect.x < self.imagesize[0] and 
            self.rect.x += (self.rect.w + self.rect.x) -  self.imagesize[0]

        if self.rect.y < 0 or self.rect.y > self.imagesize[1]:
            self.rect.y = 0
        elif (self.rect.h + self.rect.y > self.imagesize[1]):
            self.rect.y += (self.rect.h + self.rect.y) -  self.imagesize[1]

        # Scale the image to the calculated width
        # Draw the border of the box   
        img_rslt = pg.transform.scale(self.image,(w,h))
        pg.draw.rect(img_rslt,(0,0,1),(self.rect.x,self.rect.y, self.rect.w,self.rect.h), 4)

        return img_rslt

class TextBox(pg.sprite.Sprite):
    def __init__(self, x, y, **kwargs):
        '''
        TextBox( x, y) -> TextBox
        x -> x-position.
        y -> y-position.
        w -> width of the textbox.
        h -> height of the textbox. Height of the text box will be
        the height of the font.
        bgcolor ->  Background color.
        fgcolor -> Text color.
        active -> Set to true on click the TextBox
        enabled -> Enable or disable textbox

        '''
        super().__init__()

        self.__text = []
        self.__rect = []
        self.__Char = []
        self.__placeHolder = None
        self.__cursorIndex = 0
        
        self.font = pg.font.SysFont("Segoe UI",14)     
        self.x = x
        self.y = y
        self.w = 100
        self.h = self.font.get_height() + 6
        self.bgcolor = (255,255,255)
        self.fgcolor = (0,0,0)
        self.activecolor = (51, 153, 255)
        self.active = False
        self.enabled = True

        self.image = pg.Surface([self.w, self.h])
        self.image.fill(self.bgcolor)
        self.image.set_colorkey(self.bgcolor)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        pg.draw.rect(self.image, self.activecolor if self.active else self.bgcolor ,(self.x, self.y, self.w, self.h), 2)

    @property
    def PlaceHolder(self):
        return self.__placeHolder

    @PlaceHolder.setter
    def PlaceHolder(self, text):
        self.__placeHolder = text

    @property
    def Text(self):
        return ''.join(self.__Char)

    def Width(self, width):
        self.w = w

    # TODO: Clear Text in the textbox
    def Clear(self):
        self.__Char = []
        self.__text = []
        self.__rect = []
        self.__cursorIndex = 0

    # TODO: Handle Textbox event
    def event_handler(self, e):
        # TODO: Handle Mouse event
        pos = pg.mouse.get_pos()
        if e.type == pg.MOUSEBUTTONDOWN:
            if( self.rect.collidepoint(pos) and  e.button == 1):
                    self.active = True
                    
                    for i, r in enumerate(self.__rect, 0):
                        if pos[0] - self.rect.x < 5:
                            self.__cursorIndex = 0
                            break
                        elif r.x > pos[0] - self.rect.x:
                            self.__cursorIndex = i
                            break
                        else:
                            self.__cursorIndex = i + 1
                    
            else:
                self.active = False

        # TODO: Handle Keyboard keys
        if e.type == pg.KEYDOWN and self.active:
            
            txt = e.unicode

            # TODO: Handle backspace - delete the chares forward
            if pg.key.name(e.key) == 'backspace' and len(self.__text) > 0: 
                idx = self.__cursorIndex
                xdif = self.__rect[idx].x - self.__rect[idx - 1].x  if idx - 1 >= 0 and idx < len(self.__text) else 0
                for i in range( idx , len(self.__rect), 1):
                    self.__rect[i].x -= xdif #self.__rect[i-1].x + self.__rect[i-1].w if i > self.__cursorIndex else self.__rect[i].x
            
                self.__rect.pop(idx - 1)
                self.__text.pop(idx - 1)
                self.__Char.pop(idx - 1)
                self.__cursorIndex -= 1

             # TODO: Handle backspace - delete the chares backward
            elif pg.key.name(e.key) == 'delete' and len(self.__text) > 0 and len(self.__text) > self.__cursorIndex:
                idx = self.__cursorIndex
                xdif = self.__rect[idx + 1].x - self.__rect[idx].x  if len(self.__rect) > idx + 1 else 0
                for i in range(idx, len(self.__rect), 1):
                    self.__rect[i].x -= xdif #self.__rect[i].x + self.__rect[i].w if i > self.__cursorIndex else self.__rect[i].x
                
                self.__rect.pop(idx)
                self.__text.pop(idx)
                self.__Char.pop(idx)
            
             # TODO: Check the key is valid. If char is not valid or empty then return.
            char = ''.join(filter(lambda x: x in string.printable, txt))
            if char == '':
                return

            else:
                txt_fnt = self.font.render(txt, True, self.fgcolor)
                txt_rect = txt_fnt.get_rect()
                prev_char = self.__rect[self.__cursorIndex - 1] if len(self.__rect) > 0 else None
                txt_rect.x = prev_char.x + prev_char.w + 1 if prev_char != None else 5

                self.__text.insert(self.__cursorIndex, txt_fnt)
                self.__rect.insert(self.__cursorIndex, txt_rect)
                self.__Char.insert(self.__cursorIndex, char)
                self.__cursorIndex += 1

                for i in range( self.__cursorIndex, len(self.__rect), 1):
                    self.__rect[i].x = self.__rect[i-1].x + self.__rect[i-1].w + 1

    # TODO: Update Sprite
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.display()

    # TODO: On update redraw Textbox
    def display(self, screen = None):
        img = pg.Surface([self.w, self.h])
        img.fill(self.bgcolor)
        img.set_colorkey(self.bgcolor)
        img_rect = self.image.get_rect()
        
        self.image = img
        self.rect = img_rect
        self.rect.x = self.x
        self.rect.y = self.y

        for t, r in zip(self.__text, self.__rect):
            img.blit(t, r)

        x, _, w, _ = self.__rect[self.__cursorIndex - 1] if len(self.__rect) != 0 else (5,0,0,0)
        x = x + w if self.__cursorIndex > 0 else 5

        pg.draw.rect(img, self.activecolor if self.active else self.fgcolor , (0, 0, self.w, self.h), 1)

        # For blink cursor
        if time.time() % 1 > 0.5 and self.active:
            pg.draw.line(img, self.fgcolor, (x - 1, 3),(x -1, self.rect.h - 6), 1)

        if screen != None:
            screen.blit(self.image, self.rect)

class TextButton(object):
    def __init__(self, canvas, canvas_rect, x, y, width, height, text):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
        self.Text = text
        self.Canvas = canvas
        self.Canv_rect = canvas_rect

        self.bgColor = (0, 172, 237) # (77, 210, 255)
        self.fgColor = (255, 255, 255)
        self.ActiveColor = (0, 131, 179)
 
        self.Click = None
        self.args = None
        self.Active = False
        self.Enabled = True

        self._Clicked = False
        self._rad = 0
        self._curpos = [0,0]
        
        self._surface = pg.Surface([self.Width,self.Height],pg.SRCALPHA)
        self._surface.set_colorkey((0,0,0))
        self._surface.set_alpha(128)

    def handle_event(self, event):

        if not self.Enabled:
            return

        x = self.Canv_rect.x
        y = self.Canv_rect.y

        x = x + self.X
        y = y + self.Y
        w = x + self.Width
        h = y + self.Height

        # Set the button state as active if the cursor on the button
        if ( event.pos[0] >= x and event.pos[0] <= w and event.pos[1] >= y and event.pos[1] <= h ): 

            self.Active = True

            if event.type == pg.MOUSEBUTTONDOWN and self._Clicked != True:
                self._Clicked = True
                self._curpos[0] = event.pos[0]
                self._curpos[1] = event.pos[1]
                None if self.Click == None else self.Click( self, self.args)
        else:
            self.Active = False

    '''
    1. Draw the button on the given surface,
    2. Draw\Play aniamtion on click,
    3. Draw button text.

    '''    
    def draw(self):

        surf_rect = self._surface.get_rect(topleft = (self.X, self.Y))
        color = self.ActiveColor if self.Active else self.bgColor # Select the button color by state

        if self._rad == 0 :
            self._curpos[0] = self._curpos[0] - self.Canv_rect.x - self.X
            self._curpos[1] = self._curpos[1] - self.Canv_rect.y - self.Y

        # Draw animation on click
        if self._Clicked:
            pg.draw.rect(self._surface,color,(0, 0, self.Width, self.Height))

            if self._rad < self.Width:
                surf = pg.Surface([self.Width,self.Height],pg.SRCALPHA, 32)
                surf.set_colorkey((0,0,0))
                surf.set_alpha(128)
                pg.draw.circle(surf,(255, 255, 255, 100),self._curpos, self._rad)
                self._surface.blit(surf, (0,0))
                self._rad += 10
            else:
                # Reset the value after animation done
                self._Clicked = False
                self._rad = 0
        else:
            pg.draw.rect(self._surface,color,(0, 0, self.Width, self.Height))

        if not self.Enabled:
            surf = pg.Surface([self.Width,self.Height],pg.SRCALPHA, 32)
            surf.set_colorkey((0,0,0))

            pg.draw.rect(surf,(255, 255, 255, 100),(0, 0, self.Width, self.Height))
            self._surface.blit(surf, (0,0))

        #Init fonts and draw the button text
        font = pg.font.SysFont('Segoe UI', 14)
        font.set_bold(True)

        text = font.render(self.Text, True, self.fgColor)
        trect = text.get_rect()
        trect.center = (self.Width//2, self.Height//2)

        # Redraw the button on the canvas
        self._surface.blit(text, trect)
        self.Canvas.blit(self._surface, surf_rect)
     
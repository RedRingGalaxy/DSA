import pygame as pg
from Board import TreeBoard, TreeNode, TextBox, TextButton

def main():

    DONE = False
    SIZE = 750
    
    pg.init()

    screen = pg.display.set_mode([SIZE,SIZE])
    screen.fill((255,255,255))

    clock = pg.time.Clock()
    fps = 30

    tree = None # TreeNode(0)
    # tree.left = TreeNode(2)
    # tree.left.left = TreeNode(4)
    # tree.left.right = TreeNode(5)
    # tree.left.left.left = TreeNode(8)
    # tree.left.left.right = TreeNode(9)
    # tree.left.right.left = TreeNode(10)
    # tree.left.right.right = TreeNode(11)
    # tree.right = TreeNode(3)
    # tree.right.left = TreeNode(6)
    # tree.right.right = TreeNode(7)
    # tree.right.left.left = TreeNode(12)
    # tree.right.left.right = TreeNode(13)
    # tree.right.right.left = TreeNode(14)
    # tree.right.right.right = TreeNode(15)
    # tree.right.right.right.right = TreeNode(20)

    # tree.Size = 100

    treeboard = TreeBoard(tree)
    # treeboard.rect.w = int(SIZE)
    # treeboard.rect.h = int(SIZE * 0.75)
    # treeboard.x = abs(treeboard.rect.w - SIZE) //2
    # treeboard.y =  abs(treeboard.rect.h - SIZE) 

    prevpos = (0,0)
    
    font = pg.font.SysFont("Segoe UI",12)
    t1 = TextBox(50, 50, font = font)
    t1.w = 200
    t1.PlaceHolder = "Enter Text"
    t1.text = "Thiru"

    items = pg.sprite.Group()
    items.add(t1)

    b1 = TextButton(screen, screen.get_rect(), 275, 50, 100, 30, "Add")

    while not DONE:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                DONE = True

            if tree != None:
                treeboard.event_handler(event)
            t1.event_handler(event)
            # b1.handle_event(event)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_KP_ENTER:
                    if tree == None:
                        tree = TreeNode(t1.Text)
                        treeboard = TreeBoard(tree)
                        treeboard.rect.w = int(SIZE)
                        treeboard.rect.h = int(SIZE * 0.75)
                        treeboard.x = abs(treeboard.rect.w - SIZE) //2
                        treeboard.y =  abs(treeboard.rect.h - SIZE) 
                        t1.Clear()

        screen.fill((255,255,255))

        if treeboard != None and tree != None:
            screen.blit(treeboard.ZoomView(0), (treeboard.x,treeboard.y),treeboard.rect)
        #screen.draw.textbox("hello world", (100, 100, 200, 50))
        items.update()
        items.draw(screen)

        b1.draw()

        

        pg.display.update()

        clock.tick(fps)

if __name__ == "__main__":
    main()
    # pg.init()
    # font = pg.font.SysFont("Segoe UI",12)
    # t1 = TextBox(10, 5, width = 10, font = font)
    
    # print(t1.W, type(t1.Font), t1.Font.get_height(), t1.H)
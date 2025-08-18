import pygame as pg

# setup
pg.init()
window = pg.display.set_mode(size=(1200, 850))

while True:
    # Check for all events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()  # Close Window
            quit() # End Pygame






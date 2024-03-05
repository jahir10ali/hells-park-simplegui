from vector import Vector

try:
    import Simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

name = "Water Boy"
title_button_pos = Vector(296,200)

class homescreen():

    def __init__(self, title):
        self.title = title
        self.start_button_pos = Vector(450,380)
        self.how_to_play_button_pos =Vector(380,500)
    
    def draw(self, canvas):
        global title_button_pos

        canvas.draw_text(self.title, title_button_pos.get_p() , 100, 'Blue', 'serif' )
        canvas.draw_text("Start", self.start_button_pos.get_p(), 50, 'Blue', 'serif')
        canvas.draw_text("How to play", self.how_to_play_button_pos.get_p(), 50, 'Blue', 'serif')

    def click_trigger(self, pos):
        self.click_pos = pos
        if self.clicked_inside_button(pos, self.start_button_pos):
            frame.set_draw_handler(start_screen.draw)
        elif self.clicked_inside_button(pos, self.how_to_play_button_pos):
            frame.set_draw_handler(tutorial_screen.draw)



    def clicked_inside_button(self, pos, button_pos):
        return (
            self.click_pos[0] > button_pos.get_p()[0] and self.click_pos[0] < button_pos.get_p()[0]+ 100 and
            self.click_pos[1] > button_pos.get_p()[1] -50  and self.click_pos[1] < button_pos.get_p()[1]
        )
    
class startscreen():

    def draw(self, canvas):
        global title_button_pos
        canvas.draw_text("Choose your level", title_button_pos.get_p(), 50, 'Blue', 'serif')


class tutorialscreen():

    def draw(self, canvas):
        global title_button_pos
        canvas.draw_text("How to play: ", title_button_pos.get_p(), 50, 'Blue', 'serif')
        canvas.draw_text("Back", (400, 400), 50, 'Blue', 'serif')



opening_screen = homescreen(name)
start_screen = startscreen()
tutorial_screen = tutorialscreen()

frame = simplegui.create_frame("Welcome Screen", 1000, 700)
frame.set_canvas_background("white")
frame.set_mouseclick_handler(opening_screen.click_trigger)

frame.set_draw_handler(opening_screen.draw)
frame.start()

# this is the menu screen of the game to be worked on
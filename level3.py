'''
This is the level3.py file that includes everything for level 3.
'''

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from imagesANDbuttons import draw_button, draw_image


CANVAS_WIDTH = 900
CANVAS_HEIGHT = 600
PLAYER_SIZE = 20
GRAVITY = Vector(0, 0.25)
FLOOR_Y = CANVAS_HEIGHT - PLAYER_SIZE / 2  


game_over_sound = simplegui.load_sound('https://audio.jukehost.co.uk/4rXY9bKqh9LnxFndLGst7Xs9U9YpKr9b')
coin_sound = simplegui.load_sound('https://audio.jukehost.co.uk/UeryrWle3hDSLEgIqrA2zyNG0mNqX15F')
jump_sound = simplegui.load_sound('https://audio.jukehost.co.uk/849X7g5DQKqnC6dGOuU1asWeUx4D1GUy')
sprite = simplegui.load_image('https://i.ibb.co/BVLTF72/sprite.png')
sprite_inverted = simplegui.load_image('https://i.ibb.co/jfXGNJp/sprite-inverted.png')


class Platform:
    def __init__(self, position, width, height):
        self.x, self.y = position
        self.width = width
        self.height = height
        self.edge_l = self.x  
        self.edge_r = self.x + self.width  
        self.edge_b = self.y + self.height  
        self.edge_t = self.y  

    def draw(self, canvas):
        canvas.draw_polygon([(self.x, self.y),
                             (self.x + self.width, self.y),
                             (self.x + self.width, self.y + self.height),
                             (self.x, self.y + self.height)],
                            3, 'White', 'Black')


class Trap:
    def __init__(self, spikes_quantity, position, width, height):
        self.spikes = []
        self.width = width
        self.height = height
        self.edge_l = position[0] - width / 2 
        self.edge_r = position[0] + (width / 2 * spikes_quantity)  
        self.edge_b = position[1]  
        self.edge_t = position[1] - height  
        
        for i in range(spikes_quantity):
            spike_x = position[0] - width / 2 + i * width / 2
            spike_y = position[1]
            spike = [(spike_x, spike_y), (spike_x + width / 2, spike_y), (spike_x + width / 4, spike_y - height)]
            self.spikes.append(spike)

    def draw(self, canvas):
        for spike in self.spikes:
            canvas.draw_polygon(spike, 3, "#5F5F5F", "#A5A2A2")

    def hit(self, player):
        return player.offset_l() <= self.edge_r and player.offset_r() >= self.edge_l \
            and player.offset_t() <= self.edge_b and player.offset_b() >= self.edge_t
        
   
class Coin:
    def __init__(self, position, radius, border):
        self.x, self.y = position
        self.radius = radius
        self.border = border

    def draw(self, canvas):
        canvas.draw_circle([self.x, self.y], self.radius, self.border, 'Yellow', 'Orange')
  
        
class Player:
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.vel = Vector(0, 0)
        self.on_ground = True
        self.moving_left = False
        self.moving_right = False
        self.can_move = True
        self.level_complete = False
        self.spritesheet_width = 512
        self.spritesheet_height = 576
        self.column = 8
        self.rows = 9
        self.vel = Vector()
        self.frame_index = [0,0]
        self.modulo = 5
        self.sprite_number_r_and_l = 22
        self.sprite_top = 20
        self.sprite_bottom = 35

        self._init_dimension()

    def _init_dimension(self):
        self.frame_width = self.spritesheet_width / self.column
        self.frame_height = self.spritesheet_height / self.rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    def reset(self, pos, image):
        self.__init__(pos, image)

    def draw(self, canvas):
        
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )
       
        source_size = (self.frame_width, self.frame_height)
        dest_centre = self.pos.get_p()
        dest_size = (150, 150)

        canvas.draw_image(self.image, source_centre, source_size, dest_centre, dest_size)
        
    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.modulo

    def update(self, platforms, traps, coins, finish_line, clock):
        self.vel += GRAVITY
        if self.moving_left:
            self.vel.x = -5
        elif self.moving_right:
            self.vel.x = 5
        else:
            self.vel.x = 0
            
        self.pos += self.vel
        
        if self.pos.y >= CANVAS_HEIGHT - self.sprite_top:
            self.pos.y = CANVAS_HEIGHT - self.sprite_top
            self.vel.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        if self.pos.x > CANVAS_WIDTH - self.sprite_number_r_and_l and i.current_screen == 1:
            i.switch_screen()
            self.pos.x = 0 
        elif self.pos.x > CANVAS_WIDTH - self.sprite_number_r_and_l and i.current_screen == 2:
            self.pos.x = CANVAS_WIDTH - self.sprite_number_r_and_l

        if self.pos.x < 0 and i.current_screen == 1:
            self.pos.x = 0
        elif self.pos.x < 0 and i.current_screen == 2:
            i.switch_screen()
            self.pos.x = CANVAS_WIDTH  


        for platform in platforms:
            if self.vel.x > 0 and self.pos.x + self.sprite_number_r_and_l  >= platform.edge_l and \
                self.pos.x - self.sprite_number_r_and_l  < platform.edge_l and \
                self.pos.y + self.sprite_bottom > platform.y and \
                self.pos.y - self.sprite_top < platform.y + platform.height:
                self.pos.x = platform.edge_l - self.sprite_number_r_and_l
            elif self.vel.x < 0 and self.pos.x - self.sprite_number_r_and_l <= platform.edge_r and \
                    self.pos.x + self.sprite_number_r_and_l > platform.edge_r and \
                    self.pos.y + self.sprite_bottom > platform.y and \
                    self.pos.y - self.sprite_top  < platform.y + platform.height:
                self.pos.x = platform.edge_r + self.sprite_number_r_and_l 
            if self.pos.y - self.sprite_top  < platform.edge_b and \
                self.pos.y + self.vel.y - self.sprite_bottom > platform.y and \
                self.pos.x + self.sprite_number_r_and_l > platform.edge_l and \
                self.pos.x - self.sprite_number_r_and_l  < platform.edge_r:
                    self.pos.y = platform.edge_b + self.sprite_top
                    self.vel.y = 0  
                    self.on_ground = True 
            elif self.vel.y > 0 and self.pos.y - self.sprite_top  <= platform.edge_t and \
                    self.pos.y + self.sprite_bottom > platform.edge_t and \
                    self.pos.x + self.sprite_number_r_and_l  > platform.edge_l and \
                    self.pos.x - self.sprite_number_r_and_l < platform.edge_r:
                self.pos.y = platform.edge_t - self.sprite_bottom 
                self.vel.y = 0
                self.on_ground = True
                if (self.pos.x + self.sprite_number_r_and_l > platform.edge_l and \
                    self.pos.x - self.sprite_number_r_and_l < platform.edge_r):
                    self.on_ground = True

        
        for trap in traps:
            if self.pos.y - self.sprite_top <= trap.edge_t and \
                    self.pos.y + self.sprite_bottom  > trap.edge_t and \
                    self.pos.x + self.sprite_number_r_and_l > trap.edge_l and \
                    self.pos.x - self.sprite_number_r_and_l < trap.edge_r:
                self.pos.y = trap.edge_t - self.sprite_bottom
                self.vel.y = 0
                self.on_ground = False
                self.can_move = False
                self.moving_left = False  
                self.moving_right = False 
                self.death()
                break
        else:  
            self.can_move = True

     
        for coin in coins:
            distance = (self.pos.x - coin.x) ** 2 + (self.pos.y - coin.y) ** 2
            if distance <= (coin.radius + self.sprite_number_r_and_l) ** 2:
                coins.remove(coin)
                coin_sound.play()
                break

        finish_line_left = 680
        finish_line_right = 680 + finish_line.get_width() / 3
        finish_line_top = 50
        finish_line_bottom = 50 + finish_line.get_height() / 3

        if self.pos.x - self.sprite_number_r_and_l <= finish_line_right and \
                self.pos.x + self.sprite_number_r_and_l >= finish_line_left and \
                self.pos.y + self.sprite_bottom >= finish_line_top and \
                self.pos.y - self.sprite_top <= finish_line_bottom:
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  
            self.moving_right = False  
            return

        if self.pos.x + self.sprite_number_r_and_l >= finish_line_left and \
                self.pos.x - self.sprite_number_r_and_l <= finish_line_right and \
                self.pos.y + self.sprite_bottom >= finish_line_top and \
                self.pos.y - self.sprite_top <= finish_line_bottom:
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  
            self.moving_right = False 
            return

        if self.pos.y - self.sprite_top <= finish_line_bottom and \
                self.pos.y + self.sprite_bottom >= finish_line_top and \
                self.pos.x + self.sprite_number_r_and_l >= finish_line_left and \
                self.pos.x - self.sprite_number_r_and_l <= finish_line_right:
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  
            self.moving_right = False  
            return
    
    def set(self, new_frame_index, new_modulo):
        self.frame_index = new_frame_index
        self.modulo = new_modulo


    def jump(self):
        if self.on_ground:
            jump_sound.play()
            self.vel.y = -7  
            self.image = sprite
            self.set([0,2], 3)

    def start_move_left(self):
        if self.can_move: 
            self.moving_left = True
            self.image = sprite_inverted
            self.set([0,1], 8)

    def stop_move_left(self):
        self.moving_left = False
        self.image = sprite
        self.set([0,0], 5)

    def start_move_right(self):
        if self.can_move:  
            self.moving_right = True
            self.image = sprite
            self.set([0,0], 8)

    def stop_move_right(self):
        self.moving_right = False 
        self.image = sprite
        self.set([0,0], 5)        

    def death(self):
        self.die = True
        self.image = sprite
        self.set([0, 7], 6)
    
class Clock():
        def __init__(self):
            self.time = 0

        def tick(self):
            self.time += 1

        def transition(self, frame_duration):
            return self.time % frame_duration == 0
       

class Interaction:
    def __init__(self, platformsONE, platformsTWO, player, clock, trapsONE, trapsTWO, coinsONE, coinsTWO, block_pos):
        self.player = player
        self.clock = clock
        self.platformsONE = platformsONE
        self.platformsTWO = platformsTWO
        self.trapsONE = trapsONE
        self.trapsTWO = trapsTWO
        self.coinsONE = coinsONE
        self.coinsTWO = coinsTWO
        self.current_screen = 1  
        self.game_over = False  
        self.coin_count = 0 
        self.initial_coins_len = len(self.coinsONE) + len(self.coinsTWO)
        self.block_pos = Vector(platformsONE[0].width /2  , 500)

        self.pause_btn_img = 'https://i.ibb.co/LkHqxxz/pause-btn.jpg'
        self.paused_screen_img = 'https://i.ibb.co/ZdXM7LN/paused-screen.png'
        self.play_btn_img = 'https://i.ibb.co/KFG5ms3/play-btn.jpg' 
        self.exit_btn_img = 'https://i.ibb.co/r29NXsx/exit-btn.jpg'
        self.reset_btn_img = 'https://i.ibb.co/p08zvqP/reset-btn.jpg'
        self.next_lvl_btn_img = 'https://i.ibb.co/5cyXJTm/next-lvl-btn.jpg'

        self.pause_btn = None
        self.paused_screen = None
        self.play_btn = None 
        self.exit_btn = None
        self.reset_btn = None
        self.next_lvl_btn = None

        self.lvl3_bg = 'https://i.ibb.co/f80DvZw/lvl3-bg.jpg'
        self.finish_line = simplegui.load_image('https://i.ibb.co/7vHknZT/finish-line.png')
        self.level_complete_img = simplegui.load_image('https://i.ibb.co/X37pXc9/level-complete.png')
        self.game_over_img = simplegui.load_image('https://i.ibb.co/tK8VgNP/game-over.png')
        self.arrow = 'https://i.ibb.co/dpD9wZW/arrow.png'
        self.this_way = 'https://i.ibb.co/ZdhjPNJ/this-way.png'

    def reset(self, platformsONE, platformsTWO, player, clock, trapsONE, trapsTWO, coinsONE, coinsTWO, block_pos):
        self.__init__(platformsONE, platformsTWO, player, clock, trapsONE, trapsTWO, coinsONE, coinsTWO, block_pos)

    def update(self):
        if self.current_screen == 1:
            self.player.update(self.platformsONE, self.trapsONE, self.coinsONE, self.finish_line, self.clock)
        elif self.current_screen == 2:
            self.player.update(self.platformsTWO, self.trapsTWO, self.coinsTWO, self.finish_line, self.clock)
        
        if not self.player.can_move and player.level_complete == False:
            self.game_over = True

        self.coin_count = self.initial_coins_len - len(self.coinsONE) - len(self.coinsTWO)

        
    def draw(self, canvas):
        draw_image(canvas, self.lvl3_bg, 450, 300, 900, 600)
        self.update()

        self.clock.tick()
        if self.clock.transition(10):
            self.player.next_frame()

        self.player.draw(canvas)

        if not self.game_over:
            self.pause_btn = draw_button(canvas, self.pause_btn_img, 770, 20, 50, 50)
            if self.coin_count == self.initial_coins_len and self.current_screen == 2:
                canvas.draw_image(self.finish_line, (self.finish_line.get_width()/2, self.finish_line.get_height()/2), 
                                  (self.finish_line.get_width(), self.finish_line.get_height()), (680, 50), 
                                  (self.finish_line.get_width()/4, self.finish_line.get_height()/4))
        if self.current_screen == 1 and not self.game_over:
            draw_image(canvas, self.arrow, 690, 155, 200/1.5, 200/1.5)
            draw_image(canvas, self.this_way, 700, 220, 500/2.5, 100/2.5)

        if self.current_screen == 1:
            for platform in self.platformsONE:
                platform.draw(canvas)
            for trap in self.trapsONE:
                trap.draw(canvas)
            for coin in self.coinsONE:
                coin.draw(canvas)
        elif self.current_screen == 2:
            canvas.draw_circle([80, 65], 20, 3, 'Yellow', 'Orange')
            canvas.draw_text("^^ Don't forget this coin! ^^", (10, 140), 15, "White", "monospace")
            for trap in self.trapsTWO:
                trap.draw(canvas)
            for platform in self.platformsTWO:
                platform.draw(canvas)
            for coin in self.coinsTWO:
                coin.draw(canvas)

        canvas.draw_text("Coins collected: " + str(self.coin_count) + "/" + str(self.initial_coins_len), (350, 40), 20, "White", "monospace") 
        if self.coin_count != self.initial_coins_len:
            canvas.draw_text("Collect all coins to finish level", (270, 20), 20, "White", "monospace")
        else:
            canvas.draw_text("All coins collected, reach finish line", (255, 20), 20, "White", "monospace")
    
    
        if self.game_over:
            self.exit_btn = draw_button(canvas, self.exit_btn_img, 255, 420, 500/2, 200/2)
            self.reset_btn = draw_button(canvas, self.reset_btn_img, 555, 420, 500/5, 500/5)
            canvas.draw_image(self.game_over_img, (self.game_over_img.get_width()/2, self.game_over_img.get_height()/2), 
                              (self.game_over_img.get_width(), self.game_over_img.get_height()), (450, 200), 
                              (self.game_over_img.get_width(), self.game_over_img.get_height()))
            canvas.draw_text("LOL!!!", (50, 50), 50, "Red", "monospace")
            game_over_sound.play()
        
        if player.level_complete:
            self.next_lvl_btn = draw_button(canvas, self.next_lvl_btn_img, 255, 420, 500/2, 200/2)
            self.reset_btn = draw_button(canvas, self.reset_btn_img, 555, 420, 500/5, 500/5)
            canvas.draw_image(self.level_complete_img, (self.level_complete_img.get_width()/2, self.level_complete_img.get_height()/2), 
                              (self.level_complete_img.get_width(), self.level_complete_img.get_height()), (450, 260), 
                              (self.level_complete_img.get_width(), self.level_complete_img.get_height()))

    def drawTWO(self, canvas):
        self.paused_screen = draw_image(canvas, self.paused_screen_img, 450, 300, 900, 600)
        self.play_btn = draw_button(canvas, self.play_btn_img, 500, 450, 250, 100)
        self.exit_btn = draw_button(canvas, self.exit_btn_img, 150, 450, 250, 100)

    
    def reset_game(self):
        self.player.reset(self.block_pos, sprite)
        self.coinsONE = [
            Coin((64,33), 20, 3),
            Coin((364,273), 20, 3),
            Coin((770,273), 20, 3),
            Coin((650,45), 20, 3),
            Coin((660,540), 20, 3),
        ]
        self.coinsTWO = [
            Coin((265,320), 20, 3),
            Coin((428,395), 20, 3),
            Coin((810,245), 20, 3),
            Coin((850,574), 20, 3),
        ]
        self.reset(self.platformsONE, self.platformsTWO, self.player, self.clock,  self.trapsONE, self.trapsTWO, self.coinsONE, self.coinsTWO, self.block_pos)


    def handle_mouse_click(self, pos, frame, draw, drawTWO):
        if self.pause_btn.is_clicked(pos):
            frame.set_draw_handler(drawTWO)
        if self.next_lvl_btn is not None and self.next_lvl_btn.is_clicked(pos):
            import level4
            frame.set_draw_handler(level4.i.draw)
            frame.set_keydown_handler(level4.keydown)
            frame.set_keyup_handler(level4.keyup)
            frame.set_mouseclick_handler(lambda pos: level4.click(pos, frame))     
        if self.exit_btn is not None and self.exit_btn.is_clicked(pos):
            self.reset_game()  
            import levels
            frame.set_draw_handler(levels.draw)
            frame.set_mouseclick_handler(lambda pos: levels.click(pos, frame))      
        if self.reset_btn is not None and self.reset_btn.is_clicked(pos):
            self.reset_game()
        if self.play_btn is not None and self.play_btn.is_clicked(pos):
            frame.set_draw_handler(draw)

    def switch_screen(self):
        if self.current_screen == 1:
            self.current_screen = 2
        elif self.current_screen == 2:
            self.current_screen = 1

            
platformsONE = [
    Platform((2, 563), 250, 35),
    Platform((350, 470), 50, 20),
    Platform((495, 563), 200, 35),
    Platform((220, 380), 50, 50),
    Platform((0, 295), 190, 35),
    Platform((320, 295), 170, 35),
    Platform((110, 220), 50, 40),
    Platform((200, 130), 170, 35),
    Platform((750, 295), 20, 20),
    Platform((500, 70), 170, 35),
    Platform((675, 1), 35, 104),
    Platform((55, 55), 20, 20),
]

platformsTWO = [
    Platform((145, 350), 130, 30),
    Platform((405, 420), 40, 40),
    Platform((790, 548), 20, 50),
    Platform((850, 508), 50, 20),
    Platform((790, 418), 50, 20),
    Platform((380, 260), 130, 30),
    Platform((850, 350), 50, 20),
    Platform((770, 270), 70, 20),
    Platform((270, 168), 130, 30),
    Platform((30, 90), 200, 30),
    Platform((7, 1), 20, 120),
    Platform((30, -32), 200, 30),
    Platform((560, 90), 315, 30),
    Platform((878, 1), 20, 120),
    Platform((560, -32), 315, 30),
    Platform((900, 1), 20, CANVAS_HEIGHT),
]

block_pos = Vector(platformsONE[0].width /2, 500)

trapsONE = [
    Trap(12, (276, 600), 39, 40),  
    Trap(10, (723, 600), 39, 40),  
    Trap(2, (550, 68), 30, 15),
]

trapsTWO = [
    Trap(40, (2, 600), 40, 40), 
    Trap(11, (30, 120), 30, 31),  
]

coinsONE = [
    Coin((64,33), 20, 3),
    Coin((364,273), 20, 3),
    Coin((770,273), 20, 3),
    Coin((650,45), 20, 3),
    Coin((660,540), 20, 3),
]

coinsTWO = [
    Coin((265,320), 20, 3),
    Coin((428,395), 20, 3),
    Coin((810,245), 20, 3),
    Coin((850,574), 20, 3),
]

player = Player(block_pos, sprite)

clock = Clock()

i = Interaction(platformsONE, platformsTWO, player, clock, trapsONE, trapsTWO, coinsONE, coinsTWO, block_pos)


def keydown(key):
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["up"]:
        player.jump()
    elif key == simplegui.KEY_MAP["a"] or key == simplegui.KEY_MAP["left"]:
        player.start_move_left()
    elif key == simplegui.KEY_MAP["d"] or key == simplegui.KEY_MAP["right"]:
        player.start_move_right()


def keyup(key):
    if key == simplegui.KEY_MAP["a"] or key == simplegui.KEY_MAP["left"]:
        player.stop_move_left()
    elif key == simplegui.KEY_MAP["d"] or key == simplegui.KEY_MAP["right"]:
        player.stop_move_right()


def click(pos, frame):
    i.handle_mouse_click(pos, frame, i.draw, i.drawTWO) 


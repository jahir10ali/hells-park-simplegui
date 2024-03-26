try: 
    import simplegui 
except ImportError: 
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import Vector

#import simplegui
#from user305_o32FtUyCKk_0 import Vector

# Constants
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 600
PLAYER_SIZE = 30
GRAVITY = Vector(0, 0.25)
FLOOR_Y = CANVAS_HEIGHT - PLAYER_SIZE / 2  # Y-coordinate of the floor


troll_face = simplegui.load_image('https://i.ibb.co/q0nG6Qd/troll-face.png')
game_over_sound = simplegui.load_sound('https://audio.jukehost.co.uk/4rXY9bKqh9LnxFndLGst7Xs9U9YpKr9b')
#troll_laugh = simplegui.load_sound('https://audio.jukehost.co.uk/AbmCCtjkcbKmoolGFCixHvlik4zfDVES')
game_over_sound.set_volume(0.2)
coin_sound = simplegui.load_sound('https://audio.jukehost.co.uk/UeryrWle3hDSLEgIqrA2zyNG0mNqX15F')
jump_sound = simplegui.load_sound('https://audio.jukehost.co.uk/849X7g5DQKqnC6dGOuU1asWeUx4D1GUy')

arrow = simplegui.load_image('https://cdn1.iconfinder.com/data/icons/pixel-game/110/pixel-39-512.png')




class Platform:
    def __init__(self, position, width, height):
        self.x, self.y = position
        self.width = width
        self.height = height
        self.edge_l = self.x  # Left edge of the platform
        self.edge_r = self.x + self.width  # Right edge of the platform
        self.edge_b = self.y + self.height  # Bottom edge of the platform
        self.edge_t = self.y  # Top edge of the platform

    def draw(self, canvas):
        canvas.draw_polygon([(self.x, self.y),
                             (self.x + self.width, self.y),
                             (self.x + self.width, self.y + self.height),
                             (self.x, self.y + self.height)],
                            4, '#1FB016', '#915518')

    def hit(self, player):
        return player.offset_l() <= self.edge_r and player.offset_r() >= self.edge_l \
            and player.offset_t() <= self.edge_b and player.offset_b() >= self.edge_t

    

class Trap:
    def __init__(self, spikes_quantity, position, width, height):
        self.spikes = []
        self.width = width
        self.height = height
        self.edge_l = position[0] - width / 2  # Left edge of the trap
        self.edge_r = position[0] + (width / 2 * spikes_quantity)  # Right edge of the trap
        self.edge_b = position[1]  # Bottom edge of the trap
        self.edge_t = position[1] - height  # Top edge of the trap
        
        # Calculate spike positions
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

        

class Monster:
    def __init__(self, pos, width):
        self.pos = pos
        self.width = width
        self.move_speed = 2  # Default movement speed
        self.direction = 1  # Initially moving right
        self.original_x = pos[0]
        self.distance_traveled = 0
        self.MAX_DISTANCE = 100  # Maximum distance to travel in one direction

    def move(self):
        x, y = self.pos
        x += self.move_speed * self.direction
        self.pos = (x, y)
        self.distance_traveled += abs(self.move_speed)  # Increment distance traveled
        if self.distance_traveled >= self.MAX_DISTANCE:
            self.direction *= -1  # Reverse direction
            self.distance_traveled = 0  # Reset distance traveled

    def draw(self, canvas):
        x, y = self.pos
        canvas.draw_polygon([(x - self.width / 2, y - self.width / 2),
                             (x + self.width / 2, y - self.width / 2),
                             (x + self.width / 2, y + self.width / 2),
                             (x - self.width / 2, y + self.width / 2)], 1, 'White')

class UpDownMonster:
    def __init__(self, pos, width):
        self.pos = pos
        self.width = width
        self.speed = 2.5  # Default movement speed
        self.direction = 1  # Initially moving down
        self.original_y = pos[1]
        self.distance_traveled = 0
        self.MAX_DISTANCE = 170  # Maximum distance to travel in one direction

    def move(self):
        x, y = self.pos
        y += self.speed * self.direction
        self.pos = (x, y)
        self.distance_traveled += abs(self.speed)  # Increment distance traveled
        if self.distance_traveled >= self.MAX_DISTANCE:
            self.direction *= -1  # Reverse direction
            self.distance_traveled = 0  # Reset distance traveled

    def draw(self, canvas):
        x, y = self.pos
        canvas.draw_polygon([(x - self.width / 2, y - self.width / 2),
                             (x + self.width / 2, y - self.width / 2),
                             (x + self.width / 2, y + self.width / 2),
                             (x - self.width / 2, y + self.width / 2)], 1, 'White') 
       
        
class Player:
    def __init__(self, pos):
        self.pos = pos
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.vel = Vector(0, 0)
        self.on_ground = True
        self.moving_left = False
        self.moving_right = False
        self.can_move = True
        self.level_complete = False


    def draw(self, canvas):
        canvas.draw_polygon([(self.pos.x - PLAYER_SIZE / 2, self.pos.y - PLAYER_SIZE / 2),
                             (self.pos.x + PLAYER_SIZE / 2, self.pos.y - PLAYER_SIZE / 2),
                             (self.pos.x + PLAYER_SIZE / 2, self.pos.y + PLAYER_SIZE / 2),
                             (self.pos.x - PLAYER_SIZE / 2, self.pos.y + PLAYER_SIZE / 2)],
                            1, "Red", "Red")
        

    def update(self, platforms, traps, coins, finish_line, monsters, up_down_monsters):
        self.vel += GRAVITY
        # Adjust velocity based on movement direction
        if self.moving_left:
            self.vel.x = -5
        elif self.moving_right:
            self.vel.x = 5
        else:
            self.vel.x = 0
            
        self.pos += self.vel
        
        # Check if player hits the floor
        if self.pos.y >= FLOOR_Y:
            self.pos.y = FLOOR_Y
            self.vel.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
          
        
        # Ensure player stays within canvas bounds
        # Check if player hits the right edge of the screen
        if self.pos.x > CANVAS_WIDTH:
            self.pos.x = CANVAS_WIDTH 
        # Check if player hits the left edge of the screen
        if self.pos.x < PLAYER_SIZE / 2:
            self.pos.x = PLAYER_SIZE / 2


        # Check for collisions with platforms
        for platform in platforms:
            # Collision with left side of the platform
            if self.vel.x > 0 and self.pos.x + self.width / 2 >= platform.edge_l and \
                self.pos.x - self.width / 2 < platform.edge_l and \
                self.pos.y + self.height / 2 > platform.y and \
                self.pos.y - self.height / 2 < platform.y + platform.height:
                self.pos.x = platform.edge_l - self.width / 2
            # Collision with right side of the platform
            elif self.vel.x < 0 and self.pos.x - self.width / 2 <= platform.edge_r and \
                    self.pos.x + self.width / 2 > platform.edge_r and \
                    self.pos.y + self.height / 2 > platform.y and \
                    self.pos.y - self.height / 2 < platform.y + platform.height:
                self.pos.x = platform.edge_r + self.width / 2
            # Collision with bottom of the platform
            if self.pos.y - self.height / 2 < platform.edge_b and \
                self.pos.y + self.vel.y - self.height / 2 > platform.y and \
                self.pos.x + self.width / 2 > platform.edge_l and \
                self.pos.x - self.width / 2 < platform.edge_r:
                    # Collision with bottom of the platform
                    self.pos.y = platform.edge_b + self.height / 2  # Move player to just above the platform's bottom edge
                    self.vel.y = 0  # Stop vertical movement
                    self.on_ground = True  # Set player on ground after collision
            # Collision with top of the platform
            elif self.vel.y > 0 and self.pos.y - self.height / 2 <= platform.edge_t and \
                    self.pos.y + self.height / 2 > platform.edge_t and \
                    self.pos.x + self.width / 2 > platform.edge_l and \
                    self.pos.x - self.width / 2 < platform.edge_r:
                self.pos.y = platform.edge_t - self.height / 2
                self.vel.y = 0
                self.on_ground = True
                # Additional condition to prevent interference with left/right edge collision
                if (self.pos.x + self.width / 2 > platform.edge_l and \
                    self.pos.x - self.width / 2 < platform.edge_r):
                    self.on_ground = True

        
        # Check for collisions with traps
        for trap in traps:
            # Collision with top of the trap
            if self.pos.y - self.height / 2 <= trap.edge_t and \
                    self.pos.y + self.height / 2 > trap.edge_t and \
                    self.pos.x + self.width / 2 > trap.edge_l and \
                    self.pos.x - self.width / 2 < trap.edge_r:
                self.pos.y = trap.edge_t - self.height / 2
                self.vel.y = 0
                self.on_ground = False
                self.can_move = False
                self.moving_left = False  # Stop horizontal movement
                self.moving_right = False  # Stop horizontal movement
                break
        else:  # No collision with trap's top edge
            self.can_move = True

        # Check for collisions with coins
        for coin in coins:
            distance = (self.pos.x - coin.x) ** 2 + (self.pos.y - coin.y) ** 2
            if distance <= (coin.radius + self.width / 2) ** 2:
                coins.remove(coin)
                coin_sound.play()
                break
                
        
        # Check for collisions with finish line
        finish_line_left = 830
        finish_line_right = 830 + finish_line.get_width() / 3
        finish_line_top = 35
        finish_line_bottom = 35 + finish_line.get_height() / 3

        # Collision with left edge of finish line
        if self.pos.x - self.width / 2 <= finish_line_right and \
                self.pos.x + self.width / 2 >= finish_line_left and \
                self.pos.y + self.height / 2 >= finish_line_top and \
                self.pos.y - self.height / 2 <= finish_line_bottom:
            # Handle collision with left edge
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  # Stop horizontal movement
            self.moving_right = False  # Stop horizontal movement
            return

        # Collision with right edge of finish line
        if self.pos.x + self.width / 2 >= finish_line_left and \
                self.pos.x - self.width / 2 <= finish_line_right and \
                self.pos.y + self.height / 2 >= finish_line_top and \
                self.pos.y - self.height / 2 <= finish_line_bottom:
            # Handle collision with right edge
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  # Stop horizontal movement
            self.moving_right = False  # Stop horizontal movement
            return

        # Collision with top edge of finish line
        if self.pos.y - self.height / 2 <= finish_line_bottom and \
                self.pos.y + self.height / 2 >= finish_line_top and \
                self.pos.x + self.width / 2 >= finish_line_left and \
                self.pos.x - self.width / 2 <= finish_line_right:
            # Handle collision with top edge
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  # Stop horizontal movement
            self.moving_right = False  # Stop horizontal movement
            return
        
        
        # Check for collisions with monsters
        for monster in monsters:
            # Collision with left side of the monster block
            if self.vel.x > 0 and self.pos.x + self.width / 2 >= monster.pos[0] - monster.width / 2 and \
                    self.pos.x - self.width / 2 < monster.pos[0] - monster.width / 2 and \
                    self.pos.y + self.height / 2 > monster.pos[1] - monster.width / 2 and \
                    self.pos.y - self.height / 2 < monster.pos[1] + monster.width / 2:
                # Handle collision with left side of the monster block
                # Adjust player position or perform other actions as needed
                pass
            # Collision with right side of the monster block
            elif self.vel.x < 0 and self.pos.x - self.width / 2 <= monster.pos[0] + monster.width / 2 and \
                    self.pos.x + self.width / 2 > monster.pos[0] + monster.width / 2 and \
                    self.pos.y + self.height / 2 > monster.pos[1] - monster.width / 2 and \
                    self.pos.y - self.height / 2 < monster.pos[1] + monster.width / 2:
                # Handle collision with right side of the monster block
                # Adjust player position or perform other actions as needed
                pass
            # Collision with top of the monster block
            if self.pos.y - self.height / 2 <= monster.pos[1] + monster.width / 2 and \
                    self.pos.y + self.vel.y - self.height / 2 > monster.pos[1] + monster.width / 2 and \
                    self.pos.x + self.width / 2 > monster.pos[0] - monster.width / 2 and \
                    self.pos.x - self.width / 2 < monster.pos[0] + monster.width / 2:
                # Handle collision with top of the monster block
                # Adjust player position or perform other actions as needed
                pass
            # Collision with bottom of the monster block
            elif self.vel.y > 0 and self.pos.y - self.height / 2 <= monster.pos[1] - monster.width / 2 and \
                    self.pos.y + self.height / 2 > monster.pos[1] - monster.width / 2 and \
                    self.pos.x + self.width / 2 > monster.pos[0] - monster.width / 2 and \
                    self.pos.x - self.width / 2 < monster.pos[0] + monster.width / 2:
                # Handle collision with bottom of the monster block
                # Adjust player position or perform other actions as needed
                pass
         
        
        # Check for collisions with up_down_monsters
        for monster in up_down_monsters:
            # Collision with left side of the monster block
            if self.vel.x > 0 and self.pos.x + self.width / 2 >= monster.pos[0] - monster.width / 2 and \
                    self.pos.x - self.width / 2 < monster.pos[0] - monster.width / 2 and \
                    self.pos.y + self.height / 2 > monster.pos[1] - monster.width / 2 and \
                    self.pos.y - self.height / 2 < monster.pos[1] + monster.width / 2:
                # Handle collision with left side of the monster block
                # Adjust player position or perform other actions as needed
                self.on_ground = False
                self.can_move = False
                self.moving_left = False  # Stop horizontal movement
                self.moving_right = False  # Stop horizontal movement
                break
            # Collision with right side of the monster block
            elif self.vel.x < 0 and self.pos.x - self.width / 2 <= monster.pos[0] + monster.width / 2 and \
                    self.pos.x + self.width / 2 > monster.pos[0] + monster.width / 2 and \
                    self.pos.y + self.height / 2 > monster.pos[1] - monster.width / 2 and \
                    self.pos.y - self.height / 2 < monster.pos[1] + monster.width / 2:
                # Handle collision with right side of the monster block
                # Adjust player position or perform other actions as needed
                self.on_ground = False
                self.can_move = False
                self.moving_left = False  # Stop horizontal movement
                self.moving_right = False  # Stop horizontal movement
                break
            # Collision with top of the monster block
            if self.pos.y - self.height / 2 <= monster.pos[1] + monster.width / 2 and \
                    self.pos.y + self.vel.y - self.height / 2 > monster.pos[1] + monster.width / 2 and \
                    self.pos.x + self.width / 2 > monster.pos[0] - monster.width / 2 and \
                    self.pos.x - self.width / 2 < monster.pos[0] + monster.width / 2:
                # Handle collision with top of the monster block
                # Adjust player position or perform other actions as needed
                pass
            # Collision with bottom of the monster block
            elif self.vel.y > 0 and self.pos.y - self.height / 2 <= monster.pos[1] - monster.width / 2 and \
                    self.pos.y + self.height / 2 > monster.pos[1] - monster.width / 2 and \
                    self.pos.x + self.width / 2 > monster.pos[0] - monster.width / 2 and \
                    self.pos.x - self.width / 2 < monster.pos[0] + monster.width / 2:
                # Handle collision with bottom of the monster block
                # Adjust player position or perform other actions as needed
                self.on_ground = False
                self.can_move = False
                self.moving_left = False  # Stop horizontal movement
                self.moving_right = False  # Stop horizontal movement
                break



    def jump(self):
        if self.on_ground:
            jump_sound.play()
            self.vel.y = -7  # Adjust jump strength as needed

    def start_move_left(self):
        if self.can_move:  # Check if the player is allowed to move
            self.moving_left = True

    def stop_move_left(self):
        self.moving_left = False

    def start_move_right(self):
        if self.can_move:  # Check if the player is allowed to move
            self.moving_right = True

    def stop_move_right(self):
        self.moving_right = False

        
        
        
frame = simplegui.create_frame("Block Wall", CANVAS_WIDTH, CANVAS_HEIGHT)           
       

class Interaction:
    def __init__(self, platforms, player, traps, coins, monsters, up_down_monsters):
        self.player = player
        self.platforms = platforms
        self.traps = traps
        self.coins = coins
        self.monsters = monsters
        self.up_down_monsters = up_down_monsters
        self.game_over = False  # Flag to track if game over
        self.coin_count = 0  # Counter for collected coins
        self.initial_coins_len = len(self.coins)
        self.finish_line = simplegui.load_image('https://i.ibb.co/7vHknZT/finish-line.png')
        self.level_complete_img = simplegui.load_image('https://i.ibb.co/X37pXc9/level-complete.png')
        self.game_over_img = simplegui.load_image('https://i.ibb.co/tK8VgNP/game-over.png')
        


    def update(self):
        self.player.update(self.platforms, self.traps, self.coins, self.finish_line, self.monsters, self.up_down_monsters)
        
        # Check for game over condition
        if not self.player.can_move and player.level_complete == False:
            self.game_over = True

        
        # Update coin count
        self.coin_count = self.initial_coins_len - len(self.coins)

        
    def draw(self, canvas):
        self.update()
        #if not player.level_complete:
            #canvas.draw_text('Jump from platform to platform!', (50,310), 20, 'White', 'monospace')
            #canvas.draw_text('Avoid the spikes or it is Game Over!', (262,520), 20, 'White', 'monospace')
            #canvas.draw_text('Collect all the coins!', (490,170), 20, 'White', 'monospace')
        if not self.game_over and self.coin_count == self.initial_coins_len:
            #self.pause_btn = draw_button(canvas, self.pause_btn_img, 30, 20, 50, 50)
            canvas.draw_image(self.finish_line, (self.finish_line.get_width()/2, self.finish_line.get_height()/2), 
                                  (self.finish_line.get_width(), self.finish_line.get_height()), (830, 35), 
                                  (self.finish_line.get_width()/5, self.finish_line.get_height()/5))
        self.player.draw(canvas)
        for platform in self.platforms:
            platform.draw(canvas)
        for trap in self.traps:
            trap.draw(canvas)
        for coin in self.coins:
            coin.draw(canvas)
        for monster in self.monsters:
            monster.draw(canvas)
            monster.move()
        for monster in self.up_down_monsters:
            monster.draw(canvas)
            monster.move()
        
        # Draw coin count
        #canvas.draw_text("Coins collected: " + str(self.coin_count) + "/" + str(self.initial_coins_len), (350, 40), 20, "White", "monospace") 
        #if self.coin_count != self.initial_coins_len:
            #canvas.draw_text("Collect all coins to finish level", (270, 20), 20, "White", "monospace")
        #else:
            #canvas.draw_text("All coins collected, reach finish line", (255, 20), 20, "White", "monospace")
    
    
        # Draw "Game Over" text if game over
        if self.game_over:
            canvas.draw_image(self.game_over_img, (self.game_over_img.get_width()/2, self.game_over_img.get_height()/2), 
                              (self.game_over_img.get_width(), self.game_over_img.get_height()), (450, 200), 
                              (self.game_over_img.get_width(), self.game_over_img.get_height()))
            canvas.draw_text("LOL!!!", (50, 50), 50, "Red", "monospace")
            canvas.draw_image(troll_face, (troll_face.get_width()/2, troll_face.get_height()/2), 
                              (troll_face.get_width(), troll_face.get_height()), (460, 360), 
                              (troll_face.get_width()/3, troll_face.get_height()/3))
            #game_over_sound.play()
        
        # Draw "Level Complete" text if level complete
        if player.level_complete:
            canvas.draw_image(self.level_complete_img, (self.level_complete_img.get_width()/2, self.level_complete_img.get_height()/2), 
                              (self.level_complete_img.get_width(), self.level_complete_img.get_height()), (450, 260), 
                              (self.level_complete_img.get_width(), self.level_complete_img.get_height()))
            #canvas.draw_text("Level Complete", (260, 230), 80, "Red", "monospace")




platforms = [
    Platform((10, 578), 100, 20),
    Platform((115, 533), 50, 65),
    Platform((230, 440), 100, 20), 
    Platform((420, 398), 50, 200), 
    Platform((760, 578), 120, 20), 
    Platform((865,500), 30, 60),
    Platform((790,420), 40, 40),
    Platform((850,340), 40, 40), 
    Platform((790,260), 40, 40), 
    Platform((515, 270), 30, 20),
    Platform((170, 270), 150, 20),
    Platform((50, 185), 60, 20),
    Platform((120, 100), 60, 20),
    Platform((300, 60), 60, 20),
    Platform((450, 60), 445, 20),
    Platform((0, -22), CANVAS_WIDTH, 20), # canvas ceiling using a platform
    Platform((900,0), 20, CANVAS_HEIGHT), # canvas edge using a platform
]


block_pos = Vector(platforms[0].width / 2, 500)

player = Player(block_pos)

traps = [
    Trap(13, (187, 600), 38, 40),
    #Trap(1, (310, 438), 38, 30),
    #Trap(13, (497, 600), 38, 40),
    #Trap(1, (840, 576), 36.5, 38),  
    #Trap(1, (260, 268), 38, 25),
    #Trap(1, (600, 58), 38, 15),
]


coins = [
    #Coin((139,505), 20, 3),
    #Coin((254,415), 20, 3),
    #Coin((780,553), 20, 3),
    #Coin((204,245), 20, 3),
    #Coin((154,75), 20, 3),
    #Coin((504,35), 20, 3),
]

# Instances of Monster class
monsters = [
    #Monster((150, 566), 50),
    #Monster((450, 480), 50),
]

# Instances of UpDownMonster class
up_down_monsters = [
    UpDownMonster((660, 320), 50),
    UpDownMonster((660, 120), 50),
]


i = Interaction(platforms, player, traps, coins, monsters, up_down_monsters)


# Define key handlers
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


        
    

# Set the draw handler to i.drawONE initially
frame.set_draw_handler(i.draw)

frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.start()

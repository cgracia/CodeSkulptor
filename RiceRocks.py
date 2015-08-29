# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

# more globals
ROCK_LIMIT = 12

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            image_center = list(self.image_center)
            image_center[0] += self.image_size[0]
        else:
            image_center = self.image_center
        canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, self.angle)
       
    def update(self):        
        forward_vector = angle_to_vector(self.angle)
        
        if self.thrust:
            self.vel[0] += 0.1 * forward_vector[0]
            self.vel[1] += 0.1 * forward_vector[1]
        
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
            
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
    def set_angle_vel(self, angle_vel):
        self.angle_vel = angle_vel
        
    def set_thrust(self, thrust):
        self.thrust = thrust
        if thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
           
    def shoot(self):
        global a_missile
        # Set velocity to a multiple of the forward vector plus the ship velocity
        forward = angle_to_vector(self.angle) 
        missile_vel = [self.vel[0] + 5 *forward[0], self.vel[1] + 5 * forward[1]]
        
        # Make the tip the starting position
        tip = [forward[0]*self.radius+self.pos[0],forward[1]*self.radius+self.pos[1]]
        
        missile_group.add(Sprite(tip, missile_vel, 0, 0, missile_image, missile_info, missile_sound))
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            image_center = [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]]
            canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        if self.age > self.lifespan:
            return True # remove
        else:
            return False
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def collide(self, other_object):
        if dist(self.get_position(), other_object.get_position()) < self.get_radius() + other_object.get_radius():
            return True
        else:
            return False
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        
# draw a group of sprites        
def process_sprite_group(canvas, s):
    sprites = set(s)
    for sprite in sprites:
        sprite.draw(canvas)
        if sprite.update():
            s.remove(sprite)
        
# collision between a group and another object
def group_collide(group, other_object):
    s = set(group)
    number_collisions = 0
    for item in s:
        if item.collide(other_object):            
            group.remove(item)
            number_collisions += 1
            explosion_group.add(Sprite(item.pos, [0, 0], 0, 0, explosion_image, explosion_info))
    return number_collisions        

def group_group_collide(group1, group2):
    items = set(group1)
    collisions = 0
    for item in items:
        n = group_collide(group2, item)
        if n > 0:
            collisions += n
            group1.remove(item)
    return collisions

def reset():
    global started, lives, score, rock_group
    started = False
    lives = 3
    score = 0
    soundtrack.rewind()
    soundtrack.play()
    rock_group = set([])
           
def draw(canvas):
    global time, started, lives, score
    
    # animate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    if group_collide(rock_group, my_ship) > 0:
        lives -= 1
        
    score += group_group_collide(missile_group, rock_group) * 10
    
    # draw lives and score
    canvas.draw_text("Lives", (50, 50), 30, "White")
    canvas.draw_text(str(lives), (50, 80), 30, "White")
    canvas.draw_text("Score", (WIDTH - 90, 50), 30, "White")
    canvas.draw_text(str(score), (WIDTH - 90, 80), 30, "White")
        
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
    if lives <= 0:
        reset()
            
# timer handler that spawns a rock    
def rock_spawner():
    if len(rock_group) < ROCK_LIMIT and started:
        pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        vel = [random.randrange(-100, 100)*.01, random.randrange(-100, 100)*.01]
        ang_vel = random.randrange(-80, 80)*.001
        if not (dist(pos, my_ship.pos) < my_ship.radius * 3):
            rock_group.add(Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info))

# Key handlers
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.set_angle_vel(-.1)
    if key == simplegui.KEY_MAP["right"]:
        my_ship.set_angle_vel(.1)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(True)        
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
   
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.set_angle_vel(0)
    if key == simplegui.KEY_MAP["right"]:
        my_ship.set_angle_vel(0)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(False)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
rock_group = set([])
missile_group = set([])
explosion_group = set([])
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

soundtrack.play()

# get things rolling
timer.start()
frame.start()

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Camera-related variables
camera_pos = (0,500,300)
# camera_pos = (0, 290, 100)

fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
point = 0
road_line_y = [-400, 200] # (y) as x and z = 0 always 
car_pos = 1
lane = [400, 0, -400]
obstacle_y = -600
obstacle_x = 0
game_over = False
police_pos = 1
police_y = 750
obstacle_speed = 2
cheat_mode = False
hit = 0
fp_view = False
bullets = []
bullet_speed = 10
bullet_hit_count = 0
total_bullet = 3
nightmare = False
nightmare_prev_speed = 0 
color = 0
wind_shield = 30
power_show = False 
power_x = 0
power_y = -600
power_obtained = False
power_prev_point = 0
obstacle_speed_prev = 0 
police_light_controller = 0
hole_x = random.choice(lane)
hole_y = -1800
hole_active = True
hole_hit = False
hole_timer = 0
hole_z_rise = 200 
sky_mode = "night"        # 'day' or 'night'
sky_transition = 1.0  
sky_color = [0, 0, 0, 1.0]
moon_sun_place = 200
moon_color = 1

def draw_circle(x, y, radius):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for angle in range(0, 361, 10):
        glVertex2f(x + radius * math.cos(math.radians(angle)),
                   y + radius * math.sin(math.radians(angle)))
    glEnd()


def draw_moon():
    glPushMatrix()
    glColor3f(1, 1, moon_color)
    glTranslatef(moon_sun_place, -300, 400) 
    gluSphere(gluNewQuadric(), 40, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()


def draw_clouds():
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(-0.6, 0.85, 0.07)
    draw_circle(-0.55, 0.87, 0.08)
    draw_circle(-0.5, 0.85, 0.07)

def draw_sky():
    global sky_transition, sky_color, moon_sun_place, moon_color
    draw_moon()
    # Set based on sky_mode directly
    if sky_mode == "day":
        for i in range(len(sky_color) -1):
            sky_color[i] += 0.005
            if(i == 0 and sky_color[i] >= 0.5): sky_color[i] = 0.5
            if(i == 1 and sky_color[i] >= 0.8): sky_color[i] = 0.8
            if(i == 2 and sky_color[i] >= 0.92): sky_color[i] = 0.92
            if(i == 3 and sky_color[i] >= 1): sky_color[i] = 1
        if(moon_sun_place >= -200):
            moon_sun_place -= 10
        if(moon_color >= 0):
            moon_color -= 1

    elif sky_mode == "night":
        
        for i in range(len(sky_color) -1):
            sky_color[i] -= 0.005
            if(sky_color[i] < 0.13):
                sky_color[i] = 0
        if(moon_sun_place <= 200):
            moon_sun_place += 10
        if(moon_color <= 1):
            moon_color += 1
    glClearColor(sky_color[0], sky_color[1],sky_color[2], 1.0)

    r = sky_transition * 0.53
    g = sky_transition * 0.81
    b = sky_transition * 0.92 + (1 - sky_transition) * 0.05

    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    glVertex2f(-1, 1)
    glVertex2f(1, 1)
    glVertex2f(1, 0)
    glVertex2f(-1, 0)
    glEnd()

    if sky_transition < 0.5:
        draw_moon()
    elif sky_transition > 0.8:
        draw_clouds()
    # glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    # glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
def draw_hole():
    if not hole_active:
        return
    glPushMatrix()
    glColor3f(0.05, 0.05, 0.05)
    glTranslatef(hole_x, hole_y, -1)
    gluDisk(gluNewQuadric(), 0, 50, 30, 1)
    glPopMatrix()

def power_showcase():
    glPushMatrix()
    glColor3f(0.8, 0.5, 0.1)
    glTranslatef(power_x, power_y, 0) 
    gluSphere(gluNewQuadric(), 40, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_road_surroundings():
    tree_shift = road_line_y[0]  
    tree_spacing = 300
    distance_from_road = 750  
    pole_offset = 800  
    bush_height = 20

    # Roadside Bushes
    glPushMatrix()
    glColor3f(0.0, 0.8, 0.0)
    glBegin(GL_QUADS)
    for x in [-distance_from_road, distance_from_road]:
        glVertex3f(x - 20, -600 + tree_shift, 0)
        glVertex3f(x + 20, -600 + tree_shift, 0)
        glVertex3f(x + 20, 800 + tree_shift, 0)
        glVertex3f(x - 20, 800 + tree_shift, 0)
    glEnd()
    glPopMatrix()

    # Roadside Trees
    for x in [-distance_from_road, distance_from_road]:
        for y in range(-600, 800, tree_spacing):
            # Trunk
            glPushMatrix()
            glColor3f(0.55, 0.27, 0.07)
            glTranslatef(x, y + tree_shift, 40)
            glScalef(20, 20, 120)
            glutSolidCube(1)
            glPopMatrix()

            # Leaves
            glPushMatrix()
            glColor3f(0.0, 0.6, 0.0)
            glTranslatef(x, y + tree_shift, 120)
            glScalef(60, 60, 60)
            glutSolidSphere(1, 10, 10)
            glPopMatrix()

    # Random Trash Bins
    # random.seed(0)
    for x in [-distance_from_road + 40, distance_from_road - 40]:
        for y in range(-500, 800, 600):
            glPushMatrix()
            glColor3f(0.4, 0.4, 0.4)
            glTranslatef(x, y + tree_shift, 15)
            glScalef(15, 15, 30)
            glutSolidCube(1)
            glPopMatrix()
    

    # Lampposts with lights
    lamp_positions = []
    for x in [-pole_offset, pole_offset]:
        for y in range(-600, 800, 400):
            y_shifted = y + tree_shift
            lamp_positions.append((x, y_shifted))

            # Pole
            glPushMatrix()
            glColor3f(0.7, 0.7, 0.7)
            glTranslatef(x, y_shifted, 60)
            glScalef(8, 8, 180)
            glutSolidCube(1)
            glPopMatrix()

            # Lamp Glow (Night Mode)
            glPushMatrix()
            glColor3f(1.0, 1.0, 0.5)
            glTranslatef(x, y_shifted, 130)
            glScalef(25, 25, 25)
            glutSolidCube(1)
            glPopMatrix()

    # Parabolic Electric Wires
    glColor3f(0.2, 0.4, 0.2) 
    for i in range(0, len(lamp_positions) - 2, 2):
        if lamp_positions[i][0] == lamp_positions[i + 2][0]:
            x = lamp_positions[i][0]
            y1 = lamp_positions[i][1]
            y2 = lamp_positions[i + 2][1]
            z_top = 130

            glBegin(GL_LINE_STRIP)
            for t in range(0, 101):
                t_norm = t / 100
                y = y1 + (y2 - y1) * t_norm
                z = z_top - 20 * math.sin(math.pi * t_norm) #center point
                glVertex3f(x, y, z)
            glEnd()
def move_and_draw_bullets():
    global bullets, obstacle_x, obstacle_y, bullet_hit_count

    new_bullets = []
    for bullet in bullets:
        bullet['y'] -= bullet_speed
        
        # Draw bullet
        glPushMatrix()
        glColor3f(1, 1, 1)
        glTranslatef(lane[car_pos], bullet['y'], bullet['z'])
        glutSolidSphere(10, 10, 10)
        glPopMatrix()
############################################################################################
        # Check for collision
        # if abs(bullet['x'] - obstacle_x) < 50 and abs(bullet['y'] - obstacle_y) < 50:
        #     bullet_hit_count += 1
        #     if bullet_hit_count == 3:
        #         obstacle_y = -600
        #         obstacle_x = random.choice([400, 0, -400])
        #         bullet_hit_count = 0
        #     continue 
        if(lane[car_pos] == obstacle_x  and  obstacle_y-500 <= bullet['y'] <= obstacle_y + 500):
            
            obstacle_y = -600
            obstacle_x = random.choice([400, 0, -400])
                
            continue 
        
       # Only keep bullets that are still on screen
        if bullet['y'] > -600:
            new_bullets.append(bullet)
            
    bullets = new_bullets

def update_hole():
    global hole_y, hole_x, game_over, hole_active, hole_hit, camera_pos, hole_timer, hit

    if game_over:
        return

    hole_y += obstacle_speed
    
    if hole_y > 800:
        hole_y = -1800
        hole_x = random.choice(lane)
        hole_hit = False
        hole_active = True

    if not hole_hit and lane[car_pos] == hole_x and 250 <= hole_y <= 350 and not cheat_mode and not power_obtained:
        hole_hit = True
        hole_active = False
        game_over = True  
        camera_pos = (camera_pos[0], camera_pos[1], camera_pos[2] + hole_z_rise)
        hole_timer = 30  
        hit = 2

def handle_hole_z_timer():
    global camera_pos, hole_timer
    if hole_timer > 0:
        hole_timer -= 1
    elif hole_timer == 0 and camera_pos[2] > 300:
        camera_pos = (camera_pos[0], camera_pos[1], 300)  
        hole_timer = -1  
            
    
            
def draw_police_car(x, y, z=0):
    # Roof lights
    glPushMatrix()
    glColor3f(0, 0, 1)  # Blue light
    glTranslatef(x - 20, y, z + 40)
    glScalef(10, 30, 10)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1, 1, 1)  # White light
    glTranslatef(x + 20, y, z + 40)
    glScalef(10, 30, 10)
    glutSolidCube(1)
    glPopMatrix()

def draw_obstacle_car(x, y, z=0):
    glPushMatrix()
    glColor3f(0, 1, 1)  # Cyan
    glTranslatef(x, y, z + 15)
    glScalef(100, 200, 30)
    glutSolidCube(1)
    glPopMatrix()

def keyboardListener(key, x, y):
    global sky_mode,sky_transition, total_bullet, cheat_mode,color, wind_shield, total_bullet, fp_view, camera_pos, nightmare_prev_speed, nightmare, point, road_line_y, car_pos, lane, obstacle_x, obstacle_y, police_pos, hit, obstacle_speed, police_y, game_over,  hole_x, hole_y, hole_active, hole_hit, hole_timer, hole_z_rise
    if(key == b"c"):
        cheat_mode = not cheat_mode
    if(key == b"f"):
        fp_view = not fp_view
    if(key == b"r" and game_over):
        camera_pos = (0,500,300)
        point = 0
        road_line_y = [-400, 200] # (y) as x and z = 0 always 
        car_pos = 1
        lane = [400, 0, -400]
        obstacle_y = -600
        obstacle_x = 0
        game_over = False
        police_pos = 1
        police_y = 750
        obstacle_speed = 1
        cheat_mode = False
        hit = 0
        fp_view = False
        bullets.clear()
        nightmare = False
        color = 0
        wind_shield = 30
        hole_x = random.choice(lane)
        hole_y = -1800
        hole_active = True
        hole_hit = False
        hole_timer = 0
        hole_z_rise = 200 
        total_bullet = 3
    elif key == b'b':
        sky_mode = "night"
        sky_transition = 0.0
    elif key == b'd':
        sky_mode = "day"
        if sky_transition < 1.0:
            sky_transition += 0.1
            if sky_transition > 1.0:
                sky_transition=1.0 
    
    if(key == b"n"):
        nightmare = not nightmare
        if(nightmare == True):
            nightmare_prev_speed = obstacle_speed
            obstacle_speed = 60
        else:
            obstacle_speed = nightmare_prev_speed
    if key == b' ':
        if(total_bullet > 0):
            car_x = lane[car_pos]
            bullets.append({'x': car_x, 'y': 300, 'z': 15})
            total_bullet -= 1
    


def specialKeyListener(key, x, y):
    if(game_over): return
    global car_pos
    if(key == GLUT_KEY_RIGHT):
        if(car_pos != 2):
            car_pos += 1
    if(key == GLUT_KEY_LEFT):
        if(car_pos != 0):
            car_pos -= 1
            

        


def setupCamera():
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    x, y, z = camera_pos
    # Position the camera and set its orientation
    if(fp_view):
        gluLookAt(x, y, z,  # Camera position
              lane[car_pos], 0, 0,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)
    else:
        gluLookAt(x, y, z,  # Camera position
              0, 0, 0,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)


def idle():
    glutPostRedisplay()

def change_line_y():
    if(game_over): return
    global road_line_y
    for i in range(len(road_line_y)):
        road_line_y[i] += obstacle_speed
        if(road_line_y[i] >= 600):
            road_line_y[i] = -600
def road_line():
    glPushMatrix()
    glColor3f(1, 1, 1)
    glTranslatef(0, road_line_y[0], 0)
    glScalef(30, 100, 2)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1, 1, 1)
    glTranslatef(0, road_line_y[1], 0)
    glScalef(30, 100, 2)
    glutSolidCube(1)
    glPopMatrix()

def wheel(x, y, z):
    glPushMatrix()
    glColor3f(0, 0, 0)  # black color
    glTranslatef(x, y, z)
    glRotatef(90, 0, 1, 0)

    quad = gluNewQuadric()
    # Draw wheel side (cylinder body)
    gluCylinder(quad, 30, 30, 20, 50, 10)  # radius, height, slices, stacks

    # Draw front face
    glPushMatrix()
    gluDisk(quad, 10, 30, 50, 1)  # inner radius (hole), outer radius
    glPopMatrix()

    # Draw back face
    glPushMatrix()
    glTranslatef(0, 0, 20)
    gluDisk(quad, 20, 30, 50, 1)
    glPopMatrix()

    gluDeleteQuadric(quad)
    glPopMatrix()

def car_show():
    # Player car (detailed sports car appearance)
    global camera_pos, wind_shield
    wheel(lane[car_pos] + 30, 250, -10)
    wheel(lane[car_pos] + 30, 350, -10)
    wheel(lane[car_pos] - 50, 250, -10)
    wheel(lane[car_pos] - 50, 350, -10)



    glPushMatrix()
    glTranslatef(lane[car_pos], 300, 0)
    
    # Main body
    glPushMatrix()
    glColor3f(0, 0.5, color)  
    glScalef(80, 160, 40)
    glutSolidCube(1)
    glPopMatrix()
    

    if(point >= 3):
        glPushMatrix()
        glColor3f(0, 0.4, color)  
        glTranslatef(0, 40, 30)
        glScalef(70, 60, 55)
        glutSolidCube(1)
        glPopMatrix()
        wind_shield = 55
    

    # Windshield
    glPushMatrix()
    glColor3f(0.7, 0.9, 1)  # Light blue glass
    glTranslatef(0, 40, wind_shield)
    glScalef(70, 60, 5)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()
    

    

    if(fp_view):
        camera_pos = (lane[car_pos], 290, 100)
    else:
        camera_pos = (0,500,300)

def back_light():
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(lane[car_pos], 375, 0)
    glScalef(4, 0, 1)
    glutSolidCube(20)
    glPopMatrix()

def front_light():
    glPushMatrix()
    glColor3f(0.3, 1, 0.5)
    glTranslatef(lane[car_pos] + 40, 230, 0)
    glRotatef(90, 1, 0, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 5, 40, 100, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.3, 1, 0.5)
    glTranslatef(lane[car_pos] - 40, 230, 0)
    glRotatef(90, 1, 0, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 5, 40, 100, 10, 10)
    glPopMatrix()
    

def random_obstacle():
    glPushMatrix()
    glColor3f(0, 1, 1)
    glTranslatef(obstacle_x, obstacle_y, 0)
    glutSolidCube(100)
    glPopMatrix()

def move_obstacle():
    global obstacle_y,obstacle_speed_prev,power_prev_point,power_x, hole_y, obstacle_x, point, game_over, hit, police_y, obstacle_speed, car_pos, color, power_show, power_y, power_obtained
    if(game_over): return
    if(obstacle_y >= 600):
        obstacle_x = random.choice([400, 0, -400])
        obstacle_y = -600
        point += 1
        if(color < 1):
            color += 0.03 
            if(color > 1):
                color = 1 

        if(point <= 220):
            obstacle_speed += 0.1
    else:
        obstacle_y += obstacle_speed
    
    if(obstacle_x == lane[car_pos] and 120 <= obstacle_y <= 250 and not power_obtained and not cheat_mode):
        obstacle_x = random.choice([400, 0, -400])
        obstacle_y = -600
        hit += 1
        if(hit == 1):
            police_y = 550
        elif(hit == 2):
            game_over = True 

    if(cheat_mode and 100 <= obstacle_y <= 119 and obstacle_x == lane[car_pos]):
        if(car_pos == 2):
            car_pos -= 1
        elif(car_pos == 1):
            car_pos += random.choice([1, -1])
        else: 
            car_pos += 1
        obstacle_y = 120

    if(cheat_mode and 50 <= hole_y <= 150 and hole_x == lane[car_pos]):
        if(car_pos == 2):
            car_pos -= 1
        elif(car_pos == 1):
            car_pos += random.choice([1, -1])
        else: 
            car_pos += 1
        hole_y = 120
    
    if(point % 5 == 0 and point != 0 and obstacle_speed_prev == 0):
        if(not power_show):
            power_show = True
            power_x = random.choice([400, 0, -400])
    
    if(power_show):
        power_showcase()
        power_y += 1.3
        if(power_y >= 600):
            power_show = False
            power_y = -600
        ##############################################################
    if(power_x == lane[car_pos] and 120 <= power_y <= 330):
        power_y = 631
        power_obtained = True
        obstacle_speed_prev = obstacle_speed
        power_prev_point = point
        obstacle_speed = 10
    
    if(power_obtained and power_prev_point + 7 == point):
        obstacle_speed = obstacle_speed_prev
        power_obtained = False
        obstacle_speed_prev = 0



        
        

def police_show():
    global police_light_controller
    police_light_controller += 1
    if(police_light_controller > 100): police_light_controller = 0

    # Police car (realistic design)
    wheel(lane[car_pos] -50, police_y -70, 0)
    wheel(lane[car_pos] + 40, police_y -70, 0)
    # draw_police_car(lane[police_pos], police_y)

    glPushMatrix()
    glTranslatef(lane[car_pos], police_y, 0)
    
    
    
    # Main body
    glPushMatrix()
    if(police_light_controller < 25):
        glColor3f(1, 0, 0)  # White base
    elif(police_light_controller < 50):
        glColor3f(0.9, 0.9, 0.9)  # White base
    elif(police_light_controller < 75):
        glColor3f(0, 0, 1)  
    else:
        glColor3f(0.9, 0.9, 0.9)  # White base

    glScalef(80, 160, 40)
    glutSolidCube(1)
    glPopMatrix()
    
    # Police stripe
    glPushMatrix()
    glColor3f(0, 0, 0.8)  # Blue stripe
    glTranslatef(0, 0, 25)
    glScalef(85, 30, 5)
    glutSolidCube(1)
    glPopMatrix()
    
    # Light bar
    glPushMatrix()
    glColor3f(0.8, 0, 0)  # Red lights
    glTranslatef(0, 80, 35)
    glScalef(60, 10, 10)
    glutSolidCube(1)
    glPopMatrix()
    glPopMatrix()

# def police_show():
#     glPushMatrix()
#     glColor3f(1, 0, 0)
#     glTranslatef(lane[car_pos], police_y, 0)
#     glScalef(100, 200, 20)
#     glutSolidCube(1)
#     glPopMatrix()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw the grid (game floor)
    glBegin(GL_QUADS)
    
    glColor3f(0.48, 0.46, 0.46)
    glVertex3f(600, -600, 0)
    glVertex3f(-600, -600, 0)
    glVertex3f(-600, +600, 0)
    glVertex3f(600, 600, 0)
    glEnd()
    draw_sky()
    
    
    #hole
    update_hole()           
    draw_hole()             
    handle_hole_z_timer()
    # road line 
    change_line_y()
    road_line()

    random_obstacle()
    move_obstacle()
    # power_showcase()
    if(point >=10):
        front_light()
    

    car_show()
    
    if(point >= 5):
        back_light()
    police_show()
    


    # Display game info text at a fixed screen position
    draw_text(10, 770, f"Total Point: {point}")
    if(cheat_mode):
        draw_text(10, 750, "Cheat Mode Activated")
    else:
        draw_text(10, 750, "Cheat Mode is not Activated")

    if(hit == 1):
        draw_text(760, 750, "Police is chasing")
    elif(hit == 2):
        draw_text(700, 750, "Game Over! Press 'R' to restart")
    draw_text(10, 730, f"Total Bullets Remaining {total_bullet}")
    draw_text(10, 710, f"Press 'n' - Nightmare Mode")
    draw_text(10, 690, f"Press 'c' - Cheat Mode")
    draw_text(10, 670, f"Press 'd' - Day")
    draw_text(10, 650, f"Press 'b' - Night")
    draw_text(10, 630, f"Press 'space' - For Shoot")

    draw_road_surroundings()
    move_and_draw_bullets()
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, w / float(h or 1), 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutIdleFunc(idle) # Register the idle function to move the bullet automatically
    glutReshapeFunc(reshape)
    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()

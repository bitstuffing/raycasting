import pygame
import math

# Additional global variable
global autonomous_steps_left
global turning_degrees_left
global backward_distance_x, backward_distance_y, counter
global player_turned_manually

turning_degrees_left = 0  # Starts with no turning required
backward_distance_x = 0 # backward distance when colliding with a wall
backward_distance_y = 0 # backward distance when colliding with a wall
counter = 0 # counter for the backward distance applies
player_turned_manually = False

# constants for controlling the autonomous movement.
AUTONOMOUS_STEPS = 30  # Number of frames to complete an autonomous action
BACKWARD_STEPS = 20
speed = 0.05
angular_speed = 5
autonomous_speed = speed / AUTONOMOUS_STEPS  # Adjusted speed for smoother transitions
autonomous_angular_speed = angular_speed / AUTONOMOUS_STEPS  # Adjusted angular speed
autonomous_steps_left = 0  # Counter for how many frames are left for the current autonomous action

# Declare them as global
global player_pos, player_angle

collision_buffer = 1

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Maze
maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]

player_pos = [4.5, 4.5]
player_angle = 0

# Constants for the minimap

MINIMAP_CELL_SIZE = 6 # zoom

# Dimensions
MINIMAP_WIDTH = len(maze[0]) * MINIMAP_CELL_SIZE
MINIMAP_HEIGHT = len(maze) * MINIMAP_CELL_SIZE
MINIMAP_X = 10  # 10 pixels de margen
MINIMAP_Y = SCREEN_HEIGHT - MINIMAP_HEIGHT - 10  # 10 pixels de margen

# Colors
RED = (255, 0, 0)

def render_minimap(screen):
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            color = BLACK if maze[x][y] == 0 else WHITE
            pygame.draw.rect(screen, color, (MINIMAP_X + x * MINIMAP_CELL_SIZE, MINIMAP_Y + y * MINIMAP_CELL_SIZE, MINIMAP_CELL_SIZE, MINIMAP_CELL_SIZE))
    # draw player in minimap
    pygame.draw.circle(screen, (255, 0, 0), (int(MINIMAP_X + player_pos[0] * MINIMAP_CELL_SIZE), int(MINIMAP_Y + player_pos[1] * MINIMAP_CELL_SIZE)), 2)

# raycasting
def cast_ray(x, angle):
    angle_rad = math.radians(angle)
    step_size = 0.05

    # Initialize ray position to player's position
    ray_pos = [player_pos[0], player_pos[1]]

    # Calculate step increment based on the ray's angle
    step_x = step_size * math.cos(angle_rad)
    step_y = step_size * math.sin(angle_rad)

    # Cast the ray until it hits a wall
    while 0 <= ray_pos[0] < len(maze) and 0 <= ray_pos[1] < len(maze[0]):
        map_x = int(ray_pos[0])
        map_y = int(ray_pos[1])

        # If the ray hits a wall, return the distance
        if maze[map_x][map_y] == 1:
            distance = math.sqrt((ray_pos[0] - player_pos[0])**2 + (ray_pos[1] - player_pos[1])**2)
            return distance

        # Otherwise, increment the ray's position
        ray_pos[0] += step_x
        ray_pos[1] += step_y

    return float('inf')  # If no wall is hit, return a large number

def render(screen):
    for x in range(SCREEN_WIDTH):
        angle = player_angle + (x - SCREEN_WIDTH / 2) * 60 / SCREEN_WIDTH
        distance = cast_ray(x, angle)
        slice_height = SCREEN_HEIGHT / distance
        pygame.draw.rect(screen, WHITE, (x, (SCREEN_HEIGHT - slice_height) / 2, 1, slice_height))

autonomous_speed = 0.05  # Adjusted speed for smoother transitions

def autonomous_movement():
    global player_pos, player_angle, autonomous_steps_left, turning_degrees_left, backward_distance_x, backward_distance_y, counter

    backtrack_distance = 0.5  # Distance to anticipate collisions and move back when hitting a wall

    # If there are no steps left, decide the next action.
    if autonomous_steps_left <= 0 and turning_degrees_left <= 0:
        # Check for open space first
        forward_x = player_pos[0] + speed * math.cos(math.radians(player_angle))
        forward_y = player_pos[1] + speed * math.sin(math.radians(player_angle))

        # Anticipate the collision by extending the movement by backtrack_distance
        anticipated_forward_x = forward_x + backtrack_distance * math.cos(math.radians(player_angle))
        anticipated_forward_y = forward_y + backtrack_distance * math.sin(math.radians(player_angle))

        right_angle = (player_angle + 90) % 360
        right_x = player_pos[0] + speed * math.cos(math.radians(right_angle))
        right_y = player_pos[1] + speed * math.sin(math.radians(right_angle))

        # Anticipate the collision by extending the movement by backtrack_distance
        anticipated_right_x = right_x + backtrack_distance * math.cos(math.radians(right_angle))
        anticipated_right_y = right_y + backtrack_distance * math.sin(math.radians(right_angle))

        forward_wall = maze[int(anticipated_forward_x)][int(anticipated_forward_y)] == 1
        right_wall = maze[int(anticipated_right_x)][int(anticipated_right_y)] == 1

        if not right_wall or not forward_wall:  # Open space forward or left
            autonomous_steps_left = AUTONOMOUS_STEPS
            counter = 0
        else:
            # Detected a wall while trying to anticipate, so start turning routine
            turning_degrees_left = 90

    # Apply turning if needed
    if turning_degrees_left > 0:
        if counter < BACKWARD_STEPS:

            # Calculate new backward position

            # moving backwards to left
            player_pos[0] -= speed * math.cos(math.radians(player_angle))
            player_pos[1] -= speed * math.sin(math.radians(player_angle))
            
            counter+=1

            if counter == BACKWARD_STEPS:
                backward_distance_x = 0
                backward_distance_y = 0
        else:
            turn_increment = angular_speed / 10  
            player_angle += turn_increment
            turning_degrees_left -= turn_increment
            autonomous_steps_left = AUTONOMOUS_STEPS
    else:
        new_x = player_pos[0] + autonomous_speed * math.cos(math.radians(player_angle))
        new_y = player_pos[1] + autonomous_speed * math.sin(math.radians(player_angle))
        
        if maze[int(new_x)][int(new_y)] == 0:  # 0 indicates a free cell
            player_pos[0] = new_x
            player_pos[1] = new_y
            autonomous_steps_left -= 1
        else:
            # If we still detect a wall, backtrack and turn
            #player_pos[0] -= backtrack_distance * math.cos(math.radians(player_angle))
            #player_pos[1] -= backtrack_distance * math.sin(math.radians(player_angle))
            turning_degrees_left = 90


# Main loop
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock() # fps

running = True

player_pos = [5, 5]
player_angle = 0
player_move_timestamp = 0
player_move_delay = 500  # 0.5 seconds delay before autonomous movement

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                player_move_timestamp = current_time
            
            new_x = player_pos[0]
            new_y = player_pos[1]

            if event.key == pygame.K_UP:
                # Calculate new forward position
                new_x += speed * math.cos(math.radians(player_angle))
                new_y += speed * math.sin(math.radians(player_angle))
            elif event.key == pygame.K_DOWN:
                # Calculate new backward position
                new_x -= speed * math.cos(math.radians(player_angle))
                new_y -= speed * math.sin(math.radians(player_angle))
            
            # Check if new position is inside a wall
            if maze[int(new_x)][int(new_y)] == 0:  # 0 indicates a free cell
                player_pos[0] = new_x
                player_pos[1] = new_y

            # Rotation should be outside the collision check
            if event.key == pygame.K_LEFT:
                # Turn left
                player_angle -= angular_speed
                player_turned_manually = True
            if event.key == pygame.K_RIGHT:  # Changed "elif" to "if" to handle simultaneous key presses
                # Turn right
                player_angle += angular_speed
                player_turned_manually = True

    if not player_turned_manually and (player_move_timestamp is None or (current_time - player_move_timestamp) > player_move_delay):
        autonomous_movement()
    else:
        player_turned_manually = False


    screen.fill(BLACK)
    render(screen)
    render_minimap(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

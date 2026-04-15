import keyboard
import time
import random

gameEnd = False
wall = "██"
space = "  "
plr = "\033[31m██\033[0m"
plr_side_l = "\033[31m\uE0B6█\033[0m"
plr_side_r = "\033[31m█\uE0B4\033[0m"
plr_XY = [[12, 25], [13, 25], [14, 25], [15, 25], [16, 25]]
size = 28
ball = "\033[36m\uE0B6\uE0B4\033[0m"
brick = "██"
move_time = 0.1
last_move = time.time()
ball_XY = [14, 24]
ball_x_speed = random.choice([-1, 1])
ball_y_speed = -1
score = 0
  # You can add as many levels here as you want!
current_level_index = 0
# --- BRICK ARRAY REMOVED FROM SNIPPET TO SAVE YOU READING SPACE ---
# (Keep your massive bricks = [...] dictionary list right here exactly as you had it!)
bricks = []
level_1 = [
    "111111 111111",
    "111111 111111",
    "111111 111111",
    "             ",
    "             ",
    "111111 111111",
    "111111 111111",
    "111111 111111",
]

level_2 = [
    "1111111111111",
    "2222222222222",
    "1111111111111",
    "2222222222222",
    "1111111111111",
    "2222222222222",
]

level_3 = [
    "1231231231231",
    "2312312312312",
    "3123123123123",
    "1231231231231",
    "2312312312312",
    "3123123123123",
    "1231231231231",
]
all_levels = [level_1, level_2, level_3]

def get_line(x1, y1, x2, y2):
    """Returns a list of every [x, y] coordinate exactly on the line from start to end."""
    points = []

    # Calculate differences and step directions
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append([x1, y1])

        # Stop if we reached the final destination
        if x1 == x2 and y1 == y2:
            break

        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points


def print_board(walls, spaces, plr_locate, sizes, ball_locate):
    print("\033[H", end="")
    print(walls * sizes + " Your score is: " + str(score))

    for y in range(1, sizes - 1):
        print(walls, end="")
        for x in range(1, sizes - 1):
            if [x, y] in plr_locate:
                idx = plr_locate.index([x, y])
                if idx == 0:
                    print(plr_side_l, end="")
                elif idx == 4:
                    print(plr_side_r, end="")
                else:
                    print(plr, end="")
            elif [x, y] == ball_locate:
                print(ball, end="")

            elif any([x, y] in b["tiles"] for b in bricks):
                for b in bricks:
                    if b['hp'] == 1:
                        color = "\033[31m"
                    elif b['hp'] == 2:
                        color = "\033[36m"
                    elif b['hp'] == 3:
                        color = "\033[32m"
                    elif b['hp'] == 4:
                        color = "\033[33m"
                    elif b['hp'] == 5:
                        color = "\033[35m"
                    elif b['hp'] == 6:
                        color = "\033[30m"
                    elif b['hp'] == 7:
                        color = "\033[37m"
                    elif b['hp'] == 8:
                        color = "\033[34m"
                    elif b['hp'] == 9:
                        color = "\033[96m"
                    if [x, y] in b["tiles"]:
                        print(color + brick + "\033[0m", end="")
                        break
            else:
                print(spaces, end="")
        print(walls)
    print(walls * sizes)


def move_plr(sizes):
    if keyboard.is_pressed("a"):
        for coord in plr_XY:
            coord[0] -= 1
    if keyboard.is_pressed("d"):
        for coord in plr_XY:
            coord[0] += 1
    if plr_XY[4][0] >= sizes - 1:
        for coord in plr_XY:
            coord[0] -= 1
    if plr_XY[0][0] <= 0:
        for coord in plr_XY:
            coord[0] += 1


def move_ball(ball_locate, ball_speed_x, ball_speed_y, game_end, scores):
    actual_x = ball_locate[0]
    actual_y = ball_locate[1]
    full_speed_x = abs(ball_speed_x)
    full_speed_y = abs(ball_speed_y)
    while True:
        # 1. REMEMBER WHERE THIS SPECIFIC RAY CAST STARTED
        ray_start_x = actual_x
        ray_start_y = actual_y

        target_x = actual_x + ball_speed_x
        target_y = actual_y + ball_speed_y

        path = get_line(actual_x, actual_y, target_x, target_y)

        previous_x = actual_x
        previous_y = actual_y

        bounced = False
        hit_pad_x = False
        hit_pad_y = False

        for step in path:

            grid_x = step[0]
            grid_y = step[1]
            bias = 0

            # --- X WALL COLLISIONS ---
            if grid_x <= 0 or grid_x >= size - 1:
                actual_x = previous_x
                ball_speed_x *= -1
                bounced = True

                # --- Y WALL COLLISIONS (TOP) ---
            if grid_y <= 0:
                actual_y = previous_y
                ball_speed_y *= -1
                bounced = True

            # --- Y WALL COLLISIONS (BOTTOM DEATH) ---
            if grid_y >= size - 1:
                game_end = True
                actual_y = previous_y  # Makes sure the ball renders exactly above the floor when you die
                bounced = True

                # --- PADDLE COLLISION ---
            if [grid_x, previous_y] in plr_XY:
                hit_pad_x = True
                actual_x = previous_x
                ball_speed_x *= -1
                game_end = True
                bounced = True



            if [previous_x, grid_y] in plr_XY:
                hit_pad_y = True
                actual_y = previous_y
                ball_speed_y *= -1
                hit_index = plr_XY.index([previous_x, grid_y])
                if hit_index == 0:
                    bias = -2
                elif hit_index == 1:
                    bias = -1
                elif hit_index == 2:
                    bias = 0
                elif hit_index == 3:
                    bias = 1
                elif hit_index == 4:
                    bias = 2
                if bias != 0:
                    ball_speed_x += bias
                elif bias == 0:
                    if ball_speed_x == 0:
                        ball_speed_x = random.choice([1, -1])
                    else:
                        ball_speed_x = round(ball_speed_x // 2)



                if abs(ball_speed_x) > 3:
                    if ball_speed_x > 0:
                        ball_speed_x = 3
                    if ball_speed_x < 0:
                        ball_speed_x = -3
                if abs(ball_speed_y) > 3:
                    if ball_speed_y > 0:
                        ball_speed_y = 3
                    if ball_speed_y < 0:
                        ball_speed_y = -3

                full_speed_x = abs(ball_speed_x)
                bounced = True


            if not hit_pad_x and not hit_pad_y:
                 if [grid_x, grid_y] in plr_XY:
                    actual_x = previous_x
                    actual_y = previous_y
                    ball_speed_y *= -1
                    ball_speed_x *= -1
                    bounced = True

            # --- BRICK SEARCHING ---
            hit_brick_x = None
            hit_brick_y = None
            hit_brick_diagonal = None

            for f in bricks:
                if [grid_x, previous_y] in f["tiles"]:
                    hit_brick_x = f
                    break
            for f in bricks:
                if [previous_x, grid_y] in f["tiles"]:
                    hit_brick_y = f
                    break

            if not hit_brick_x and not hit_brick_y:
                for f in bricks:
                    if [grid_x, grid_y] in f["tiles"]:
                        hit_brick_diagonal = f
                        break

            # --- BRICK COLLISIONS ---
            if hit_brick_x:
                if hit_brick_x in bricks:
                    hit_brick_x['hp'] -= 1
                    scores += 1
                    if hit_brick_x['hp'] <= 0:
                        bricks.remove(hit_brick_x)
                    actual_x = previous_x
                    ball_speed_x *= -1
                    bounced = True

            if hit_brick_y:
                if hit_brick_y in bricks:
                    hit_brick_y['hp'] -= 1
                    scores += 1
                    if hit_brick_y['hp'] <= 0:
                        bricks.remove(hit_brick_y)
                    actual_y = previous_y
                    ball_speed_y *= -1
                    bounced = True

            if hit_brick_diagonal:
                if hit_brick_diagonal in bricks:
                    hit_brick_diagonal['hp'] -= 1
                    scores += 1
                    if hit_brick_diagonal['hp'] <= 0:
                        bricks.remove(hit_brick_diagonal)
                    actual_x = previous_x
                    actual_y = previous_y
                    ball_speed_y *= -1
                    ball_speed_x *= -1

                    bounced = True



            # --- HIT STOP TRIGGER ---
            # Note 3: If we hit anything, we immediately Break out of the 'for' loop.
            # This prevents the Render Trap and draws the frame precisely on impact!
            if bounced:
                break

            previous_x = grid_x
            previous_y = grid_y

        if not bounced:
            actual_x = target_x
            actual_y = target_y
            break
        else:
            traveled_x = abs(ray_start_x - actual_x)
            traveled_y = abs(ray_start_y - actual_y)
            remaining_x = abs(ball_speed_x) - traveled_x
            remaining_y = abs(ball_speed_y) - traveled_y
            if ball_speed_x > 0:
                ball_speed_x = remaining_x
            elif ball_speed_x < 0:
                ball_speed_x = -remaining_x
            if ball_speed_y > 0:
                ball_speed_y = remaining_y
            elif ball_speed_y < 0:
                ball_speed_y = -remaining_y

            if ball_speed_x == 0 and ball_speed_y == 0:
                break

            # (Still inside your while True loop)
            if not bounced:
                actual_x = target_x
                actual_y = target_y

            # Whether we bounced or not, break out of the while loop!
            break

    # --- FULL SPEED MEMORY RESTORATION ---
    # (This must go OUTSIDE the while loop, right before you write the positions!)
    if ball_speed_x > 0:
        ball_speed_x = full_speed_x
    elif ball_speed_x < 0:
        ball_speed_x = -full_speed_x

    if ball_speed_y > 0:
        ball_speed_y = full_speed_y
    elif ball_speed_y < 0:
        ball_speed_y = -full_speed_y

    # Write the calculated math position back to the actual ball list
    ball_locate[0] = int(round(actual_x))
    ball_locate[1] = int(round(actual_y))

    return ball_speed_x, ball_speed_y, game_end, bounced, scores


def parse_bricks(b, level):
    for y, line in enumerate(level):
        for x, char in enumerate(line):
            if char != " ":
                hp = int(char)
                actual_brick_y = y + 1
                actual_brick_x1 = 1 + (x * 2)
                actual_brick_x2 = actual_brick_x1 + 1
                b.append({"tiles": [[actual_brick_x1, actual_brick_y], [actual_brick_x2, actual_brick_y]], "hp": hp})




parse_bricks(bricks, all_levels[current_level_index])

# --- MAIN GAME LOOP ---
while not gameEnd:
    if len(bricks) == 0:
        current_level_index += 1
        parse_bricks(bricks, all_levels[current_level_index])
        ball_XY = [14, 24]
        ball_x_speed = random.choice([-1, 1])
        ball_y_speed = -1
        if current_level_index > len(all_levels):
            gameEnd = True
    print_board(wall, space, plr_XY, size, ball_XY)
    if time.time() - last_move >= move_time:
        last_move = time.time()
        move_plr(size)
        ball_x_speed,ball_y_speed,gameEnd,bounces,score=move_ball(ball_XY, ball_x_speed, ball_y_speed, gameEnd, score)
        if bounces:
            last_move = time.time() - (move_time - 0.01)
    time.sleep(0.001)

# --- GAME OVER LOOP ---
while gameEnd:
    # Note 4: Drawing the board one final time fixes the "Ghost Game Over"
    if current_level_index > len(all_levels):
        if current_level_index > len(all_levels):
            print("\033[H\033[J")
            print("YOU WIN!")
            time.sleep(1000)
    else:
        print_board(wall, space, plr_XY, size, ball_XY)
        print("Game Over")
        time.sleep(1000)
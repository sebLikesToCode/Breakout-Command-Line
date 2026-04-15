# Breakout-Command-Line
Breakout played in the windows terminal, this was quite difficult for me

breakout-cli 
a breakout clone for the windows terminal. it uses ray casting logic to handle the ball physics so it never "tunnels" through bricks, even at high speeds.

how it works
ray casting collision: instead of just checking if the ball is touching something, the game uses get_line to calculate every coordinate the ball passes through between frames. if any of those points hit a brick or the paddle, it triggers a bounce.

procedural level loading: i built a parser that reads levels from a list of strings. each number (1-9) represents a brick and its HP, so adding new levels is just adding a new string array.

paddle physics: the ball's horizontal speed changes depending on where it hits the paddle. hitting the edges adds "spin" (bias), while hitting the center stabilizes the trajectory.

technical wins
bresenham's algorithm: used a line algorithm to prevent the ball from skipping over objects. this fixed a bug where the ball would phase through the paddle if it was moving too fast.

multi-hit brick system: bricks have health (hp). I used a dictionary system to track each brick's coordinates and health, and a dynamic color system to show how much HP they have left.

bouncing logic: the move_ball function handles X, Y, and diagonal collisions separately to make sure the ball reflects at the correct angle every time.

what's next
this script is getting pretty long and the collision logic is heavy. i'm going to refactor this into OOP

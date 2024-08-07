import board
import time
import neopixel
import random
import digitalio
import sys
import select

# IO Enable
io_enable_pin = digitalio.DigitalInOut(board.IO_POWER)
io_enable_pin.direction = digitalio.Direction.OUTPUT
io_enable_pin.value = False

# Matrix settings
max_xpos = 12
max_ypos = 8
anzahl = max_xpos * max_ypos
pixel_pin = board.D2
ORDER = neopixel.GRB
ZICKZACK = True

def umrechnen(xpos, ypos):
    if ZICKZACK:
        return umrechnen_zickzack(xpos, ypos)
    else:
        return umrechnen_normal(xpos, ypos)

def umrechnen_normal(xpos, ypos):
    return ypos * max_xpos + xpos

def umrechnen_zickzack(xpos, ypos):
    if ypos % 2 == 0:
        pixelnummer = ypos * max_xpos + xpos
    else:
        pixelnummer = (ypos + 1) * max_xpos - xpos - 1
    return pixelnummer

def alles_anzeigen(spielfeld, pixels):
    for i in range(len(spielfeld)):
        pixels[i] = spielfeld[i]
    pixels.show()

# ---------------------------------------------------------
# Game Settings
BACKGROUND = (0, 0, 0)
BALL_COLOR = (255, 255, 255)
PADDLE_COLOR = (0, 255, 0)
BRICK_COLOR = (255, 0, 0)

def initialisieren(spielfeld):
    for i in range(anzahl):
        spielfeld.append(BACKGROUND)

def draw_paddle(spielfeld, paddle_pos):
    for x in paddle_pos:
        spielfeld[umrechnen(x, max_ypos-1)] = PADDLE_COLOR

def draw_ball(spielfeld, ball_pos):
    spielfeld[umrechnen(ball_pos[0], ball_pos[1])] = BALL_COLOR

def draw_bricks(spielfeld, bricks):
    for brick in bricks:
        spielfeld[umrechnen(brick[0], brick[1])] = BRICK_COLOR

def clear_screen(spielfeld):
    for i in range(len(spielfeld)):
        spielfeld[i] = BACKGROUND

def move_paddle(paddle_pos, direction):
    if direction == 'left' and paddle_pos[0] > 0:
        paddle_pos = [pos - 1 for pos in paddle_pos]
    elif direction == 'right' and paddle_pos[-1] < max_xpos - 1:
        paddle_pos = [pos + 1 for pos in paddle_pos]
    return paddle_pos

def update_ball(ball_pos, ball_dir, paddle_pos, bricks):
    new_x = ball_pos[0] + ball_dir[0]
    new_y = ball_pos[1] + ball_dir[1]

    # Check for wall collisions
    if new_x < 0 or new_x >= max_xpos:
        ball_dir[0] = -ball_dir[0]
        new_x = ball_pos[0] + ball_dir[0]
    if new_y < 0:
        ball_dir[1] = -ball_dir[1]
        new_y = ball_pos[1] + ball_dir[1]

    # Check for paddle collision
    if new_y >= max_ypos - 1 and new_x in paddle_pos:
        ball_dir[1] = -ball_dir[1]
        new_y = ball_pos[1] + ball_dir[1]

    # Check for brick collisions
    if [ball_pos[0], new_y] in bricks:
        bricks.remove([ball_pos[0], new_y])
        ball_dir[1] = -ball_dir[1]
        new_y = ball_pos[1] + ball_dir[1]
    if [new_x, new_y] in bricks:
        bricks.remove([new_x, new_y])
        ball_dir[1] = -ball_dir[1]
        new_y = ball_pos[1] + ball_dir[1]

    # Check for bottom collision (game over)
    if new_y >= max_ypos:
        return None, ball_dir, bricks, True  # Ball lost, game over

    return [new_x, new_y], ball_dir, bricks, False

def countdown(pixels, seconds=5):
    for i in range(seconds, 0, -1):
        pixels.fill((100,0,0))
        pixels.show()
        time.sleep(0.5)
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.5)
        print(f"Starting in {i} seconds...")

def main():
    pixels = neopixel.NeoPixel(pixel_pin, max_xpos * max_ypos, brightness=0.15,
                               auto_write=False, pixel_order=ORDER)
    spielfeld = []
    initialisieren(spielfeld)

    paddle_pos = [5, 6, 7]
    ball_pos = [6, 3]
    ball_dir = [1, 1]
    bricks = [[x, y] for x in range(12) for y in range(3)]

    countdown(pixels, 3)

    ball_update_time = time.time()
    ball_update_interval = 0.3  # Ball update interval (seconds)

    while True:
        clear_screen(spielfeld)

        # Update ball position at a slower rate
        current_time = time.time()
        if current_time - ball_update_time > ball_update_interval:
            ball_pos, ball_dir, bricks, game_over = update_ball(ball_pos, ball_dir, paddle_pos, bricks)
            if game_over:
                print("Game Over!")
                time.sleep(1.0)
                ball_pos = [6, 3]
                bricks = [[x, y] for x in range(12) for y in range(3)]
                countdown(pixels, 3)
                draw_paddle(spielfeld, paddle_pos)
                draw_ball(spielfeld, ball_pos)
                draw_bricks(spielfeld, bricks)
                alles_anzeigen(spielfeld, pixels)
                time.sleep(1.0)
            ball_update_time = current_time

        draw_paddle(spielfeld, paddle_pos)
        draw_ball(spielfeld, ball_pos)
        draw_bricks(spielfeld, bricks)

        alles_anzeigen(spielfeld, pixels)

        time.sleep(0.05)  # Paddle movement and screen update interval

        # Benutzersteuerung für Paddle-Bewegung
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            steuerzeichen = sys.stdin.read(1).lower()
            if steuerzeichen == 'a':
                paddle_pos = move_paddle(paddle_pos, 'left')
            elif steuerzeichen == 'd':
                paddle_pos = move_paddle(paddle_pos, 'right')

if __name__ == '__main__':
    main()

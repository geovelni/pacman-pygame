import pygame 
import sys
import random
import time

pygame.init()

TILE_SIZE = 32

LEVELS = [
    [line.ljust(20, '#') for line in level]
    for level in [
        [
            "####################",
            "#........#.........#",
            "#.######.#.#######.#",
            "#.#....#.#.......#.#",
            "#.#.##.#.####..#.#.#",
            "#.#.#.......#.####.#",
            "#.#.#########.#.#..#",
            "#..................#",
            "####################"
        ],
        [
        "####################",
        "##................##",
        "#.......#..#.......#",
        "#.....##....##.....#",
        "#....##..##..##....#",
        "#.....##....##.....#",
        "#.......#..#.......#",
        "##................##",
        "####################"
    ],
        [
            "####################",
            "#..................#",
            "#.#####.##.#.#######",
            "#.#...#.#..#......#",
            "#.#.#.#.####.###.#.#",
            "#...#.......#....#.#",
            "#.#.#########.##.#.#",
            "#..................#",
            "####################"
        ]
    ]
]

GRAY = (160, 160, 160)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PURPLE = (160, 32, 240)
DOT_COLOR = (100, 100, 100)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 36)

def load_background(level, WIDTH, HEIGHT):
    try:
        background = pygame.image.load(f"fundal{level + 1}.jpg")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        return background
    except Exception as e:
        print(f"[Eroare încărcare fundal]: {e}")
        return None

def generate_items(maze, pacman_pos):
    fruit_positions = []
    dot_positions = []
    while len(fruit_positions) < 4:
        y = random.randint(1, len(maze) - 2)
        x = random.randint(1, len(maze[0]) - 2)
        if maze[y][x] != '#' and [y, x] != pacman_pos and [y, x] not in fruit_positions:
            fruit_positions.append([y, x])

    enemy_positions = []
    while len(enemy_positions) < 4:
        y = random.randint(1, len(maze) - 2)
        x = random.randint(1, len(maze[0]) - 2)
        if maze[y][x] != '#' and [y, x] != pacman_pos and [y, x] not in fruit_positions:
            enemy_positions.append([y, x])

    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] != '#' and [y, x] != pacman_pos:
                dot_positions.append([y, x])

    return fruit_positions, enemy_positions, dot_positions

def move_enemies(enemy_positions, maze):
    for enemy in enemy_positions:
        direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        new_y = enemy[0] + direction[0]
        new_x = enemy[1] + direction[1]
        if 0 <= new_y < len(maze) and 0 <= new_x < len(maze[0]) and maze[new_y][new_x] != '#':
            enemy[0] = new_y
            enemy[1] = new_x

def show_level_summary(screen, current_level, score, level_time, WIDTH, HEIGHT):
    screen.fill(BLACK)
    text1 = font.render(f"Nivelul {current_level + 1} finalizat!", True, WHITE)
    text2 = font.render(f"Scor: {score}", True, WHITE)
    text3 = font.render(f"Timp: {int(level_time)} secunde", True, WHITE)
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2 + 30))
    pygame.display.flip()
    pygame.time.wait(3000)

def game_loop():
    current_level = 0
    score = 0
    clock = pygame.time.Clock()

    while current_level < len(LEVELS):
        MAZE = LEVELS[current_level]
        ROWS = len(MAZE)
        COLS = len(MAZE[0])
        WIDTH = COLS * TILE_SIZE
        HEIGHT = ROWS * TILE_SIZE + 30
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        background = load_background(current_level, WIDTH, HEIGHT)

        pacman_pos = [1, 1]
        fruit_positions, enemy_positions, dot_positions = generate_items(MAZE, pacman_pos)

        power_up_active = False
        power_up_start_time = 0

        level_start_time = time.time()
        paused = False
        level_running = True

        while level_running:
            clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    paused = not paused

            if paused:
                continue

            keys = pygame.key.get_pressed()
            y, x = pacman_pos
            if keys[pygame.K_UP] and MAZE[y - 1][x] != '#':
                pacman_pos[0] -= 1
            elif keys[pygame.K_DOWN] and MAZE[y + 1][x] != '#':
                pacman_pos[0] += 1
            elif keys[pygame.K_LEFT] and MAZE[y][x - 1] != '#':
                pacman_pos[1] -= 1
            elif keys[pygame.K_RIGHT] and MAZE[y][x + 1] != '#':
                pacman_pos[1] += 1

            move_enemies(enemy_positions, MAZE)

            if pacman_pos in enemy_positions:
                if power_up_active:
                    enemy_positions.remove(pacman_pos)
                else:
                    print("Ai pierdut!")
                    return

            if pacman_pos in fruit_positions:
                fruit_positions.remove(pacman_pos)
                score += 10
                power_up_active = True
                power_up_start_time = time.time()

            if pacman_pos in dot_positions:
                dot_positions.remove(pacman_pos)

            if not dot_positions:
                level_time = time.time() - level_start_time
                show_level_summary(screen, current_level, score, level_time, WIDTH, HEIGHT)
                current_level += 1
                break  

            if power_up_active and time.time() - power_up_start_time > 3:
                power_up_active = False

            if background:
                screen.blit(background, (0, 30))
            else:
                screen.fill(BLACK)

            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 30))

            for row_idx, row in enumerate(MAZE):
                for col_idx, tile in enumerate(row):
                    if tile == '#':
                        rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE + 30, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, GRAY, rect)

            for dot in dot_positions:
                dx, dy = dot[1] * TILE_SIZE + TILE_SIZE // 2, dot[0] * TILE_SIZE + TILE_SIZE // 2 + 30
                pygame.draw.circle(screen, DOT_COLOR, (dx, dy), 4)

            for fruit in fruit_positions:
                fx, fy = fruit[1] * TILE_SIZE + TILE_SIZE // 2, fruit[0] * TILE_SIZE + TILE_SIZE // 2 + 30
                pygame.draw.circle(screen, PURPLE, (fx, fy), TILE_SIZE // 4)

            for enemy in enemy_positions:
                ex, ey = enemy[1] * TILE_SIZE, enemy[0] * TILE_SIZE + 30
                color = BLUE if power_up_active else RED
                pygame.draw.rect(screen, color, (ex, ey, TILE_SIZE, TILE_SIZE))

            px, py = pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2, pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2 + 30
            pygame.draw.circle(screen, YELLOW, (px, py), TILE_SIZE // 2 - 4)

            elapsed = int(time.time() - level_start_time)
            text_time = font.render(f"Timp: {elapsed}s", True, WHITE)
            text_score = font.render(f"Scor: {score}", True, WHITE)
            screen.blit(text_time, (10, 5))
            screen.blit(text_score, (150, 5))

            pygame.display.flip()

    print("Felicitări! Ai terminat toate nivelele!")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
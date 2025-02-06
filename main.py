import pygame
import time
import random
import os
from pygame.locals import *
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minigames Menu")
BG = pygame.transform.scale(pygame.image.load("backround.jpg"), (WIDTH, HEIGHT))
MENU_BG = pygame.transform.scale(pygame.image.load("minigames.jpg"), (WIDTH, HEIGHT))


PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5
FONT = pygame.font.SysFont("Times New Roman", 30)
LEADERBOARD_FILE = "leaderboard.txt"


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)
    for star in stars:
        pygame.draw.rect(WIN, "yellow", star)

    pygame.display.update()


def save_score(score):
    scores = load_leaderboard()
    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:5]  # Keep only top 5 scores
    with open(LEADERBOARD_FILE, "w") as file:
        for s in scores:
            file.write(f"{s}\n")


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as file:
        return [float(line.strip()) for line in file.readlines()]


def display_leaderboard():
    WIN.fill((0, 0, 0))
    title_text = FONT.render("Leaderboard", 1, "white")
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    scores = load_leaderboard()
    for i, score in enumerate(scores):
        score_text = FONT.render(f"{i + 1}. {score:.2f}s", 1, "white")
        WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 100 + i * 40))

    pygame.display.update()
    pygame.time.delay(4000)


def main_menu():
    run = True
    while run:
        WIN.blit(MENU_BG, (0, 0))

        frame_rect = pygame.Rect(WIDTH // 2 - 150, 180, 300, 200)
        pygame.draw.rect(WIN, (0, 0, 0, 180), frame_rect)
        pygame.draw.rect(WIN, "white", frame_rect, 3)

        title_text = FONT.render("Choose Minigame", 1, "white")
        game1_text = FONT.render("1. Space Dodge", 1, "white")
        game2_text = FONT.render("2. Car Game", 1, "white")
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 200))
        WIN.blit(game1_text, (WIDTH // 2 - game1_text.get_width() // 2, 250))
        WIN.blit(game2_text, (WIDTH // 2 - game2_text.get_width() // 2, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main()
                elif event.key == pygame.K_2:
                    car_game()

def car_game():
    size = width, height = (800, 800)
    road_w = int(width / 1.6)
    roadmark_w = int(width / 80)
    right_lane = width / 2 + road_w / 4
    left_lane = width / 2 - road_w / 4
    speed = 1

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Car Game")
    screen.fill((60, 220, 0))
    pygame.display.update()

    car = pygame.image.load("car.png")
    car_loc = car.get_rect()
    car_loc.center = right_lane, height * 0.8

    car2 = pygame.image.load("otherCar.png")
    car2_loc = car2.get_rect()
    car2_loc.center = left_lane, height * 0.2

    counter = 0
    start_time = time.time()
    running = True

    while running:
        counter += 1
        elapsed_time = time.time() - start_time
        if counter == 5000:
            speed += 0.15
            counter = 0

        car2_loc[1] += speed
        if car2_loc[1] > height:
            if random.randint(0, 1) == 0:
                car2_loc.center = right_lane, -200
            else:
                car2_loc.center = left_lane, -200

        if car_loc[0] == car2_loc[0] and car2_loc[1] > car_loc[1] - 250:

            screen.fill((0, 0, 0))
            lost_text = FONT.render("You Lost!", 1, "white")
            screen.blit(lost_text, (width // 2 - lost_text.get_width() // 2, height // 2))
            pygame.display.update()
            pygame.time.delay(3000)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [K_a, K_LEFT]:
                    car_loc = car_loc.move([-int(road_w / 2), 0])
                if event.key in [K_d, K_RIGHT]:
                    car_loc = car_loc.move([int(road_w / 2), 0])

        pygame.draw.rect(screen, (50, 50, 50), (width / 2 - road_w / 2, 0, road_w, height))
        pygame.draw.rect(screen, (255, 240, 60), (width / 2 - roadmark_w / 2, 0, roadmark_w, height))
        pygame.draw.rect(screen, (255, 255, 255), (width / 2 - road_w / 2 + roadmark_w * 2, 0, roadmark_w, height))
        pygame.draw.rect(screen, (255, 255, 255), (width / 2 + road_w / 2 - roadmark_w * 3, 0, roadmark_w, height))

        screen.blit(car, car_loc)
        screen.blit(car2, car2_loc)

        timer_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
        screen.blit(timer_text, (10, 10))

        pygame.display.update()

    pygame.quit()

def main():
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count >= star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            save_score(elapsed_time)
            lost_text = FONT.render("You Lost", 1, "white")
            WIN.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - lost_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            display_leaderboard()
            break

        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
    main_menu()

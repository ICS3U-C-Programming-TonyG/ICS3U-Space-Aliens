# Created by: Mr. Gao
# Created on: July 2025
# This program is the "Space Aliens" program on the PyBadge

import ugame
import stage
import constants
import time
import random
import supervisor

def splash_scene():
    coin_sound = open("coin.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(image_bank_background, 10, 8)

    # Draw splash logo using tiles
    background.tile(2, 2, 0)
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)
    background.tile(2, 3, 0)
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)
    background.tile(2, 4, 0)
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)
    background.tile(2, 5, 0)
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [background]
    game.render_block()

    time.sleep(2.0)
    menu_scene()

def menu_scene():
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")

    text = []
    text1 = stage.Text(width=29, height=12)
    text1.move(10, 10)
    text1.text("MT Game Studios, Made by Tony G.")
    text.append(text1)

    text2 = stage.Text(width=29, height=12)
    text2.move(10, 30)
    text2.text("PRESS START")
    text.append(text2)

    background = stage.Grid(image_bank_background, 10, 8)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START != 0:
            game_scene()
            return
        game.tick()

def game_scene():
    def show_alien():
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x < 0:
                aliens[alien_number].move(
                    random.randint(0 + constants.SPRITE_SIZE, constants.SCREEN_X - constants.SPRITE_SIZE),
                    constants.OFF_TOP_SCREEN)
                break

    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    a_button = constants.button_state["button_up"]

    pew_sound = open("pew.wav", "rb")
    boom_sound = open("boom.wav", "rb")
    crash_sound = open("crash.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)

    ship = stage.Sprite(image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

    aliens = []
    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        a_single_alien = stage.Sprite(image_bank_sprites, 9, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        aliens.append(a_single_alien)
    show_alien()

    lasers = []
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(image_bank_sprites, 10, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        lasers.append(a_single_laser)

    score = 0

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = aliens + lasers + [ship] + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()

        # Handle A button state for firing lasers
        if keys & ugame.K_X:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]

        # Ship movement controls
        if keys & ugame.K_RIGHT:
            if ship.x <= constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(ship.x + constants.SHIP_SPEED, ship.y)
            else:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
        if keys & ugame.K_LEFT:
            if ship.x >= 0:
                ship.move(ship.x - constants.SHIP_SPEED, ship.y)
            else:
                ship.move(0, ship.y)
        if keys & ugame.K_UP:
            if ship.y >= 0:
                ship.move(ship.x, ship.y - constants.SHIP_SPEED)
            else:
                ship.move(ship.x, 0)
        if keys & ugame.K_DOWN:
            if ship.y <= constants.SCREEN_Y - constants.SPRITE_SIZE:
                ship.move(ship.x, ship.y + constants.SHIP_SPEED)
            else:
                ship.move(ship.x, constants.SCREEN_Y - constants.SPRITE_SIZE)
        
        # Fire laser if A button just pressed
        if a_button == constants.button_state["button_just_pressed"]:
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:
                    lasers[laser_number].move(ship.x, ship.y)
                    sound.play(pew_sound)
                    break

        # Move lasers up the screen
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                lasers[laser_number].move(lasers[laser_number].x, lasers[laser_number].y - constants.LASER_SPEED)
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    lasers[laser_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        # Move aliens down the screen
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                aliens[alien_number].move(aliens[alien_number].x, aliens[alien_number].y + constants.ALIEN_SPEED)
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()
                    # Lose one score if alien escapes
                    score -= 1
                    if score < 0:
                        score = 0

        # Check for collisions between ship and aliens
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0 and aliens[alien_number].y >= 0 and aliens[alien_number].y < constants.SCREEN_Y:
                if stage.collide(aliens[alien_number].x + 1, aliens[alien_number].y,
                                aliens[alien_number].x + 15, aliens[alien_number].y + 15,
                                ship.x + 1, ship.y,
                                ship.x + 15, ship.y + 15):
                    sound.stop()
                    sound.play(crash_sound)
                    time.sleep(2.0)
                    game_over_scene(score)
                    return

        # Check for collisions between lasers and aliens
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                for alien_number in range(len(aliens)):
                    if aliens[alien_number].x > 0:
                        if (lasers[laser_number].x < aliens[alien_number].x + constants.SPRITE_SIZE and
                            lasers[laser_number].x + constants.SPRITE_SIZE > aliens[alien_number].x and
                            lasers[laser_number].y < aliens[alien_number].y + constants.SPRITE_SIZE and
                            lasers[laser_number].y + constants.SPRITE_SIZE > aliens[alien_number].y):
                            lasers[laser_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            aliens[alien_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            sound.stop()
                            sound.play(boom_sound)
                            show_alien()
                            show_alien()
                            # Gain one score for shooting alien
                            score += 1
                            if score > 100:
                                you_win_scene(score)
                                return

        game.render_sprites(aliens + lasers + [ship])
        game.tick()

def game_over_scene(score):
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)
    text = []
    text1 = stage.Text(width=29, height=14)
    text1.move(22, 10)
    text1.text("GAME OVER")
    text.append(text1)

    text2 = stage.Text(width=29, height=12)
    text2.move(10, 40)
    text2.text("Your Score: {}".format(score))
    text.append(text2)

    text3 = stage.Text(width=29, height=12)
    text3.move(32, 60)
    text3.text("press select")
    text.append(text3)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()
    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_SELECT != 0:
            supervisor.reload()
        game.tick()

def you_win_scene(score):
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)
    text = []
    text1 = stage.Text(width=29, height=14)
    text1.move(22, 10)
    text1.text("YOU WIN!")
    text.append(text1)

    text2 = stage.Text(width=29, height=12)
    text2.move(10, 40)
    text2.text("Final Score: {}".format(score))
    text.append(text2)

    text3 = stage.Text(width=29, height=12)
    text3.move(32, 60)
    text3.text("press select")
    text.append(text3)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()
    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_SELECT != 0:
            supervisor.reload()
        game.tick()

if __name__ == "__main__":
    splash_scene()
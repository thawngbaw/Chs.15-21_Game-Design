'''
SPRITE GAME
-----------
Here you will start the beginning of a game that you will be able to update as we
learn more in upcoming chapters. Below are some ideas that you could include:

1.) Find some new sprite images.
2.) Move the player sprite with arrow keys rather than the mouse. Don't let it move off the screen.
3.) Move the other sprites in some way like moving down the screen and then re-spawning above the window.
4.) Use sounds when a sprite is killed or the player hits the sidewall.
5.) See if you can reset the game after 30 seconds. Remember the on_update() method runs every 1/60th of a second.
6.) Try some other creative ideas to make your game awesome. Perhaps collecting good sprites while avoiding bad sprites.
7.) Keep score and use multiple levels. How do you keep track of an all time high score?
8.) Make a two player game.

'''
import arcade
import random

sw = 1000
sh = 600
wolf_speed = 1
wolf_scale = .1
#wolf_count = 50
bullet_scale = .1
bullet_speed = 10

EXPLOSION_TEXTURE_COUNT = 50

player_scale = .3
player_speed = 5


class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Images/explosions/explosion0000.png")
        self.current_texture = 0
        self.textures = texture_list

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()

class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Bullet.png", bullet_scale)

    def update(self):
        self.center_y -= bullet_speed
        if self.bottom < -1:
            self.kill()

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("player.png", player_scale)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.right >= sw:
            self.right = sw
        elif self.left <= 0:
            self.left = 0
        elif self.top > sh:
            self.top = sh
        elif self.bottom <= 0:
            self.bottom = 0


class Wolf(arcade.Sprite):
    def __init__(self):
        super().__init__("wolf.png", wolf_scale)
        self.w = int(self.width)
        self.h = int(self.height)

    def update(self):
        self.center_x += wolf_speed
        if self.right > sw:
           self.center_x = random.randrange(0, 500)
           #self.center_y = random.randrange(sh + self.h, sh * 2)


class MyGame(arcade.Window):
    def __init__(self, sw, sh, title):
        super().__init__(sw, sh, title)
        self.set_mouse_visible(False)
        self.background = None
        self.background = arcade.load_texture("BG.png")

        self.explosion_texture_list = []

        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def reset(self):
        self.wolf_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.explosion = arcade.SpriteList()
        self.score = 0
        self.wolf_count = 50
        self.Gameover = False

        # create player
        self.player = Player()
        self.player.center_x = sw / 2
        self.player.center_y = sh/2
        self.player_list.append(self.player)

        # create wolf
        for i in range(self.wolf_count):
            wolf = Wolf()
            wolf.center_x = random.randrange(0, 400)
            wolf.center_y = random.randrange(2, 40)
            self.wolf_list.append(wolf)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, sw, sh, self.background)
        self.player_list.draw()
        self.wolf_list.draw()
        self.bullet_list.draw()
        self.explosion.draw()

        the_score = f"Score:{self.score}"
        arcade.draw_text(the_score, sw-80, sh-20, arcade.color.WHITE, 14)

        wolf_left = f"wolf left:{len(self.wolf_list)}"
        arcade.draw_text(wolf_left, 10, 40, arcade.color.BLACK, 14)

        if self.Gameover == True:
            arcade.draw_rectangle_filled(sw // 2, sh // 2, sw, sh, arcade.color.BLACK)
            arcade.draw_text("Game Over:Press Space to Play Again", sw/2, sh/2-20, ((0, 255, 0)), 14, align="center",
                             anchor_x="center")


    def on_update(self, dt):
        self.player_list.update()
        self.wolf_list.update()
        self.bullet_list.update()
        self.explosion.update()

        if len(self.wolf_list) == 0:
            self.Gameover = True

        wolf_hit_list = arcade.check_for_collision_with_list(self.player, self.wolf_list)
        for wolf in wolf_hit_list:
            wolf.kill()
            self.score += 1


        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.wolf_list)
            if len(hit_list) > 0:
                self.bullet.kill()
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                self.explosion.append(explosion)

            for self.wolf in hit_list:
                self.wolf_count += 2
                self.wolf.change_x = random.randrange(0, 500)
                self.wolf.change_y = (2, 40)
                self.wolf.kill()

                self.score += 30

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -player_speed
        elif key == arcade.key.RIGHT:
            self.player.change_x = player_speed
        elif key == arcade.key.UP:
            self.player.change_y = player_speed
        elif key == arcade.key.DOWN:
            self.player.change_y = -player_speed
        elif key == arcade.key.F:
            self.reset()
        elif key == arcade.key.SPACE and not self.Gameover:
            self.bullet = Bullet()    # instantiate a bullet
            self.bullet.center_x = self.player.center_x
            self.bullet.bottom = self.player.bottom
            self.bullet.angle = 270
            self.bullet_list.append(self.bullet)
            self.score -= 1

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0





def main():
    my_window = MyGame(sw, sh, "my game")
    my_window.reset()
    arcade.run()


if __name__ == "__main__":
    main()
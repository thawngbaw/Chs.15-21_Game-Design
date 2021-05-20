import random
import arcade
import math

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
bullet_scale = 1
bullet_speed = 10
bullet_pts = -1
trooper_pts = 5
SW = 800
SH = 600
sp = 4
ANGLE_SPEED = 5
t_speed = 2
EXPLOSION_TEXTURE_COUNT = 50
MOVEMENT_SPEED = 5

''' 
instruction page = 0
level 1 = 1
level 2 = 2
level 3 = 3
end game = 4
'''


class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Images/explosions/explosion0000.png")
        self.current_texture = 0
        self.textures = texture_list
        self.explosion_sound = arcade.load_sound("sounds/explosion.mp3")

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self. current_texture)
        else:
            self.kill()


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
        self.speed = 0
        self.change_angle = 0

    def update(self):
        self.angle += self.change_angle
        angle_rad = math.radians(self.angle)
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

        if self.left < 0:
            self.left = 0
        elif self.right > SW:
            self.right = SW
        elif self.top > SH:
            self.top = SH
        elif self.bottom < 0:
            self.bottom = 0


class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)
        self.dx = random.randrange(-1, 2, 2)
        self.dy = random.randrange(-1, 2, 2)

    def update(self):
        self.center_y += self.dy
        self.center_x += self.dx
        if self.top > SH or self.bottom < 0:
            self.dy *= -1
        elif self.left < 0 or self.right > SW:
            self.dx *= -1


class Enemy_bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png", bullet_scale)
        self.angle_list = [0, 90, 180, 270]
        self.angle = random.choice(self.angle_list)

    def update(self):
        if self.angle == 0:
            self.center_x += bullet_speed
        elif self.angle == 90:
            self.center_y += bullet_speed
        elif self.angle == 180:
            self.center_x -= bullet_speed
        else:
            self.center_y -= bullet_speed

        if self.top < 0 or self.bottom > SH or self.right < 0 or self.left > SW:
            self.kill()


class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)
        self.explosion = arcade.load_sound('sounds/explosion.mp3')
        self.speed = 0

    def update(self):
        angle_shoot = math.radians(self.angle-90)
        self.center_x += -self.speed * math.sin(angle_shoot)
        self.center_y += self.speed * math.cos(angle_shoot)
        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()



# ------MyGame Class--------------
class MyGame(arcade.Window):
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        self.set_mouse_visible(False)
        self.current_state = 0
        self.Gameover = True

        self.explosion_texture_list = []

        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def reset(self):
        if self.current_state == 1:
            self.background = arcade.load_texture("Images/sky1.png")
            self.trooper_count = 10
        elif self.current_state == 2:
            self.background = arcade.load_texture("Images/sky2.png")
            self.trooper_count = 20
        elif self.current_state == 3:
            self.background = arcade.load_texture("Images/sky3.png")
            self.trooper_count = 30

        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ebullet_list = arcade.SpriteList()
        self.explosion = arcade.SpriteList()

        #  create player
        self.BB8 = Player()
        self.BB8.center_x = SW/2
        self.BB8.center_y = SH/2
        self.BB8.bottom = 2
        self.player_list.append(self.BB8)

        # Create Troopers
        for i in range(self.trooper_count):
            trooper = Trooper()
            if i % 2 == 0:
                trooper.center_x = random.randrange(trooper.w, int(SW/2))
            else:
                trooper.center_x = random.randrange(int(SW*2/3), SW-trooper.w)
                trooper.center_y = random.randrange(trooper.h, SH - trooper.h)
                self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()

        if self.current_state == 0:
            arcade.draw_rectangle_filled(SW // 2, SH // 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Use Arrow keys to move and Space to fire. choose levels 1-3", SW / 2, SH / 2 - 20, ((0, 255, 0)), 14, align="center",
                             anchor_x="center")
        elif self.Gameover == False:
            arcade.draw_texture_rectangle(SW//2, SH//2, SW, SH, self.background)
            self.player_list.draw()
            self.trooper_list.draw()
            self.bullet_list.draw()
            self.ebullet_list.draw()
            self.explosion.draw()

            #  print the score
            arcade.draw_lrtb_rectangle_filled(SW-95, SW, SH, SH-35, arcade.color.WHITE)
            the_level = f"Level:{self.current_state}"
            arcade.draw_text(the_level, SW - 90, SH - 17, arcade.color.BLACK, 14)
            the_score = f"Score:{self.score}"
            arcade.draw_text(the_score, SW - 90, SH - 32, arcade.color.BLACK, 14)

        else:#  draw game over screen
            output = f"score:{self.score}"
            arcade.draw_rectangle_filled(SW//2, SH//2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game Over! Choose a level to Play Again: 1-3", SW/2, SH/2-20,((0, 255, 0)), 14, align="center", anchor_x="center")
            arcade.draw_text(output, SW / 2, SH / 2 - 40, ((0, 255, 0)), 14,
                             align="center", anchor_x="center")


    def on_update(self, dt):

        if self.current_state > 0 and self.current_state < 4:
            self.Gameover = False
        else:
            self.Gameover = True

        if not self.Gameover:
            self.player_list.update()
            self.trooper_list.update()
            self.bullet_list.update()
            self.ebullet_list.update()
            self.explosion.update()

            if len(self.trooper_list) == 0:
                self.current_state += 1
                self.reset()

        #  detect BB8 colliding with trooper
            bb8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
            if len(bb8_hit) > 0 and not self.Gameover:
                self.BB8.kill()
                self.current_state = 4
                self.Gameover=True

            # randomly drop Bomb
            for trooper in self.trooper_list:
                if random.randrange(800) == 0 and not self.Gameover:
                    ebullet = Enemy_bullet()
                    ebullet.center_x = trooper.center_x
                    ebullet.center_y = trooper.center_y
                    self.ebullet_list.append(ebullet)

            BB8_bombed = arcade.check_for_collision_with_list(self.BB8, self.ebullet_list)
            if len(BB8_bombed) > 0 and not self.Gameover:
                arcade.play_sound(self.BB8.explosion)
                self.BB8.kill()
                BB8_bombed[0].kill()
                self.current_state = 4
                self.Gameover = True

            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)
                if len(hit_list) > 0:
                    arcade.play_sound(bullet.explosion)
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    self.explosion.append(explosion)
                    self.bullet.kill()



                for trooper in hit_list:
                    trooper.kill()  # order 67
                    self.score += trooper_pts


    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT and not self.Gameover:
            self.BB8.change_angle = ANGLE_SPEED
        elif key == arcade.key.RIGHT and not self.Gameover:
            self.BB8.change_angle = -ANGLE_SPEED
        elif key == arcade.key.UP and not self.Gameover:
            self.BB8.speed = MOVEMENT_SPEED
        elif key == arcade.key.DOWN and not self.Gameover:
            self.BB8.speed = -MOVEMENT_SPEED
        elif key == arcade.key.P:
            self.reset()
        elif key == arcade.key.SPACE and not self.Gameover:
            self.bullet = Bullet()  # instantiate a bullet
            self.bullet.center_x = self.BB8.center_x
            self.bullet.center_y = self.BB8.center_y
            self.bullet.angle = self.BB8.angle + 90
            self.bullet.speed = bullet_speed
            self.bullet_list.append(self.bullet)
            self.score += bullet_pts
            arcade.play_sound(self.BB8.laser_sound)


            # level choosing
        if key == arcade.key.I and self.Gameover:
            self.current_state = 0
        elif key == arcade.key.KEY_1 and self.Gameover:
            self.current_state = 1
            self.score = 0
            self.reset()
        elif key == arcade.key.KEY_2 and self.Gameover:
            self.current_state = 2
            self.score = 0
            self.reset()
        elif key == arcade.key.KEY_3 and self.Gameover:
            self.current_state = 3
            self.score = 0
            self.reset()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT and not self.Gameover:
            self.BB8.change_angle = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN and not self.Gameover:
            self.BB8.speed = 0


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 trig aiming")
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
application.asset_folder = application.asset_folder.parent / "assets"
window.exit_button.visible = False

grass_texture = load_texture("grass_block.png")
stone_texture = load_texture("stone_block.png")
brick_texture = load_texture("brick_block.png")
dirt_texture = load_texture("dirt_block.png")
sky_texture = load_texture("skybox.png")
arm_texture = load_texture("arm_texture.png")
punch_sound = Audio("punch_sound", loop=False, autoplay=False)

block_pick = 1

pick_mapping = [
    grass_texture,
    stone_texture,
    brick_texture,
    dirt_texture
]


def update():
    global block_pick

    if held_keys["left mouse"] or held_keys["right mouse"]:
        arm.active()
    else:
        arm.passive()

    if held_keys["1"]:
        block_pick = 1
    if held_keys["2"]:
        block_pick = 2
    if held_keys["3"]:
        block_pick = 3
    if held_keys["4"]:
        block_pick = 4


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        voxel_color = color.color(0, 0, random.uniform(0.9, 1))
        super().__init__(
            parent=scene,
            position=position,
            model="block",
            origin_y=0.5,
            texture=texture,
            color=voxel_color,
            highlight_color=color.color(0, 0, 0.8),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == "right mouse down":
                punch_sound.play()
                Voxel(position=self.position + mouse.normal, texture=pick_mapping[block_pick - 1])
            if key == "left mouse down":
                punch_sound.play()
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=sky_texture,
            scale=150,
            double_sided=True
        )


class Arm(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model="arm",
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)


for x in range(20):
    for z in range(20):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()
sky = Sky()
arm = Arm()

app.run()

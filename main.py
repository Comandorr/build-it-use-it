from instruments import*

window = display.set_mode((win_w, win_h))
run = True
tilemap = image.load('sprite_map.png').convert_alpha()
Tiles = sprite.Group()
Obstacles = sprite.Group()
Items = sprite.Group()
Crates = sprite.Group()
world = []
menu = []
scene = 'menu'
# world / menu


class Player(sprite.Sprite):
    def __init__(self, img, x, y, size_x=0, size_y=0):
        super().__init__()
        self.image = image.load(img).convert_alpha()
        if size_x != 0:
            self.image = transform.scale(self.image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.visible = True
        self.speed = 2
        self.take_distance = 30

    def reset(self):
        if self.visible:
            window.blit(self.image, (self.rect.x, self.rect.y))
            for i in Items:
                if distance(self, i) < self.take_distance:
                    take_hint.rect.x = player.rect.x
                    take_hint.rect.bottom = player.rect.top
                    take_hint.reset()
            for i in Crates:
                if distance(self, i) < self.take_distance:
                    brake_hint.rect.x = player.rect.x
                    brake_hint.rect.bottom = player.rect.top
                    brake_hint.reset()

    def up(self):
        for t in world:
            t.rect.y += self.speed

    def down(self):
        for t in world:
            t.rect.y -= self.speed

    def left(self):
        for t in world:
            t.rect.x += self.speed

    def right(self):
        for t in world:
            t.rect.x -= self.speed

    def take(self):
        target = self.take_distance+1
        for i in Items:
            if distance(self, i) < target:
                target = distance(self, i)
        for i in Items:
            if distance(self, i) == target:
                Items.remove(i)
                resources[i.tip] += 1

    def brake(self):
        target = self.take_distance + 1
        for i in Crates:
            if distance(self, i) < target:
                target = distance(self, i)
        for i in Crates:
            if distance(self, i) == target:
                Crates.remove(i)
                print('\ncrate broken', i.rect.x, i.rect.y)
                for item in range(randint(2, 5)):
                    new_item(items, (i.rect.x+randint(-50, 50), i.rect.y+randint(-50, 50)), 24)

    def control(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.up()
            if sprite.spritecollide(self, Obstacles, False) or sprite.spritecollide(self, Crates, False):
                self.down()
        if keys[K_s]:
            self.down()
            if sprite.spritecollide(self, Obstacles, False) or sprite.spritecollide(self, Crates, False):
                self.up()
        if keys[K_d]:
            self.right()
            if sprite.spritecollide(self, Obstacles, False) or sprite.spritecollide(self, Crates, False):
                self.left()
        if keys[K_a]:
            self.left()
            if sprite.spritecollide(self, Obstacles, False) or sprite.spritecollide(self, Crates, False):
                self.right()
        if keys[K_e]:
            self.take()
        if keys[K_f]:
            self.brake()


class Tile(sprite.Sprite):
    def __init__(self, picture, position, size=(16, 16)):
        super().__init__()
        self.image = tilemap.subsurface((picture[0], picture[1], 16, 16))
        self.image = transform.scale(self.image, size)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.position = position

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Sprite(sprite.Sprite):
    def __init__(self, picture, position, size=(16, 16), tip=None):
        super().__init__()
        self.image = image.load(picture).convert_alpha()
        self.image = transform.scale(self.image, size)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.position = position
        self.tip = tip

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Button(sprite.Sprite):
    def __init__(self, position, size=(100, 50)):
        super().__init__()
        self.image = Surface(size)
        self.image.fill(gray)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.visible = True

    def reset(self):
        if self.visible:
            window.blit(self.image, (self.rect.x, self.rect.y))
        self.image.fill(gray)

    def update(self):
        if self.rect.collidepoint(mouse.get_pos()):
            self._func()

    def _func(self):
        self.image.fill(white)


class Text(sprite.Sprite):
    def __init__(self, text, position, f, back=None):
        super().__init__()
        self.image = f.render(text, 1, black, back)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class InventoryItem(sprite.Sprite):
    def __init__(self, position, img, _txt, txt2):
        _x = position[0]
        _y = position[1]
        self.img = Sprite(img, (_x + 15, _y), (70, 70))
        self.back = Button((_x, _y - 5), (100, 100))
        self.text = Text(_txt, (_x + 5, _y + 75), f22, white)
        self.text2 = Text(txt2, (_x + 5, _y), f28, white)

    def reset(self):
        self.back.reset()
        self.img.reset()
        self.text.reset()
        self.text2.reset()


def generate_map(size, tile):
    for x in range(int(-size[0]/2), int(size[0]/2)):
        for y in range(int(-size[1]/2), int(size[1]/2)):
            pic_x = randint(8, 15)
            pic_y = randint(0, 1)
            picture = (pic_x*16+pic_x, pic_y*16+pic_y)
            Tiles.add(Tile(picture, [center_x + x * tile, center_y + y * tile], (tile, tile)))


def generate_obstacles(area, start, end, size):
    for x in range(int(-area[0] / 2), int(area[0] / 2)):
        for y in range(int(-area[1] / 2), int(area[1] / 2)):
            if chance(3):
                pic_x = randint(start[0], start[1])
                pic_y = randint(end[0], end[1])
                picture = (pic_x * 16 + pic_x, pic_y * 16 + pic_y)
                Obstacles.add(Tile(picture, [center_x + x * size, center_y + y * size], (size, size)))


def generate_items(area, size, pictures):
    for x in range(int(-area[0] / 2), int(area[0] / 2)):
        for y in range(int(-area[1] / 2), int(area[1] / 2)):
            if chance(3):
                new_item(pictures, (center_x + x * size, center_y + y * size), size)


def new_item(pictures, position, size):
    x = position[0]
    y = position[1]
    picture = choice(pictures)
    tip = picture[7:len(picture) - 4]
    Items.add(Sprite(picture, [x, y], (size, size), tip=tip))
    print('item generated', position)


def generate_crates(area, size, pictures):
    for x in range(int(-area[0] / 2), int(area[0] / 2)):
        for y in range(int(-area[1] / 2), int(area[1] / 2)):
            if chance(3):
                picture = choice(pictures)
                Crates.add(Sprite(picture, [center_x + x * size, center_y + y * size], (size, size)))


def check_map():
    sprite.spritecollide(player, Crates, True)
    sprite.spritecollide(player, Items, True)
    sprite.spritecollide(player, Obstacles, True)
    sprite.groupcollide(Obstacles, Items, False, True)
    sprite.groupcollide(Obstacles, Crates, False, True)
    sprite.groupcollide(Crates, Items, False, True)


generate_map((100, 100), 32)
generate_obstacles((100, 100), (24, 30), (7, 8), 48)
# generate_items((100, 100), 24, items)
generate_crates((100, 100), 32, crates)
player = Player('character.png', win_w/2, win_h/2)
check_map()
b1 = Button((100, 200))
text1 = Text('кнопка', (100, 200), f36)
take_hint = Text('E', (100, 200), f36, gray)
brake_hint = Text('F', (100, 200), f36, gray)
inventory = []
for x in range(4):
    for y in range(2):
        r = items[x + y * 4]
        txt = r[7:len(r) - 4]
        item = InventoryItem((center_x + x * 125, center_y - 295 + y*120), r, txt, str(resources[txt]))
        menu.append(item)


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                if scene == 'world':
                    scene = 'menu'
                elif scene == 'menu':
                    scene = 'world'
        if e.type == MOUSEBUTTONDOWN and scene == 'menu':
            b1.update()

    window.fill(black)

    if scene == 'world':
        player.control()
        world = Tiles.sprites() + Obstacles.sprites() + Items.sprites() + Crates.sprites()
        for a in world:
            a.reset()
        player.reset()
    elif scene == 'menu':
        b1.reset()
        text1.reset()
        for m in menu:
            m.reset()

    fps = int(clock.get_fps())
    fps_text = Text('fps: '+str(fps), (0, 0), f24, gray)
    fps_text.reset()
    clock.tick_busy_loop(60)
    display.update()

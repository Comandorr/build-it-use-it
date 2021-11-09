from instruments import*

window = display.set_mode((win_w, win_h))
run = True
tilemap = image.load('sprite_map.png').convert_alpha()
Tiles = Group()
Obstacles = Group()
Items = Group()
Crates = Group()
world = []
menu = []
Robots = Group()
buddys = []
scene = 'world'
daytime = time.get_ticks()
day = 30
inventory_max = 15
inventory = 0
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
                global inventory
                inventory += 1

    def brake(self):
        target = self.take_distance + 1
        for i in Crates:
            if distance(self, i) < target:
                target = distance(self, i)
        for i in Crates:
            if distance(self, i) == target:
                Crates.remove(i)
                for j in range(randint(2, 5)):
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
        self.text = text
        self.image = f.render(text, 1, black, back)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class InventoryItem(sprite.Sprite):
    def __init__(self, position, img, _txt, txt2, tip='inventory'):
        super().__init__()
        _x = position[0]
        _y = position[1]
        self._x = _x
        self._y = _y
        self._txt = _txt
        self.img = Sprite(img, (_x + 15, _y), (70, 70))
        self.back = Button((_x, _y - 5), (100, 100))
        self.text = Text(_txt, (_x + 5, _y + 75), f22, white)
        self.text2 = Text(txt2, (_x + 5, _y), f28, white)
        self.tip = tip
        self.back._func = self.click

    def update_txt2(self):
        if self.tip == 'inventory':
            _txt2 = str(resources[self._txt])
        elif self.tip == 'robot':
            _txt2 = str(squad[self._txt])
        self.text2 = Text(_txt2, (self._x + 5, self._y), f28, white)

    def reset(self):
        self.update_txt2()
        self.back.reset()
        self.img.reset()
        self.text.reset()
        self.text2.reset()

    def click(self):
        global selected
        selected = self
        if self.tip == 'robot':
            select()


class Robot(sprite.Sprite):
    def __init__(self, img, speed=1):
        super().__init__()
        self.image = image.load('images/'+img+'.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 100
        self.rect.y = player.rect.y
        self.speed = speed
        Robots.add(self)

    def update(self):
        vector = [0, 0]
        vector[0] = player.rect.x + randint(-10, 10) - self.rect.x
        vector[1] = player.rect.y + randint(-10, 10) - self.rect.y
        move = [0, 0]
        if vector[0] > 0:
            move[0] = 1
        elif vector[0] < 0:
            move[0] = -1
        if vector[1] > 0:
            move[1] = 1
        elif vector[1] < 0:
            move[1] = -1

        self.rect.x += move[0] * self.speed
        if sprite.spritecollide(self, Obstacles, False) \
                or sprite.spritecollide(self, Crates, False)\
                or sprite.collide_rect(self, player):
            self.rect.x -= move[0] * self.speed
        self.rect.y += move[1] * self.speed
        if sprite.spritecollide(self, Obstacles, False)\
                or sprite.spritecollide(self, Crates, False)\
                or sprite.collide_rect(self, player):
            self.rect.y -= move[1] * self.speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


def generate_map(size, tile):
    for x in range(int(-size[0]/2), int(size[0]/2)):
        for y in range(int(-size[1]/2), int(size[1]/2)):
            pic_x = randint(8, 15)
            pic_y = randint(0, 1)
            picture = (pic_x * 16 + pic_x, pic_y * 16 + pic_y)
            Tiles.add(Tile(picture, [center_x + x * tile, center_y + y * tile], (tile, tile)))


def generate_obstacles(area, start, end, size):
    for x in range(int(-area[0] / 2), int(area[0] / 2)):
        for y in range(int(-area[1] / 2), int(area[1] / 2)):
            if chance(5):
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


def generate_crates(area, size, pictures):
    for x in range(int(-area[0] / 2), int(area[0] / 2)):
        for y in range(int(-area[1] / 2), int(area[1] / 2)):
            if chance(1):
                picture = choice(pictures)
                Crates.add(Sprite(picture, [center_x + x * size, center_y + y * size], (size, size)))


def check_map():
    sprite.spritecollide(player, Crates, True)
    sprite.spritecollide(player, Items, True)
    sprite.spritecollide(player, Obstacles, True)
    sprite.groupcollide(Obstacles, Items, False, True)
    sprite.groupcollide(Obstacles, Crates, False, True)
    sprite.groupcollide(Crates, Items, False, True)
    sprite.groupcollide(Robots, Crates, False, True)
    sprite.groupcollide(Robots, Obstacles, False, True)


def select():
    global selected
    img_build.image = image.load('images/' + selected._txt + '.png').convert_alpha()
    img_build.image = transform.scale(img_build.image, (100, 100))
    for i in buddys:
        if i.name == selected._txt:
            robo = i

    for t in menu_texts:
        res = t.text.split()[0]
        t.image = f22.render(res + ' - ' + str(resources[res]) + ' / ' + str(robo.recipe[res]), 1, black, white)


for i in squad:
    recipe = {}
    for r in resources:
        recipe[r] = randint(0, 3)
    buddys.append(Buddy(i, recipe, randint(1, 4)/2))
selected = buddys[0]

generate_map((150, 150), 32)
generate_obstacles((100, 100), (24, 30), (7, 8), 48)
# generate_items((100, 100), 24, items)
generate_crates((150, 150), 32, crates)
player = Player('character.png', win_w/2, win_h/2)
check_map()
b1 = Button((225, 550), (200, 50))
b0 = Button((win_w-225, 550), (200, 50))
text1 = Text('построить', (b1.rect.x + 15, b1.rect.y + 5), f48)
text0 = Text('продолжить', (b0.rect.x + 5, b1.rect.y + 10), f44)
take_hint = Text('E', (100, 200), f36, gray)
brake_hint = Text('F', (100, 200), f36, gray)
for x in range(4):
    for y in range(2):
        r = items[x + y * 4]
        txt = r[7:len(r) - 4]
        item = InventoryItem((center_x + x * 125, center_y - 295 + y*120), r, txt, str(resources[txt]))
        menu.append(item)

for x in range(len(buddys) % 5):
    for y in range(len(buddys) // 5 + 1):
        r = 'images/' + buddys[x + y * 4].name + '.png'
        txt = buddys[x + y * 4].name
        item = InventoryItem((100 + x * 125, center_y - 295 + y*120), r, txt, str(squad[txt]), tip='robot')
        menu.append(item)

b2 = Button((100, 250), (200, 250))
b3 = Button((350, 250), (200, 250))
img_build = Sprite(robots[0], (b2.rect.x+50, b2.rect.y+50),  size=(100, 100))
menu_texts = []


def build():
    for i in buddys:
        if i.name == selected._txt:
            robo = i
    buildable = True
    for i in resources:
        if resources[i] < robo.recipe[i]:
            buildable = False
    if buildable:
        for i in resources:
            resources[i] -= robo.recipe[i]
        squad[robo.name] += 1
        Robot(robo.name)
        check_map()
        if robo.name == 'cargo':
            global inventory_max
            inventory_max += 10
        elif robo.name == 'searcher':
            global day
            day += 15


def next_day():
    global scene, daytime, inventory
    scene = 'world'
    daytime = time.get_ticks()
    inventory = 0


b1._func = build
b0._func = next_day

c = b3.rect.y
for i in resources:
    c += 25
    text = i + ' - ' + str(resources[i]) + ' / ' + str(buddys[0].recipe[i])
    menu_texts.append(Text(text, (b3.rect.x + 20, c), f24, white))
menu2 = [b0, b1, b2, b3, text0, text1, img_build]


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN and scene == 'menu':
            b1.update()
            b0.update()
            for item in menu:
                item.back.update()

    window.fill(black)

    if scene == 'world':
        player.control()
        world = Tiles.sprites() + Obstacles.sprites() + Items.sprites() + Crates.sprites() + Robots.sprites()
        for a in world:
            a.reset()
        Robots.update()
        Robots.reset()
        player.reset()
    elif scene == 'menu':
        for m in menu + menu2 + menu_texts:
            m.reset()

    fps = int(clock.get_fps())
    fps_text = Text('fps: '+str(fps), (0, 0), f24, gray)
    if scene == 'world':
        time_left = day-(time.get_ticks()-daytime)/1000
        if time_left < 10:
            time_text = Text('Время '+str(round(time_left, 2)), (win_w - 175, 0), f36, red)
        else:
            time_text = Text('Время '+str(round(time_left, 2)), (win_w - 175, 0), f36, gray)
        if time_left <= 0:
            scene = 'menu'
        time_text.reset()
        if (inventory_max - inventory) <= 5:
            inventory_text = Text('Рюкзак '+str(inventory) + '/' + str(inventory_max), (win_w - 175, 30), f36, red)
        else:
            inventory_text = Text('Рюкзак '+str(inventory) + '/' + str(inventory_max), (win_w - 175, 30), f36, gray)
        inventory_text.reset()
        if inventory >= inventory_max:
            scene = 'menu'

    fps_text.reset()
    clock.tick_busy_loop(60)
    display.update()

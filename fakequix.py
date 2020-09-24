import pygame
import pygame.freetype
import random

class SimpleScene:

    FONT = None

    def __init__(self, next_scene, *text):
        self.background = pygame.Surface((640, 480))
        self.background.fill(pygame.Color('lightgrey'))

        y = 80
        if text:
            if SimpleScene.FONT == None:
                SimpleScene.FONT = pygame.freetype.SysFont(None, 32)
            for line in text:
                SimpleScene.FONT.render_to(self.background, (120, y), line, pygame.Color('black'))
                SimpleScene.FONT.render_to(self.background, (119, y-1), line, pygame.Color('white'))
                y += 50

        self.next_scene = next_scene
        self.additional_text = None

    def start(self, text):
        self.additional_text = text

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        if self.additional_text:
            y = 180
            for line in self.additional_text:
                SimpleScene.FONT.render_to(screen, (120, y), line, pygame.Color('black'))
                SimpleScene.FONT.render_to(screen, (119, y-1), line, pygame.Color('white'))
                y += 50

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return (self.next_scene, None)

class GameState:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.questions = [
            ('How many legs has a cow?', 4),
            ('How many legs has a bird?', 2),
            ('What is 1 x 1 ?', 1)
        ]
        self.current_question = None
        self.right = 0
        self.wrong = 0

    def pop_question(self):
        q = random.choice(self.questions)
        self.questions.remove(q)
        self.current_question = q
        return q

    def answer(self, answer):
        if answer == self.current_question[1]:
            self.right += 1
        else:
            self.wrong += 1

    def get_result(self):
        return f'{self.right} answers correct', f'{self.wrong} answers wrong', '', 'Good!' if self.right > self.wrong else 'You can do better!'

class SettingScene:

    def __init__(self):
        self.background = pygame.Surface((640, 480))
        self.background.fill(pygame.Color('lightgrey'))

        if SimpleScene.FONT == None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 32)

        SimpleScene.FONT.render_to(self.background, (120, 50), 'Select your difficulty level', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (119, 49), 'Select your difficulty level', pygame.Color('white'))

        self.rects = []
        x = 120
        y = 120
        for n in range(4):
            rect = pygame.Rect(x, y, 80, 80)
            self.rects.append(rect)
            x += 100

    def start(self, *args):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        n = 1
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color('darkgrey'), rect)
            pygame.draw.rect(screen, pygame.Color('darkgrey'), rect, 5)
            SimpleScene.FONT.render_to(screen, (rect.x+30, rect.y+30), str(n), pygame.Color('black'))
            SimpleScene.FONT.render_to(screen, (rect.x+29, rect.y+29), str(n), pygame.Color('white'))
            n+=1

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        return ('GAME', GameState(n))
                    n += 1

class GameScene:
    def __init__(self):
        if SimpleScene.FONT == None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 32)

        self.rects = []
        x = 120
        y = 120
        for n in range(4):
            rect = pygame.Rect(x, y, 80, 80)
            self.rects.append(rect)
            x += 100

    def start(self, gamestate):
        self.background = pygame.Surface((640, 480))
        self.background.fill(pygame.Color('lightgrey'))
        self.gamestate = gamestate
        question, answer = gamestate.pop_question()
        SimpleScene.FONT.render_to(self.background, (120, 50), question, pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (119, 49), question, pygame.Color('white'))


    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        n = 1
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color('darkgrey'), rect)
            pygame.draw.rect(screen, pygame.Color('darkgrey'), rect, 5)
            SimpleScene.FONT.render_to(screen, (rect.x+30, rect.y+30), str(n), pygame.Color('black'))
            SimpleScene.FONT.render_to(screen, (rect.x+29, rect.y+29), str(n), pygame.Color('white'))
            n+=1

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        self.gamestate.answer(n)
                        if self.gamestate.questions:
                            return ('GAME', self.gamestate)
                        else:
                            return ('RESULT', self.gamestate.get_result())
                    n += 1

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    dt = 0
    scenes = {
        'TITLE':    SimpleScene('SETTING', 'Welcome to the quiz', '', '', '', 'press [SPACE] to start'),
        'SETTING':  SettingScene(),
        'GAME':     GameScene(),
        'RESULT':   SimpleScene('TITLE', 'Here is your result:'),
    }
    scene = scenes['TITLE']
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        result = scene.update(events, dt)
        if result:
            next_scene, state = result
            if next_scene:
                scene = scenes[next_scene]
                scene.start(state)

        scene.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60)

if __name__ == '__main__':
    main()
import os
import pygame
pygame.init()

SIZE = WIDTH, HEIGHT = 720, 480
BACKGROUND_COLOR = pygame.Color('white')
FPS = 60

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (720,480))
DISPLAYSURF = pygame.display.set_mode((720,480))
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


def load_images(path):
    """
    모든 이미지를 디렉토리에 로드함. 디렉토리는 이미지만 포함해야함.

    Args:
        경로 : 이미지를 로드 할 디렉토리의 상위경로 or 절대경로

    Returns:
        이미지 목록
    """
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert()
        images.append(image)
    return images

class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position, images):
        """
        애니메이션 스프라이트 개체

        Args:
            position: AnimationSprite를 배치할 x,y좌표
            images: 애니메이션에서 사용될 이미지
        """
        super(AnimatedSprite, self).__init__()

        size = (160, 200)  # 이미지의 크기와 일치해야함

        self.rect = pygame.Rect(position, size)
        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]  # 모든 이미지 뒤집기
        self.index = 0
        self.image = images[self.index]  # 'image' 는 애니메이션에서의 현재 이미지

        self.velocity = pygame.math.Vector2(0, 0)

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_time_dependent(self, dt):
        """
        약 0.1초마다 스프라이트 이미지를 업데이트

        Args:
            dt: 각 프레임 사이의 경과시간
        """
        if self.velocity.x > 0:  # 스프라이트가 오른쪽으로 움직일 때, 올바른 이미지를 사용할 것.
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.move_ip(*self.velocity)

    def update_frame_dependent(self):
        """
       6프레임마다 스프라이트 이미지를 업데이트 (프레임속도가 60이면 약 0.1초마다 바꿈
        """
        if self.velocity.x > 0:  # 스프라이트가 오른족으로 움직일 때, 올바른 이미지를 사용할 것.
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.move_ip(*self.velocity)

    def update(self, dt):
        """이것은 'all_sprites.update (dt)가 호출될 때 나오는 메소드임."""
        # 주석 달기/주석 해제를 통해서 두 가지 업데이트 방법을 전환하세요.
        self.update_time_dependent(dt)
        # self.update_frame_dependent()

def main():
    images = load_images(path='C:\\Users\\admin\\Desktop\\pacman')  # 이미지 디렉토리에 상대경로/전체경로를 적을것. (\가 하나만 있을때 유니코드 에러가 나므로 \\로 바꿀것)
    player = AnimatedSprite(position=(100, 100), images=images)
    all_sprites = pygame.sprite.Group(player)  # 스프라이트 그룹생성, 그곳에 player를 추가함.

    running = True
    while running:

        dt = clock.tick(FPS) / 1000  # 각 루프사이의 시간 (초)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.velocity.x = 4
                elif event.key == pygame.K_LEFT:
                    player.velocity.x = -4
                elif event.key == pygame.K_DOWN:
                    player.velocity.y = 4
                elif event.key == pygame.K_UP:
                    player.velocity.y = -4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.velocity.x = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    player.velocity.y = 0

        all_sprites.update(dt)  # 목록의 모든 스프라이트(현재는 Player만 해당.) 에서 'update'메소드 호출

        DISPLAYSURF.blit(background,(0,0))
        all_sprites.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
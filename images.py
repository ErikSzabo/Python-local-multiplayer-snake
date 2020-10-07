import pygame

class Image:
    """Játékban használt képek statikus tárolója."""

    snake_heads = [
        [
            pygame.image.load("assets/images/head1_left.png"),
            pygame.image.load("assets/images/head1_right.png"),
            pygame.image.load("assets/images/head1_down.png"),
            pygame.image.load("assets/images/head1_up.png")
        ],
        [
            pygame.image.load("assets/images/head2_left.png"),
            pygame.image.load("assets/images/head2_right.png"),
            pygame.image.load("assets/images/head2_down.png"),
            pygame.image.load("assets/images/head2_up.png")
        ]
    ]

    food_image = pygame.image.load("assets/images/apple.png")
    super_food_image = pygame.image.load("assets/images/super_apple.png")
    menu_left_arrow = pygame.image.load("assets/images/left_arrow.png")
    menu_right_arrow = pygame.image.load("assets/images/right_arrow.png")
    menu_control = [pygame.image.load("assets/images/arrow_control.png"),
                    pygame.image.load("assets/images/wasd_control.png")]

    @staticmethod
    def scale_game_images(grid_size):
        """
        Átméretezi a játékban használt képeket a négyzetrács méretének megfelelően.
        Paraméterek:
            grid_size: négyzetrács mérete
        """
        for heads in Image.snake_heads:
            for i in range(len(heads)):
                heads[i] = pygame.transform.scale(heads[i], (grid_size, grid_size))

        Image.food_image = pygame.transform.scale(Image.food_image, (grid_size, grid_size))
        Image.super_food_image = pygame.transform.scale(Image.super_food_image, (grid_size, grid_size))
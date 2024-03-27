import pytest
import pygame
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import sys

# Додаємо шлях до директорії з кодом, який потрібно протестувати
global_dir = Path(__file__).parent.parent / 'src'
sys.path.append(str(global_dir))
# Додаємо шлях до директорії з кодом, який потрібно протестувати
from GameScene import GameScene

@pytest.fixture(autouse=True)
def mock_pygame():
    mock_surface = MagicMock()
    mock_surface.convert.return_value = mock_surface
    mock_surface.convert_alpha.return_value = mock_surface
    mock_surface.get_size.return_value = (800, 600)
    mock_surface.get_width.return_value = 800
    mock_surface.get_height.return_value = 600

    with patch('pygame.Surface', return_value=mock_surface), \
         patch('pygame.image.load', return_value=mock_surface), \
         patch('pygame.display.set_mode', return_value=mock_surface), \
         patch('pygame.display.init'), \
         patch('pygame.font.Font', return_value=MagicMock()), \
         patch('pygame.sprite.Group', return_value=MagicMock()), \
         patch('pygame.transform.scale', return_value=mock_surface), \
         patch('pygame.key.get_pressed', return_value=[False] * 300), \
         patch('pygame.event.get', return_value=[]):  # Мок для подій, щоб уникнути зациклювання у тесті
        yield


@pytest.fixture(autouse=True)
def mock_file_io():
    with patch('builtins.open', mock_open(read_data='10')), \
         patch('struct.unpack', return_value=(0.5,)):
        yield

def test_game_scene_initialization():
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600

    num_players = 2

    game_scene = GameScene(screen, num_players)

    assert game_scene.num_players == num_players
    assert isinstance(game_scene.players, list)
    assert len(game_scene.players) == num_players

def test_game_scene_event_handling():
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600

    with patch('GameScene.Road') as MockRoad:
        mock_road_instance = MockRoad.return_value
        mock_road_instance.rect.top = 400
        mock_road_instance.screen_height = 600
        mock_road_instance.get_edge_coordinates.return_value = (100, 700)

        game_scene = GameScene(screen, 1)

        game_scene.road1.rect.top = 400
        game_scene.road2.rect.top = 400

        if hasattr(game_scene, 'road3'):
            game_scene.road3.rect.top = 400

        with patch('pygame.event.get') as mock_get, \
             patch('pygame.display.flip'):  # Замокати pygame.display.flip, щоб уникнути помилки ініціалізації
            mock_get.return_value = [MagicMock(type=pygame.QUIT)]
            game_scene.run()

def test_game_scene_player_movement_handling():
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600

    with patch('GameScene.Road') as MockRoad, \
         patch('GameScene.Player') as MockPlayer:  # Мокуємо клас гравця
        mock_road_instance = MockRoad.return_value
        mock_road_instance.rect.top = 400
        mock_road_instance.screen_height = 600
        mock_road_instance.get_edge_coordinates.return_value = (100, 700)

        mock_player_instance = MockPlayer.return_value
        mock_player_instance.rect = MagicMock(x=100, y=100)  # Припустиме початкове положення гравця

        game_scene = GameScene(screen, 1)
        game_scene.road1.rect.top = 400
        game_scene.road2.rect.top = 400

        player_initial_x = game_scene.players[0].rect.x  # Тепер це має працювати без помилок
        player_initial_y = game_scene.players[0].rect.y

        with patch('pygame.event.get') as mock_get, \
             patch('pygame.display.flip'):
            mock_get.return_value = [MagicMock(type=pygame.QUIT)]
            game_scene.run_one_frame()

            # Тепер можна перевірити, чи змінилися координати гравця після виконання run_one_frame()




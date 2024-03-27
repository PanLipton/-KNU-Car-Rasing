import pytest
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
    # Налаштування повернення коректних значень для get_size
    mock_surface.get_size.return_value = (800, 600)
    mock_surface.get_width.return_value = 800
    mock_surface.get_height.return_value = 600

    with patch('pygame.Surface', return_value=mock_surface), \
         patch('pygame.image.load', return_value=mock_surface), \
         patch('pygame.display.set_mode', return_value=mock_surface), \
         patch('pygame.display.init'), \
         patch('pygame.font.Font', return_value=MagicMock()), \
         patch('pygame.sprite.Group', return_value=MagicMock()), \
         patch('pygame.transform.scale', return_value=mock_surface):
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


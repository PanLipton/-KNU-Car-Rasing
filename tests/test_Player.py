import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add path to the directory with the code to be tested
global_dir = Path(__file__).parent.parent / 'src'
sys.path.append(str(global_dir))
from Player.Player import APlayer  # Adjust the import according to your actual package structure

@pytest.fixture(autouse=True)
def mock_pygame():
    mock_surface = MagicMock()
    mock_surface.convert.return_value = mock_surface
    mock_surface.convert_alpha.return_value = mock_surface
    mock_surface.get_size.return_value = (100, 100)  # Modify as needed
    mock_surface.get_width.return_value = 100
    mock_surface.get_height.return_value = 100

    with patch('pygame.Surface', return_value=mock_surface), \
         patch('pygame.image.load', return_value=mock_surface), \
         patch('pygame.display.set_mode', return_value=mock_surface), \
         patch('pygame.display.flip'), \
         patch('pygame.font.Font', return_value=MagicMock()), \
         patch('pygame.sprite.Group', return_value=MagicMock()), \
         patch('pygame.transform.scale', return_value=mock_surface), \
         patch('pygame.time.get_ticks', return_value=1000):
        yield

@pytest.fixture
def initialized_player():
    screen = MagicMock()
    player = APlayer(screen, '../assets/cars/player-car-1.png', 100, 100, 50, 50)
    return player

@pytest.mark.player
@pytest.mark.parametrize("movement_distance, expected_x", [
    (10, 110),
    (-10, 90),
    (0, 100)
])
def test_player_movement(initialized_player, movement_distance, expected_x):
    initial_x = initialized_player._x
    initialized_player.MoveRight(movement_distance, [])
    assert initialized_player._x == initial_x + movement_distance

@pytest.mark.player
def test_score_management(initialized_player):
    initial_score = initialized_player.get_score()
    initialized_player.change_score(5)
    assert initialized_player.get_score() == initial_score + 5
    initialized_player.change_score(-3)
    assert initialized_player.get_score() == initial_score + 2

@pytest.mark.explosion
@pytest.mark.parametrize("explosion_sheet, frame_width, frame_height", [
    ('explosion1.png', 64, 64),
    ('explosion2.png', 32, 32)
])
def test_explosion_animation_loading(initialized_player, explosion_sheet, frame_width, frame_height):
    initialized_player._load_explosion_frames(explosion_sheet, frame_width, frame_height)
    assert len(initialized_player._explosion_animation) > 0  # Assuming the sheet contains multiple frames

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys

# Add the parent directory to the sys.path
global_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(global_dir))

# Importing Pygame after adding parent directory to sys.path
import pygame

from Bot.Bot import Bot

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
         patch('pygame.transform.scale', return_value=mock_surface):
        yield


@pytest.fixture
def screen():
    # Create a MagicMock object representing the Pygame screen
    screen_mock = MagicMock(name='pygame.Surface', spec=pygame.surface.Surface)
    screen_mock.get_width.return_value = 1000
    screen_mock.get_height.return_value = 1000
    screen_mock.fill.return_value = None  # Add any necessary methods and attributes
    return screen_mock


@pytest.mark.move_down
@pytest.mark.parametrize("distance, initial_y", [
    (5, 50),
    (10, 100),
    (15, 150),
    (20, 200)
])
def test_MoveDown(screen, distance, initial_y):
    # Create a Bot object
    bot = Bot(screen, "bot-1.png", 150, initial_y, 50, 100)
    
    # Get the initial location of the bot
    initial_location = bot.getActorLocation()
    
    # Call the MoveDown method with the specified distance
    bot.MoveDown(distance)
    
    # Get the updated location of the bot
    updated_location = bot.getActorLocation()
    
    # Assert that the bot's y-coordinate has been updated correctly
    assert updated_location[1] == initial_location[1] + distance
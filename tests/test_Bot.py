import sys
import os
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add the parent directory to the sys.path
global_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(global_dir))

# Importing Pygame after adding parent directory to sys.path
import pygame

from Bot.Bot import Bot

import sys
import os
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add the parent directory to the sys.path
src_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(src_dir))

# Importing Pygame after adding parent directory to sys.path
import pygame

from Bot.Bot import Bot

@pytest.fixture
def screen():
    # Create a MagicMock object representing a Pygame surface
    screen_mock = MagicMock(name='pygame.Surface', spec=pygame.surface.Surface)
    screen_mock.get_width.return_value = 1000
    screen_mock.get_height.return_value = 1000
    screen_mock.fill.return_value = None  # Add any necessary methods and attributes
    return screen_mock

@pytest.fixture
def mocked_load():
    # Mocking the pygame.image.load function
    with patch('pygame.image.load') as mock_load:
        # Create a MagicMock object representing a Pygame surface
        mock_image = MagicMock(name='pygame.Surface', spec=pygame.surface.Surface)
        mock_image.convert_alpha.return_value = mock_image
        # Return the MagicMock object
        mock_load.return_value = mock_image
        
        # Mocking the pygame.transform.scale function
        with patch('pygame.transform.scale') as mock_scale:
            # Return the original mock_image without scaling
            mock_scale.return_value = mock_image
            
            yield mock_load

@pytest.mark.move_down
@pytest.mark.parametrize("distance, initial_y", [
    (5, 50),
    (10, 100),
    (15, 150),
    (20, 200)
])
def test_MoveDown(screen, mocked_load, distance, initial_y):
    # Mock the path to the image file
    image_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'cars', 'bot-1.png')
    print(f"Type of screen: {type(screen)}")  # Add this line for debugging
    
    # Create a Bot object
    bot = Bot(screen, image_path, 150, initial_y, 50, 100)
    
    # Get the initial location of the bot
    initial_location = bot.getActorLocation()
    
    # Call the MoveDown method with the specified distance
    bot.MoveDown(distance)
    
    # Get the updated location of the bot
    updated_location = bot.getActorLocation()
    
    # Assert that the bot's y-coordinate has been updated correctly
    assert updated_location[1] == initial_location[1] + distance
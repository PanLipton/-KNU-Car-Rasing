import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

global_dir = Path(__file__).parent.parent / 'src'
sys.path.append(str(global_dir))

from Menu.BaseMenu import BaseMenu


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
def mock_gui_manager():
    return MagicMock()


@pytest.fixture
def mock_menu_manager():
    return MagicMock()


@pytest.fixture
def mock_screen():
    return MagicMock()


@pytest.fixture
def base_menu(mock_screen, mock_gui_manager, mock_menu_manager):
    return BaseMenu(mock_screen, mock_gui_manager, mock_menu_manager, 'background_image.png')


@pytest.mark.parametrize("method_to_test", [
    ("draw_background",),
    ("draw",)  # Assuming the correct method name is draw
])
def test_draw_methods(base_menu, mock_screen, method_to_test):
    method_name = method_to_test[0]
    getattr(base_menu, method_name)()
    mock_screen.blit.assert_called_once()
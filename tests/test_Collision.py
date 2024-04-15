import sys
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add the parent directory to the sys.path
global_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(global_dir))

# Import the Collision module after mocking pygame
from Collision.Collision import UBoxCollision

@pytest.fixture
def mock_screen():
    return MagicMock()

@pytest.fixture
def collision(request, mock_screen):  
    x, y, w, h, color = request.param
    return UBoxCollision(mock_screen, x, y, w, h, color)
@pytest.mark.collision_interaction
@pytest.mark.parametrize(
    "collision",
    [(0, 0, 50, 100, 'White'),  # Test case 1 parameters
     (49, 0, 50, 100, 'White')],  # Test case 2 parameters
    indirect=True  # Indicate that the fixture is used for parametrization
)
def test_collision_interaction(collision, mock_screen):
    # Mocking the colliderect method of pygame.Rect
    with patch('pygame.Rect', MagicMock(return_value=True)):
        assert collision.colliderect(collision)

@pytest.mark.set_coordinates
@pytest.mark.parametrize(
    "collision, coordinates",
    [((50, 0, 50, 100, 'White'), (200, 300)),  # Test case 1 parameters
     ((50, 0, 50, 100, 'White'), (400, 500))],  # Test case 2 parameters
    indirect=["collision"]  # Indicate that the "collision" fixture is used for parametrization
)
def test_set_coordinates(collision, mock_screen, coordinates):
    with patch('pygame.Rect', MagicMock()):
        collision.setCoordinates(coordinates)
        assert collision.x == coordinates[0]
        assert collision.y == coordinates[1]
@pytest.mark.update_rect
@pytest.mark.parametrize(
    "collision",
    [(50, 0, 50, 100, 'White')],  # Test case parameters
    indirect=True  # Indicate that the fixture is used for parametrization
)
def test_update_rect(collision, mock_screen):
    with patch('pygame.Rect', MagicMock()):
        collision._updateRect()
        assert collision.left == collision.x
        assert collision.top == collision.y

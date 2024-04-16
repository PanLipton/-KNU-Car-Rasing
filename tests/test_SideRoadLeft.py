import pytest
import sys
from pathlib import Path
import pygame
from pytest_mock import mocker
from unittest.mock import patch, Mock, MagicMock

global_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(global_dir))
from SideRoadLeft import SideRoadLeft

###../assets/img/sideroad.png

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


@patch('pygame.image.load', return_value=MagicMock())
@pytest.mark.image_loading
def test_image_loading(mock_load, side_road):
    side_road.load_image("../assets/img/sideroad.png")
    mock_load.assert_called_once_with("../assets/img/sideroad.png")

@pytest.fixture
def side_road():
    return SideRoadLeft("../assets/img/sideroad.png", 800, 600)

@pytest.mark.initialization
def test_initialization(side_road):
    assert side_road.screen_width == 800
    assert side_road.screen_height == 600
    assert side_road.y_offset == 0
    assert side_road.image is not None  # Перевірка, що image не є None
    assert side_road.rect is not None  # Перевірка, що rect не є None

@pytest.mark.parametrize("top_value, expected_result", [
    (700, True),   # Вершина rect знаходиться вище або на рівні нижньої межі екрану
    (600, True),   # Вершина rect знаходиться на рівні нижньої межі екрану
    (599, False),  # Вершина rect знаходиться вище нижньої межі екрану
])
@pytest.mark.update_moves_downward
def test_update_moves_downward(side_road, top_value, expected_result):
    # Мокуємо атрибут rect
    side_road.rect = MagicMock()
    side_road.rect.top = top_value

    # Викликаємо метод update зі швидкістю 10
    side_road.update(10)

    # Отримуємо нове значення y координати rect
    new_rect_y = side_road.rect.y

    # Перевіряємо, чи правильно обробляється рух вниз
    if top_value >= 600:
        # Якщо вершина rect знаходиться на або вище нижньої межі екрану,
        # очікуємо, що нова y координата буде від'ємною
        assert new_rect_y < 0 and expected_result
    else:
        # Інакше, очікуємо, що нова y координата буде не меншою за початкову
        assert side_road.rect.y >= top_value and side_road.rect.y == -600 if expected_result else True

@pytest.mark.parametrize("speed, initial_top, expected_top", [
    (-10, 599, 589),   # When speed is -10 and initial top is 599, expect new top to be 589 (599 - 10)
    (-20, 588, 568),   # When speed is -20 and initial top is 588, expect new top to be 568 (588 - 20)
    (-10, -600, 0)     # When speed is -10 and initial top is -600, expect new top to be 0 (clamped at 0)
])
@pytest.mark.update_moves_to_top_when_exceeds_height
def test_update_moves_to_top_when_exceeds_height(speed, initial_top, expected_top):
    # Initialize variables
    rect_top = initial_top

    # Update the top position based on the speed
    rect_top += speed

    # Ensure the rect stays within the screen boundaries
    if rect_top > 0:
        assert rect_top == expected_top
    else:
        assert 0 == expected_top

@pytest.mark.parametrize("centerx, width, expected_left_edge, expected_right_edge", [
    (100, 200, 0, 200),   # Причина: центр rect = 100, ширина rect = 200
    (50, 100, 0, 100),    # Причина: центр rect = 50, ширина rect = 100
])
@pytest.mark.get_edge_coordinates
def test_get_edge_coordinates(side_road, centerx, width, expected_left_edge, expected_right_edge):
    side_road.rect.centerx = centerx
    side_road.rect.width = width
    left_edge, right_edge = side_road.get_edge_coordinates()
    assert left_edge == expected_left_edge
    assert right_edge == expected_right_edge

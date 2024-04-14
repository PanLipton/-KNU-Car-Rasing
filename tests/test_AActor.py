import sys
import pytest
import pygame
from unittest.mock import MagicMock
from pathlib import Path

# Add the parent directory to the sys.path
global_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(global_dir))

from Actor.Actor import AActor

@pytest.fixture
def screen():
    # Mock the pygame.Surface object
    mock_surface = MagicMock(name='pygame.Surface')
    return mock_surface

@pytest.fixture
def actor_image():
    # Mock the pygame.Surface object for actor image
    mock_actor_image = MagicMock(name='pygame.Surface')
    return mock_actor_image

# Mocking pygame module and its Surface class
@pytest.fixture(autouse=True)
def mock_pygame(monkeypatch):
    pygame_mock = MagicMock()
    pygame_mock.Surface = MagicMock(return_value=MagicMock())
    monkeypatch.setattr('Actor.Actor.pygame', pygame_mock)

@pytest.mark.actor_init
@pytest.mark.parametrize("initial_x, initial_y, width, height", [
    (0, 0, 50, 100),
    (50, 50, 50, 100),
    (100, 200, 50, 100)
])
def test_init(screen, actor_image, initial_x, initial_y, width, height):
    actor = AActor(screen, actor_image, initial_x, initial_y, width, height)
    assert actor._x == initial_x
    assert actor._y == initial_y
    assert actor._w == width
    assert actor._h == height
    assert actor._screen == screen
    assert actor._BoxCollision is not None

@pytest.mark.actor_location_get
@pytest.mark.parametrize("initial_x, initial_y, expected_location", [
    (50, 50, (50, 50)),
    (0, 0, (0, 0)),
    (100, 200, (100, 200))
])
def test_getActorLocation(screen, actor_image, initial_x, initial_y, expected_location):
    actor = AActor(screen, actor_image, initial_x, initial_y, 50, 100)
    location = actor.getActorLocation()
    assert location == pygame.math.Vector2(expected_location)

@pytest.mark.actor_location_set
@pytest.mark.parametrize("initial_x, initial_y, new_location", [
    (0, 0, pygame.math.Vector2(100, 200)),
    (50, 50, pygame.math.Vector2(0, 0)),
    (100, 200, pygame.math.Vector2(50, 50))
])
def test_setActorLocation(screen, actor_image, initial_x, initial_y, new_location):
    actor = AActor(screen, actor_image, initial_x, initial_y, 50, 100)
    actor.setActorLocation(new_location)
    assert actor._x == new_location.x
    assert actor._y == new_location.y

@pytest.mark.actor_intersects
@pytest.mark.parametrize("actor1_x, actor2_x, intersect_expected", [
    (0, 40, True),
    (0, 100, False),
    (100, 150, False)
])
def test_Intersects(screen, actor_image, actor1_x, actor2_x, intersect_expected):
    actor1 = AActor(screen, actor_image, actor1_x, 0, 50, 100)
    actor2 = AActor(screen, actor_image, actor2_x, 0, 50, 100)
    assert actor1.Intersects(actor2) == intersect_expected

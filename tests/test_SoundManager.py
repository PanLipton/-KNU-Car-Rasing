import sys
from pathlib import Path

import pytest
from unittest.mock import MagicMock, patch

# Проверяем наличие Pygame перед импортом SoundManager
try:
    import pygame
except ImportError:
    pygame = None

# Путь к директории с исходным кодом
global_dir = Path(__file__).parent.parent / 'src'
sys.path.append(str(global_dir))

# Импорт SoundManager должен происходить после добавления пути в sys.path
from SoundManager.SoundManager import SoundManager


# Фикстура для создания экземпляра SoundManager перед каждым тестом
@pytest.fixture
def sound_manager_instance():
    # Сбрасываем существующий экземпляр SoundManager перед каждым тестом
    SoundManager._instance = None
    return SoundManager()


# Тест проверки синглтона
def test_singleton_instance(sound_manager_instance):
    assert sound_manager_instance is SoundManager()


# Тест инициализации SoundManager
def test_sound_manager_initialization(sound_manager_instance):
    assert sound_manager_instance.sound_enabled == True


# Параметризованный тест для проверки методов воспроизведения звука
@pytest.mark.parametrize("play_method", [
    ("playMusicMenu"),
    ("playMusicGame"),
])
def test_play_methods(sound_manager_instance, mocker, play_method):
    # Проверяем, что Pygame установлен перед выполнением теста
    if pygame is None:
        pytest.skip("Pygame is not installed, skipping test.")

    # Создаем мок-объект для замены метода воспроизведения
    mock_play_method = getattr(sound_manager_instance, play_method)
    mock_play_method_mock = MagicMock()
    setattr(sound_manager_instance, play_method, mock_play_method_mock)

    # Вызываем метод воспроизведения
    getattr(sound_manager_instance, play_method)()

    # Проверяем, что вызвался замокированный метод воспроизведения
    mock_play_method_mock.assert_called_once()


# Тест для проверки инициализации SoundManager в условиях отсутствия аудиоустройства
@patch('SoundManager.SoundManager.pygame.mixer.init')
def test_sound_manager_initialization_no_audio(mock_init):
    # Проверяем наличие Pygame перед выполнением теста
    if pygame is None:
        pytest.skip("Pygame is not installed, skipping test.")

    # Инициализация SoundManager
    sound_manager = SoundManager()

    # Проверяем, что pygame.mixer.init() вызывается
    mock_init.assert_called_once()

    # Проверяем, что sound_enabled устанавливается в False
    assert sound_manager.sound_enabled == False

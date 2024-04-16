import shutil
import struct
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

global_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(global_dir))

# Импортируем SoundManager и создаем фикстуру для использования в тестах
from SoundManager.SoundManager import SoundManager


# Создаем тестовый файл volume_test.bin с заданным значением громкости
def create_test_volume_file(volume, file_path):
    data = struct.pack('f', volume)
    with open(file_path, "wb") as f:
        f.write(data)


# Теперь мы можем использовать эту функцию в наших тестах для создания файла
def test_set_music_volume(sound_manager, monkeypatch, tmp_path):
    # Создаем тестовый файл volume_test.bin во временной директории
    volume_test_file = tmp_path / "volume_test.bin"
    create_test_volume_file(0.5, volume_test_file)

    # Мокаем метод set_volume объектов Sound
    def mock_set_volume(volume):
        sound_manager.music_game.volume = volume
        sound_manager.music_menu.volume = volume

    # Применяем мок
    monkeypatch.setattr(sound_manager.music_game, 'set_volume', mock_set_volume)
    monkeypatch.setattr(sound_manager.music_menu, 'set_volume', mock_set_volume)

    # Загружаем тестовое значение громкости из файла volume_test.bin
    with open(volume_test_file, "rb") as f:
        test_volume = struct.unpack('f', f.read())[0]

    # Применяем тестовое значение громкости
    sound_manager.setMusicVolume(test_volume)

    # Проверяем, сохраняется ли значение громкости в объектах Sound
    assert sound_manager.music_game.volume == test_volume
    assert sound_manager.music_menu.volume == test_volume


@pytest.fixture
def sound_manager(monkeypatch, tmp_path):
    # Получаем путь к файлу volume.bin внутри репозитория
    volume_bin_path = Path(__file__).resolve().parent.parent / "assets" / "bin" / "volume.bin"

    # Мокаем объекты для звуков
    sound_manager = SoundManager()
    sound_manager.music_game = MagicMock()
    sound_manager.music_menu = MagicMock()
    sound_manager.sound_win = MagicMock()
    sound_manager.sound_lose = MagicMock()

    # Создаем тестовый файл volume_test.bin
    volume_test_file = tmp_path / "volume_test.bin"
    create_test_volume_file(0.5, volume_test_file)

    # Переопределяем путь к файлу volume.bin для SoundManager
    sound_manager.volume_bin_path = volume_test_file

    return sound_manager


# Тесты для метода setMusicVolume
def test_set_music_volume(sound_manager, monkeypatch):
    # Мокаем метод set_volume объектов Sound
    def mock_set_volume(volume):
        sound_manager.music_game.volume = volume
        sound_manager.music_menu.volume = volume

    # Применяем мок
    monkeypatch.setattr(sound_manager.music_game, 'set_volume', mock_set_volume)
    monkeypatch.setattr(sound_manager.music_menu, 'set_volume', mock_set_volume)

    sound_manager.setMusicVolume(0.5)

    # Проверяем, сохраняется ли значение громкости в объектах Sound
    assert sound_manager.music_game.volume == 0.5
    assert sound_manager.music_menu.volume == 0.5


# Тесты для метода playSoundWin
def test_play_sound_win(sound_manager, monkeypatch):
    # Применяем мок для метода play объекта Sound
    monkeypatch.setattr(sound_manager.sound_win, 'play', MagicMock())
    sound_manager.playSoundWin()
    # Проверяем, вызывается ли метод проигрывания звука победы
    sound_manager.sound_win.play.assert_called_once()


# Тесты для метода playSoundLose
def test_play_sound_lose(sound_manager, monkeypatch):
    # Применяем мок для метода play объекта Sound
    monkeypatch.setattr(sound_manager.sound_lose, 'play', MagicMock())
    sound_manager.playSoundLose()
    # Проверяем, вызывается ли метод проигрывания звука поражения
    sound_manager.sound_lose.play.assert_called_once()

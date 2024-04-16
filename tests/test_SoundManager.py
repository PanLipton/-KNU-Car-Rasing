import shutil
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

global_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(global_dir))

# Импортируем SoundManager и создаем фикстуру для использования в тестах
from SoundManager.SoundManager import SoundManager

@pytest.fixture
def sound_manager(monkeypatch, tmp_path):
    # Создаем замоканные объекты для тестирования
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()

    # Копируем файл volume.bin из репозитория во временную директорию для тестов
    source_file = Path(__file__).resolve().parent.parent / "assets" / "bin" / "volume.bin"
    shutil.copy(source_file, test_dir)

    sound_manager = SoundManager()
    sound_manager.music_game = MagicMock()
    sound_manager.music_menu = MagicMock()
    sound_manager.sound_win = MagicMock()
    sound_manager.sound_lose = MagicMock()
    return sound_manager

# Тесты для метода setMusicVolume
@pytest.mark.parametrize("volume", [0.0, 0.5, 1.0])
def test_set_music_volume(sound_manager, volume, monkeypatch):
    # Мокаем метод set_volume объектов Sound
    def mock_set_volume(volume):
        sound_manager.music_game.volume = volume
        sound_manager.music_menu.volume = volume
    # Применяем мок
    monkeypatch.setattr(sound_manager.music_game, 'set_volume', mock_set_volume)
    monkeypatch.setattr(sound_manager.music_menu, 'set_volume', mock_set_volume)

    sound_manager.setMusicVolume(volume)
    # Проверяем, сохраняется ли значение громкости в объектах Sound
    assert sound_manager.music_game.volume == volume
    assert sound_manager.music_menu.volume == volume

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

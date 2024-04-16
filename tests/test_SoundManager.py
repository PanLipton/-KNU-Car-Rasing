import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

global_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(global_dir))

# Импортируем SoundManager и создаем фикстуру для использования в тестах
from SoundManager.SoundManager import SoundManager

@pytest.fixture
def sound_manager(monkeypatch):
    sound_manager = SoundManager()
    monkeypatch.setattr(sound_manager, 'sound_enabled', True)  
    sound_manager.music_game = MagicMock()
    sound_manager.music_menu = MagicMock()
    sound_manager.sound_win = MagicMock()
    sound_manager.sound_lose = MagicMock()
    return sound_manager

@pytest.mark.parametrize("volume", [0.0, 0.5, 1.0])
def test_set_music_volume(sound_manager, volume, monkeypatch):
    BASE_DIR = Path(__file__).resolve().parent.parent
    VOLUME_BIN_PATH = BASE_DIR / 'assets' / 'bin' / 'volume.bin'
    assert os.path.exists(VOLUME_BIN_PATH), f"File not found: {VOLUME_BIN_PATH}"

    # Применяем мок метода set_volume объектов Sound
    monkeypatch.setattr(sound_manager.music_game, 'set_volume', MagicMock())
    monkeypatch.setattr(sound_manager.music_menu, 'set_volume', MagicMock())

    sound_manager.setMusicVolume(volume)
    # Проверяем, сохраняется ли значение громкости в объектах Sound
    assert sound_manager.music_game.set_volume.call_count == 1
    assert sound_manager.music_game.set_volume.call_args[0][0] == volume
    assert sound_manager.music_menu.set_volume.call_count == 1
    assert sound_manager.music_menu.set_volume.call_args[0][0] == volume

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

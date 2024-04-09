import sys
from pathlib import Path

import pytest
from unittest.mock import MagicMock

global_dir = Path(__file__).parent.parent / 'src'
sys.path.append(str(global_dir))
from SoundManager.SoundManager import SoundManager 

@pytest.fixture
def sound_manager_instance():

    SoundManager._instance = None
    return SoundManager()

def test_singleton_instance(sound_manager_instance):

    assert sound_manager_instance is SoundManager()

def test_sound_manager_initialization(sound_manager_instance):

    assert sound_manager_instance.sound_enabled == True

@pytest.mark.parametrize("play_method", [
    ("playMusicMenu"),
    ("playMusicGame"),

])
def test_play_methods(sound_manager_instance, mocker, play_method):

    mock_play_method = getattr(sound_manager_instance, play_method)
    mock_play_method_mock = MagicMock()
    setattr(sound_manager_instance, play_method, mock_play_method_mock)

    getattr(sound_manager_instance, play_method)()

    mock_play_method_mock.assert_called_once()

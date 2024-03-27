import pytest
import pygame
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
global_dir = Path(__file__).parent.parent / 'src'
sys.path.append(str(global_dir))
from GameController import GameController

def mock_pygame():
    with patch('pygame.font.Font') as mock_font:
        mock_font.return_value = MagicMock()
        with patch('pygame.init'), \
                patch('pygame.display.set_mode'), \
                patch('pygame.display.set_caption'), \
                patch('pygame_gui.UIManager'), \
                patch('SoundManager.SoundManager.sound_manager.playMusicMenu'), \
                patch('pygame.font.init'), \
                patch('pygame.font.Font'):
            yield

# Тест ініціалізації GameController
def test_game_controller_initialization():
    gc = GameController(debug=True)
    assert gc.debug is True

# Тест основного циклу виконання (run)
def test_game_controller_run():
    with patch('pygame.init'), \
         patch('pygame.display.set_mode') as mock_set_mode, \
         patch('pygame.time.Clock'), \
         patch('pygame.event.get') as mock_get, \
         patch('pygame.display.flip'), \
         patch('pygame.quit'):
        # Налаштування mock об'єкта, щоб повертати коректний розмір вікна
        mock_set_mode.return_value.get_size.return_value = (800, 600)
        mock_get.return_value = [MagicMock(type=pygame.QUIT)]
        gc = GameController()
        gc.run()
        # Перевірити, чи був викликаний pygame.quit()
        pygame.quit.assert_called_once()


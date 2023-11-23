import pygame
import pyautogui
import time

MAX_PHASE: int = 2

class CreePy:
    def __init__(self) -> None:
        pygame.init()
        self._phase: int = 1
        self._phase_duration: int = 10 # seconds
        self._phase_switch_sleep: int = 5 # seconds
        self.__PHASES: dict = {1 : self._phase_one, 2 : self._phase_one}
    
    def _phase_one(self) -> None:
        end_time = time.time() + self._phase_duration
        while time.time() < end_time:
            pyautogui.moveRel(xOffset=10, yOffset=10, duration=0.4)
    
    def _phase_two(self) -> None:
        end_time = time.time() + self._phase_duration
        while time.time() < end_time:
            pass
    
    def next_phase(self) -> None:
        if self._phase < MAX_PHASE:
            self._phase += 1
        time.sleep(self._phase_switch_sleep)
        self.__PHASES[self._phase]()
        
    def __play_music(self, file_path: str) -> None:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    
    def __stop_music(self) -> None:
        pygame.mixer.music.stop()    
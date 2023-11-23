import pyautogui
import time

MAX_PHASE: int = 2

class CreePy:
    def __init__(self) -> None:
        self._phase: int = 1
        self._phase_duration: int = 10 # seconds
        self._phase_switch_sleep: int = 5 # seconds
        self.__PHASES: dict = {1 : self._phase_one, 2 : self._phase_one}
    
    def _phase_one(self) -> None:
        end_time = time.time() + self._phase_duration
        while time.time() < end_time:
            pyautogui.moveRel(xOffset=10, yOffset=10, duration=0.4)
    
    def next_phase(self) -> None:
        if self._phase < MAX_PHASE:
            self._phase += 1
        time.sleep(self._phase_switch_sleep)
        self.__PHASES[self._phase]()
import pygame
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume 
import time

class CreePy:
    def __init__(self) -> None:
        pygame.init()
        self._phase: int = 1
        self._phase_duration: int = 10 # seconds
        self._phase_switch_sleep: int = 5 # seconds
        self._volume_level: float = 0.0
    
    @property
    def __MAX_PHASE(self) -> int:
        return 2
    
    @property
    def __PHASES(self) -> dict:
        return {1 : self._phase_one, 2 : self._phase_two}
    
    @property
    def __MUTE(self) -> int:
        return 1
    
    @property
    def __UNMUTE(self) -> int:
        return 0
    
    def _phase_one(self) -> None:
        end_time = time.time() + self._phase_duration
        while time.time() < end_time:
            pyautogui.moveRel(xOffset=10, yOffset=10, duration=0.4)
    
    def _phase_two(self) -> None:
        end_time = time.time() + self._phase_duration
        self.__play_music(r'./resources/phase_two/mi.mp3')
        while time.time() < end_time:
            pass
        self.__stop_music()
    
    def next_phase(self) -> None:
        if self._phase < self.__MAX_PHASE:
            self._phase += 1
        time.sleep(self._phase_switch_sleep)
        self.__PHASES[self._phase]()
        
    def __play_music(self, file_path: str) -> None:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    
    def __stop_music(self) -> None:
        pygame.mixer.music.stop()    
        
    def __update_volume(self) -> None:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        volume.SetMute(self.__UNMUTE, None)
        
        # the range of the master volume level is 0.0 (0) to 1.0 (100)
        volume.SetMasterVolumeLevelScalar(self._volume_level, None)
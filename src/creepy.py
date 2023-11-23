import pygame
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume 
from PIL import Image, ImageTk
import tkinter as tk
import threading
import time

class CreePy:
    def __init__(self) -> None:
        pygame.init()
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self._volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        self._phase: int = 1
        self._phase_duration: int = 30 # seconds
        self._phase_switch_sleep: int = 2 # seconds
        self._volume_level: float = self._volume.GetMasterVolumeLevelScalar()
        self._volume_switch_sleep: int = 5 # seconds
    
    @property
    def __MAX_PHASE(self) -> int:
        return 3
    
    @property
    def __PHASES(self) -> dict:
        return {1 : self._phase_one, 2 : self._phase_two, 3 : self._phase_three}
    
    @property
    def __MUTE(self) -> int:
        return 1
    
    @property
    def __UNMUTE(self) -> int:
        return 0
    
    @property
    def __MAX_VOLUME_LEVEL(self) -> float:
        return 1.0
    
    @property 
    def __MIN_VOLUME_LEVEL(self) -> float:
        return 0.0
    
    def _phase_one(self) -> None:
        end_time = time.time() + self._phase_duration
        while time.time() < end_time:
            pyautogui.moveRel(xOffset=10, yOffset=10, duration=0.4)
    
    def _phase_two(self) -> None:
        end_time = time.time() + self._phase_duration
        self.__play_music(r'./resources/phase_two/mi.mp3')
        while time.time() < end_time:
            self.__increase_volume(0.01)
            time.sleep(self._volume_switch_sleep)
            self.__update_volume()
        self.__stop_music()
    
    def _phase_three(self) -> None:
        end_time = time.time() + self._phase_duration
           
        process = threading.Thread(target=self.__stuck_image, args=(r'./resources/phase_three/pi.png',))
        process.start()
        
        while time.time() < end_time:
            pass
    
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
        self._volume.SetMute(self.__UNMUTE, None)
        
        # the range of the master volume level is 0.0 (0) to 1.0 (100)
        self._volume.SetMasterVolumeLevelScalar(self._volume_level, None)
    
    def __increase_volume(self, inc_value: float) -> None:
        if self._volume_level + inc_value <= self.__MAX_VOLUME_LEVEL:
            self._volume_level += inc_value
            
    def __decrease_volume(self, dec_value: float) -> None:
        if self._volume_level - dec_value >= self.__MIN_VOLUME_LEVEL:
            self._volume_level -= dec_value
            
    def __stuck_image(self, image_path: str) -> None:
        image = Image.open(image_path)
        root = tk.Tk()
        root.attributes("-topmost", True) 
        root.attributes('-fullscreen', True)
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        image = image.resize((screen_width, screen_height))
        
        tk_image = ImageTk.PhotoImage(image)
        
        label = tk.Label(root, image=tk_image)
        label.pack(fill=tk.BOTH, expand=tk.YES)
        
        root.mainloop()        
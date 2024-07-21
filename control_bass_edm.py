import time,random
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def set_volume(left_volume, right_volume):
    while True:
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            current_volume_left, current_volume_right, _ = volume.GetVolumeRange()
            volume.SetChannelVolumeLevelScalar(0, left_volume, None)  # Left channel
            volume.SetChannelVolumeLevelScalar(1, right_volume, None)  # Right channel
            break
        except:
            None
def increase_volume(min_volume,max_volume):
    if min_volume > max_volume:
        max_volume=max_volume-2
        for i in range (max_volume ,min_volume):
            volume = (min_volume-i+max_volume)/100
            while True:
                try:
                    set_volume(volume, volume)
                    time.sleep(0.1)
                    break
                except Exception as e:
                    None
        return volume
    elif min_volume==max_volume:
        volume=max_volume
        return volume        
    else:
        for i in range(min_volume, max_volume):
            volume = i / 100
            while True:
                try:
                    set_volume(volume, volume)
                    time.sleep(0.1)  # Adjust sleep time as needed
                    break
                except Exception as e:
                    None
        return volume    
def oscillate_volume():
    global volume
    count = 1 / 100
    volume_left = volume
    volume_right = volume

    for i in range (random.randint(1000,5000)):
        if volume_left <= 0.2 or volume_right <=0.2:
            count = -count
        volume_right += count
        volume_left -= count
        if volume_left >=0.9: 
            volume_left=0.9
        if volume_right >=0.9:
            volume_right=0.9
        while True:    
            try:
                set_volume(volume_left, volume_right)
                time.sleep(0.1)
                break
            except Exception as e:
                None
      
def random_volume_change():
    global left_volume,right_volume
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume_left, current_volume_right, _ = volume.GetVolumeRange()

        for _ in range(15):  # Change volume randomly 10 times
            left_volume = (random.randint(25, 65))/100
            right_volume = (random.randint(25, 65))/100
            while True:
                try:
                    set_volume(left_volume, right_volume)# Random volume level between 10% and 100%
                    break
                except:
                    None
            time.sleep(0.3)       
    except Exception as e:
        None
def compair_argument():
    global left_volume,right_volume,volume
    equa=int((((left_volume+right_volume)*100))/2)
    if left_volume >= right_volume:
        for i in range (0,int((equa-int(right_volume*100))/1)+1):
            while True:
                try:                    
                    set_volume(right_volume+i/100,left_volume-i/100)
                    time.sleep(0.1)
                    break
                except:
                    None
        increase_volume(equa,56)           
    else:
        for i in range (0,int((equa-int(left_volume*100))/1)+1):
            while True:
                try:
                    set_volume(right_volume-i/100,left_volume+i/100)
                    time.sleep(0.1)
                    break
                except:
                    None
        increase_volume(equa,56)
    volume=55/100
while True:    
    volume=increase_volume(10,51)
    random_volume_change()
    compair_argument()
    while True:
        time_follow=random.randint(50,250)
        time.sleep(time_follow)
        increase_volume(int(volume*100),55)
        oscillate_volume()
        compair_argument()

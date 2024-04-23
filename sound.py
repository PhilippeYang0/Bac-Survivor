from pygame import mixer

mixer.init(channels = 8)
bgm_channel = mixer.Channel(0)

def sound_effect(file_path:str,volume:float):
    """
    Renvoie le son du fichier
    Le volume du son est modifiable, 0.0 < volume < 1.0
    """
    se = mixer.Sound(file_path)
    se.set_volume(volume)
    se.play()

def sound_effect_without_file(sound:mixer.Sound,volume:float):
    """
    Joue le son contenu dans sound à un volume de valeur volume compris entre 0.0 et 1.0.
    """
    sound.set_volume(volume)
    sound.play()

def sound_background(file_path:str,volume:float):
    """
    Renvoie le son du fichier
    Le volume du son est modifiable, 0.0 < volume < 1.0
    """
    bgm = mixer.Sound(file_path)
    bgm.set_volume(volume)
    bgm_channel.set_volume(volume)
    bgm_channel.play(bgm,-1)
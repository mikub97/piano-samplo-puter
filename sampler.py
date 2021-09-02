#!/usr/bin/env python
import argparse
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from scipy.io import wavfile
import pygame
import sound_stretcher as ss


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", action='store_true',
                        help='flag if to use pianoputer')
    parser.add_argument("-r", action='store_true',
                        help='flag if to run audacity')
    parser.add_argument(
        '--wav', '-w',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='bowl.wav',
        help='WAV file (default: bowl.wav)')
    parser.add_argument(
        '--keyboard', '-k',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='keyboard',
        help='keyboard file (default: keyboard)')
    return (parser.parse_args(), parser)




def mpc_key_sound_default() :
    key_to_file = {
        'a': 'samples/fav/kick1.ogg',
        's': 'samples/fav/kick2.ogg',
        'd': 'samples/fav/perc1.ogg',
        'f': 'samples/fav/perc2.ogg',
        'g': 'samples/fav/hithat1.ogg',
        'h': 'samples/fav/hithat2.ogg',
        'j': 'samples/fav/snare1.ogg',
        'k': 'samples/fav/snare2.ogg',
    }

    key_to_sound = {}
    for key, file in key_to_file.items():
        key_to_sound[key] = pygame.mixer.Sound(file=file)

    return key_to_sound

def change_key_sound(keys,key_to_sound) :
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               print('Escape')
               return key_to_sound
            if pygame.key.name(event.key) in keys:
               Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
               filename = askopenfilename()
               if type(filename)==tuple :
                   print('esc')
                   return key_to_sound# show an "Open" dialog box and return the path to the selected file
               print(pygame.key.name(event.key) + '-->' + filename)
               if filename.split('.')[1] == 'ogg':
                    key_to_sound.update({pygame.key.name(event.key): pygame.mixer.Sound(file=filename)})
               elif filename.split('.')[1] == 'wav':
                    fps, sound = wavfile.read(filename)
                    key_to_sound.update({pygame.key.name(event.key):  pygame.sndarray.make_sound(sound)})
               return key_to_sound

def make_sound_wav(file):
    fps, sound = wavfile.read(file)
    return pygame.sndarray.make_sound(sound)


def main():

    # Parse command line arguments
    (args, parser) = parse_arguments()
    fps = 44100  #default value

    if args.p is True:
        fps, sound = wavfile.read(args.wav.name)
        pygame.mixer.init(fps, -16, 1, 2048)
        tones = range(-25, 25)
        sys.stdout.write('Transponding sound file... ')
        sys.stdout.flush()
        transposed_sounds = [ss.pitchshift(sound, n) for n in tones]
        print('DONE')
        keys = args.keyboard.read().split('\n')
        sounds = map(pygame.sndarray.make_sound, transposed_sounds)
        key_sound = dict(zip(keys, sounds))
        is_playing = {k: False for k in keys}

    else:
        pygame.mixer.init(fps, -16, 1, 2048)
        keys = args.keyboard.read().split('\n')
        key_sound = mpc_key_sound_default()
        is_playing =  {k: False for k in keys}
        time_playing =  {k: 0 for k in keys}
    if args.r is True:
        import os
        os.system("audacity&")
    screen = pygame.display.set_mode((500, 150))
    while True:
        event = pygame.event.wait()

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:
            if (key in key_sound.keys()) and (not is_playing[key]):
                key_sound[key].play(fade_ms=50)
                is_playing[key] = True
                # if recorder.is_rec:
                #     # recorder.play(key_sound[key])
                #     time_playing[key] = time.time()


            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise KeyboardInterrupt

            elif event.key == pygame.K_LALT:
                print('Changing key sound')
                s = change_key_sound(keys,key_sound)

            elif event.key == pygame.K_RETURN:
                print('enter')
                # recorder.record()

        elif event.type == pygame.KEYUP and key in key_sound.keys():
            # Stops with 50ms fadeout
            key_sound[key].fadeout(50)
            is_playing[key] = False
            # if recorder.is_rec:
            #     recorder.play(key_sound[key],time.time()-time_playing[key])
            #     time_playing[key] = 0


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')

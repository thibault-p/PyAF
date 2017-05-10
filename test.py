import logging

from emulators.advmame_emulator import AdvmameEmulator

logging.basicConfig(level=logging.INFO)

emu = AdvmameEmulator('advmame', '/tmp')


emu.scanForRoms()

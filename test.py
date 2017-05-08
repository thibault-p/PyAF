import logging

from emulators.advmame_emulator import AdvmameEmulator

logging.basicConfig(level=logging.INFO)

emu = AdvmameEmulator('/tmp/adv', '/tmp')


emu.scanForRoms()

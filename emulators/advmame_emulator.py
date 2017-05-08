import logging
from generic_emulator import GenericEmulator



class AdvmameEmulator(GenericEmulator):

    def __init__(self, execPath, romsPath):
        super(AdvmameEmulator, self).__init__(execPath, romsPath)


    def checkRomValidity(self, romPath):
        logger = logging.getLogger('pyaf')
        logger.info('Check validity of rom: %s', romPath)

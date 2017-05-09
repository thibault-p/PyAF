import logging
from os.path import join
from generic_emulator import GenericEmulator



class AdvmameEmulator(GenericEmulator):
    commands = {
        'generate_roms_file': '',
        'run_rom': ''
    }

    def __init__(self, execPath, romsPath):
        super(AdvmameEmulator, self).__init__(execPath, romsPath)

    def generateSupportedRomFile(self):
        logger = logging.getLogger('pyaf')
        logger.info('Generate file of supported roms list')

    def checkRomValidity(self, romPath):
        logger = logging.getLogger('pyaf')
        logger.info('Check validity of rom: %s', romPath)
        super(AdvmameEmulator, self).extractDataFromZipFile(join(self.romsPath, romPath))

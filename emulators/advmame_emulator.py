import logging
import subprocess
from  xml.etree import cElementTree

from os.path import join
from tempfile import gettempdir
from generic_emulator import GenericEmulator



class AdvmameEmulator(GenericEmulator):
    commands = {
        'generate_roms_file': ['--listxml'],
        'run_rom': ''
    }

    default_tmp_roms_list = '/tmp/out.xml'

    def __init__(self, execPath, romsPath):
        super(AdvmameEmulator, self).__init__(execPath, romsPath)

    def buildCommand(self, cmdName):
        if not cmdName in AdvmameEmulator.commands:
            return None
        cmd = [self.execPath] + AdvmameEmulator.commands[cmdName][:]
        return ' '.join(str(e) for e in cmd)


    def generateSupportedRomsFile(self):
        logger = logging.getLogger('pyaf')
        tmp = join(gettempdir(), '.advmame_roms.xml')
        logger.info('Generate file of supported roms list in: %s', tmp)
        cmd = self.buildCommand('generate_roms_file')
        logger.info('Run command: %s', cmd)
        with open(AdvmameEmulator.default_tmp_roms_list, 'w') as xml:
            p = subprocess.Popen(cmd, shell=True, stdout=xml)
            ret_code = p.wait()
            xml.flush()

        self.getRomData('toto')

    def checkRomValidity(self, romPath):
        logger = logging.getLogger('pyaf')
        logger.info('Check validity of rom: %s', romPath)
        super(AdvmameEmulator, self).extractDataFromZipFile(
            join(self.romsPath, romPath))


    def getRomData(self, romName):
        logger = logging.getLogger('pyaf')
        logger.info('Check validity of rom: %s', romName)
        with open(AdvmameEmulator.default_tmp_roms_list, 'r') as file:
            for event, elem in cElementTree.iterparse(file):
                if elem.tag == 'game':
                    logger.info('Found a game: %s', elem.itertext())
                    elem.clear()

import logging
import subprocess
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

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

    def supportedRomsiterator(self):
        logger = logging.getLogger('pyaf')
        with open(AdvmameEmulator.default_tmp_roms_list, 'r') as file:
            for event, elem in ET.iterparse(file):
                if elem.tag == 'game':
                    game = self.parseGame(elem)
                    yield game
                    elem.clear()


    def parseGame(self, gameNode):
        logger = logging.getLogger('pyaf')
        attribs = gameNode.attrib
        game = {'roms': {}}
        if not 'runnable' in attribs or attribs['runnable'] == 'no':
            #Not a game, bios or something
            return None
        game['name'] = attribs['name']
        for child in gameNode:
            if child.tag == 'rom':
                if not 'name' in child.attrib or not 'crc' in child.attrib:
                    return None
                game['roms'][child.attrib['name']] = child.attrib['crc']
            if child.tag == 'video':
                game['video'] = child.attrib
        return game

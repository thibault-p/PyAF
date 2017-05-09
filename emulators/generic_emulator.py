import logging
import zipfile
from os import listdir
from os.path import isfile, join, splitext

class GenericEmulator(object):

    def __init__(self, execPath, romsPath):
        self.romsPath = romsPath
        self.execPath = execPath

    def scanForRoms(self):
        logger = logging.getLogger('pyaf')
        logger.info('Retrieve list of roms contained in: %s', self.romsPath)
        files = [f for f in listdir(self.romsPath) if isfile(join(self.romsPath, f))]
        logger.info('Found %d files.', len(files))
        for f in files:
            filename, fileExt = splitext(f)
            if fileExt == '.zip':
                self.checkRomValidity(f)

    def checkRomValidity(self, romPath):
        raise NotImplementedError

    def extractDataFromZipFile(self, zipFilePath):
        logger = logging.getLogger('pyaf')
        data = []
        logger.info('Files in: %s', zipFilePath)
        with zipfile.ZipFile(zipFilePath, 'r') as romZip:
            infos = romZip.infolist()
            for info in infos:
                logger.info('Filename: %s  CRC: %s', info.filename, info.CRC)
                data.append({'filename': info.filename, 'crc': info.CRC})
        return data

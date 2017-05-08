import logging
from os import listdir
from os.path import isfile, join

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
            self.checkRomValidity(f)

    def checkRomValidity(self, romPath):
        raise NotImplementedError




    def extractDataFromZipFile(self, zipFilePath):
        

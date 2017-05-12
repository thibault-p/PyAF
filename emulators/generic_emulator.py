import logging
import zipfile

from os import listdir
from os.path import isfile, join, splitext

class GenericEmulator(object):

    def __init__(self, execPath, romsPath):
        self.romsPath = romsPath
        self.execPath = execPath

    def scanForRoms(self, folder= None):
        logger = logging.getLogger('pyaf')
        # Generates the file needed to compare roms
        self.generateSupportedRomsFile()

        validRoms = []
        unvalidRoms = []

        if not folder:
            folder = self.romsPath
        logger.info('Retrieve list of roms contained in: %s', folder)
        files = [f for f in sorted(listdir(self.romsPath)) if isfile(join(folder, f))]
        logger.info('Found %d files.', len(files))
        romsToScan = []
        for f in files:
            filename, fileExt = splitext(f)
            if fileExt == '.zip':
                romsToScan.append(filename)

        # iterate over supported rom
        iterator = self.supportedRomsiterator()
        for r in iterator:
            if not r:
                continue
            if r['name'] in romsToScan:
                errors = self.checkRomValidity(join(folder, r['name'] + '.zip'), r)



    def generateSupportedRomsFile(self):
        raise NotImplementedError

    def supportedRomsiterator(self):
        raise NotImplementedError


    def checkRomValidity(self, romPath, baseRom):
        logger = logging.getLogger('pyaf')
        logger.info('Checking rom validity %s', romPath)
        romsToCheck = self.extractDataFromZipFile(romPath)
        errors = []
        for rom in baseRom['roms']:
            if not rom in romsToCheck:
                logger.info('File %s is missing', rom)
                errors.append(rom + ' is missing.')
                continue
            crc1 = baseRom['roms'][rom]
            crc2 = romsToCheck[rom]
            if crc1 != crc2:
                logger.info('File %s not valid, crc mismatch (got %s expect %s)', rom, crc1, crc2)
                errors.append(rom + 'is not valid. Bad CRC.')
        return errors



    def extractDataFromZipFile(self, zipFilePath):
        logger = logging.getLogger('pyaf')
        data = {}
        with zipfile.ZipFile(zipFilePath, 'r') as romZip:
            infos = romZip.infolist()
            for info in infos:
                data[info.filename] = format(info.CRC, '08x')
        return data

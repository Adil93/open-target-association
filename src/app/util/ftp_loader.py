from ftplib import FTP
from os.path import dirname
import logging as logger
import pandas as pd


class FtpLoader:

    def __init__(self, host, destinationBaseDir='data/'):
        self.host = host
        self.destinationBaseDir = destinationBaseDir

    def loadData(self, dataDirectory, destinationDirectory):

        try:
            ftp = FTP(self.host)
            ftp.login()
            logger.info(
                "Loading data in {0} --> {1}".format(dataDirectory, destinationDirectory))

            wholeData = pd.DataFrame()
            ftp.cwd(dataDirectory)
            files = ftp.nlst()

            for fileName in files:
                if not fileName.__contains__("json"):
                    continue
                logger.info("Downloading {0}".format(fileName))
                ftp.retrbinary("RETR %s" %
                               fileName, open(fileName, 'wb').write)
                dataStr = open(fileName, "r").read()
                try:
                    data = pd.read_json(dataStr, lines=True)

                    wholeData = data if wholeData.empty else wholeData.append(
                        data, sort=False)
                except ValueError:
                    logger.info("{0} - wrong json".format(fileName))
            ftp.close()
            return wholeData
        except ValueError:
            logger.info("Error Occured!!")
        finally:
            ftp.close()

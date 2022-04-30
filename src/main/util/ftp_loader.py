import os
import sys
from ftplib import FTP
from os.path import dirname

import pandas as pd

sys.path.append(dirname(__file__))


class FtpLoader:

    def __init__(self, host, destinationBaseDir='data/'):
        self.host = host
        self.destinationBaseDir = destinationBaseDir

    def loadData(self, dataDirectory, destinationDirectory):

        try:
            ftp = FTP(self.host)
            ftp.login()
            print(
                "Loading data in {0} --> {1}".format(dataDirectory, destinationDirectory))

            wholeData = pd.DataFrame()
            ftp.cwd(dataDirectory)
            files = ftp.nlst()
            os.chdir(self.destinationBaseDir)
            if not os.path.isdir(destinationDirectory):
                os.mkdir(destinationDirectory)
            os.chdir(destinationDirectory)

            for fileName in files:
                if not fileName.__contains__("json"):
                    continue
                print("Downloading {0}".format(fileName))
                ftp.retrbinary("RETR %s" %
                               fileName, open(fileName, 'wb').write)
                dataStr = open(fileName, "r").read()
                try:
                    data = pd.read_json(dataStr, lines=True)

                    wholeData = data if wholeData.empty else wholeData.append(
                        data, sort=False)
                except ValueError:
                    print("{0} - wrong json".format(fileName))
            os.chdir("../../")
            ftp.close()
            return wholeData
        except ValueError:
            print("Error Occured!!")
        finally:
            ftp.close()

#! /usr/bin/python3
import logging
import config
import urllib.request

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.loggingPath,
                    level=logging.INFO
                    )

def getPublicIP(url):
    try:
        return str(urllib.request.urlopen(url).read().decode('utf-8'))
    except Exception as err:
        logging.error(err)
        return None

def updateZones(path, identifyer, ip):
    try:
        zonesFile = open(path, 'r+')
        lines = zonesFile.readlines()
        zonesFile.seek(0)
        newLines = []
        updated = False

        for n, line in enumerate(lines):
            record = line.split()
            if len(record) == 5 and record[-1] == identifyer and record[-2] != ip:
                updated = True
                logging.info('Updated line %i: %s -> %s' % (n, record[-2], ip))
                record[-2] = ip
        
            newLines.append(" ".join(record))
        if updated:
            zonesFile.write("\n".join(newLines))
            zonesFile.truncate()
        zonesFile.close()
    except Exception as err:
        logging.error(err)

if __name__ == '__main__':
    ip = getPublicIP(config.ipCheckUrl)
    if ip != None:
        updateZones(config.zone['path'], config.zone['identifyer'], ip)

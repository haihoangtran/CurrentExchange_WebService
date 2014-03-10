import urllib
import urllib2

class CurrencyExchange(): 
    def __init__(self):
        self.ADJUSTED_RATIO = 0.98
        self.vendorList = []
    
    def getRateFromWeb(self, vendorName, currencyName):
        url = "https://agile.cs.uh.edu/rate?cur="+currencyName+"&vendor="+vendorName
        try:
            connection = urllib.urlopen(url)
            try:
                return float(connection.read())
            except ValueError:
                return 0.00
        except IOError:
            return 0.00
    
    def addVendor(self,vendorList):
        for vendor in vendorList:
            if vendor not in self.vendorList and len(vendor)>0:
                self.vendorList.append (vendor)

    def adjustRate(self, rate):
        return rate*self.ADJUSTED_RATIO
    
    def getExchangeRate (self, currencyName):
        rate = 0.0
        vendorName = ""
        for i in range (len(self.vendorList)):
            try:
                tempRate = self.getRateFromWeb(self.vendorList[i], currencyName)
            except IOError:
                continue
            if rate < tempRate:
                rate = tempRate
                vendorName = self.vendorList[i]
        return [vendorName, self.adjustRate(rate)]

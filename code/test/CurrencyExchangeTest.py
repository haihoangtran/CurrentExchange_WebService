import unittest
from CurrencyExchange import *
from mock import MagicMock
import urllib
import urllib2

class CurrencyExchangeTest(unittest.TestCase):
    def setUp(self):
        self.currencyExchange = CurrencyExchange()
        
    def test_canary(self):
        self.assertTrue(True)
        
    def test_get_currency_rate_from_0_vendor(self):
        self.assertEquals(["", 0.0], self.currencyExchange.getExchangeRate('GBP'))
    
    def test_adjust_rate(self):
        self.assertEquals(98, self.currencyExchange.adjustRate(100))
    
    def test_get_max_currency_rate_from_invalid_vendor_name(self):
        self.currencyExchange.addVendor([""])
        self.assertEquals(['', 0.0], self.currencyExchange.getExchangeRate("GBP"))
        
    def test_get_currency_rate_from_1_vendor(self):
        self.currencyExchange.addVendor(["v1"]);
        self.currencyExchange.getRateFromWeb = MagicMock(return_value = 100.00)
        self.assertEquals(["v1", 98.00], self.currencyExchange.getExchangeRate('GBP'))

    def test_get_max_currency_rate_from_2_same_vendors(self):
        self.currencyExchange.addVendor(["v1", "v1"])
        self.currencyExchange.getRateFromWeb = MagicMock()
        self.currencyExchange.getRateFromWeb.side_effect = [80.00, 90.00]
        self.assertEquals(["v1", 78.4],self.currencyExchange.getExchangeRate('GBP'))
    
    def test_get_max_currency_rate_from_2_different_vendors(self):
        vendor = {"v1" : 60.00, "v2": 100.00}
        self.currencyExchange.addVendor(["v1", "v2"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"]])
        self.assertEquals(["v2", 98],self.currencyExchange.getExchangeRate('GBP'))
    
    def test_get_max_currency_rate_if_price_of_vendor1_is_greater_than_vendor2(self):
        vendor = {"v1" : 100.00, "v2": 90.00}
        self.currencyExchange.addVendor(["v1", "v2"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"]])
        self.assertEquals(["v1", 98], self.currencyExchange.getExchangeRate('GBP'))
    
    def test_get_max_currency_rate_if_rate_of_vendor1_is_equal_to_vendor2(self):
        vendor = {"v1" : 100.00, "v2": 100.00}
        self.currencyExchange.addVendor(["v1", "v2"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"]])
        self.assertEquals(["v1", 98], self.currencyExchange.getExchangeRate('GBP'))
        
    def test_get_max_currency_rate_if_rate_of_vendor1_is_less_than_vendor2(self):
        vendor = {"v1" : 50.00, "v2": 90.00}
        self.currencyExchange.addVendor(["v1", "v2"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"]])
        self.assertEquals(["v2", 88.2], self.currencyExchange.getExchangeRate('GBP'))
   
    def test_get_max_currency_rate_from_3_vendors_when_vendor1_is_max(self):
        vendor = {"v1" : 100.00, "v2": 80.00, "v3": 90.00}
        self.currencyExchange.addVendor(["v1" ,"v2", "v3"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"], vendor["v3"]])
        self.assertEquals(["v1", 98], self.currencyExchange.getExchangeRate('GBP'))
        
    def test_get_max_currency_rate_from_3_vendors_when_vendor2_is_max(self):
        vendor = {"v1" : 80.00, "v2": 100.00, "v3": 90.00}
        self.currencyExchange.addVendor(["v1" ,"v2", "v3"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"], vendor["v3"]])
        self.assertEquals(["v2", 98], self.currencyExchange.getExchangeRate('GBP'))        
     
    def test_get_max_currency_rate_from_3_vendors_when_vendor3_is_max(self):
        vendor = {"v1" : 80.00, "v2": 90.00, "v3": 100.00}
        self.currencyExchange.addVendor(["v1" ,"v2", "v3"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"], vendor["v3"]])
        self.assertEquals(["v3", 98], self.currencyExchange.getExchangeRate('GBP'))
    
    def test_get_max_currency_rate_from_3_vendors_when_vendor2_and_vendor3_are_max(self):
        vendor = {"v1" : 80.00, "v2": 100.00, "v3": 100.00}
        self.currencyExchange.addVendor(["v1" ,"v2", "v3"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"], vendor["v3"]])
        self.assertEquals(["v2", 98], self.currencyExchange.getExchangeRate('GBP'))
    
    def test_get_max_currency_rate_from_3_vendors_when_3_vendors_are_max(self):
        vendor = {"v1" : 100.00, "v2": 100.00, "v3": 100.00}
        self.currencyExchange.addVendor(["v1" ,"v2", "v3"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"], vendor["v3"]])
        self.assertEquals(["v1", 98], self.currencyExchange.getExchangeRate('GBP'))
    
    def test_get_max_currency_rate_from_1_vendor_giving_invalid_rate(self):
        vendor = {"v1" : -80.00}
        self.currencyExchange.addVendor(["v1"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"]])
        self.assertEquals(["", 0.0], self.currencyExchange.getExchangeRate('GBP'))
    
    def test_get_max_currency_rate_from_vendors_giving_invalid_rates(self):
        vendor = {"v1" : -80.00, "v2": 0.0}
        self.currencyExchange.addVendor(["v1", "v2"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"]])
        self.assertEquals(["", 0.0], self.currencyExchange.getExchangeRate('GBP'))
        
    def test_get_max_currency_rate_from_2_vendors_giving_invalid_rates_and_1_vendor_giving_valid_rate(self):
        vendor = {"v1" : -80.00, "v2": 0.0, "v3": 100.0}
        self.currencyExchange.addVendor(["v1", "v2", "v3"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"], vendor["v3"]])
        self.assertEquals(["v3", 98.0], self.currencyExchange.getExchangeRate('GBP'))
        
    def test_get_max_currency_rate_from_1_vendor_giving_invalid_rates_and_2_vendors_giving_valid_rate(self):
        vendor = {"v1" : -80.00, "v2": 100.0, "v3": 80.0}
        self.currencyExchange.addVendor(["v1", "v2", "v3"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"], vendor["v3"]])
        self.assertEquals(["v2", 98.0], self.currencyExchange.getExchangeRate('GBP'))
    
    def test_get_max_currency_rate_from_1_vendor_when_web_service_fails(self):
        self.currencyExchange.addVendor(["v1"])
        self.currencyExchange.getRateFromWeb = MagicMock( side_effect = IOError())
        self.assertEquals(['', 0.0], self.currencyExchange.getExchangeRate('GBP'))
        
    def test_get_max_currency_rate_from_2_vendors_when_web_service_of_vendor1_fails(self):
        vendor = {"v1" : IOError(), "v2": 100.00}
        self.currencyExchange.addVendor(["v1", "v2"])
        self.currencyExchange.getRateFromWeb = MagicMock( side_effect = [vendor["v1"], vendor["v2"]] )
        self.assertEquals(["v2" , 98], self.currencyExchange.getExchangeRate('GBP'))
        
    def test_get_max_currency_rate_from_3_vendors_when_web_service_of_vendor1_fails(self):
        vendor = {"v1" : IOError(), "v2": 90.00, "v3": 100.00}
        self.currencyExchange.addVendor(["v1" ,"v2", "v3"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"], vendor["v3"]])
        self.assertEquals(["v3", 98], self.currencyExchange.getExchangeRate('GBP'))
    
    def test_get_max_currency_rate_from_3_vendors_when_web_service_of_all_vendors_fail(self):
        vendor = {"v1" : IOError(), "v2": IOError(), "v3": IOError()}
        self.currencyExchange.addVendor(["v1" ,"v2", "v3"])
        self.currencyExchange.getRateFromWeb = MagicMock(side_effect = [vendor["v1"], vendor["v2"], vendor["v3"]])
        self.assertEquals(["", 0.0], self.currencyExchange.getExchangeRate('GBP'))
    
    def test_get_max_curency_rate_from_1_vendor_from_the_actual_web_service(self):
        self.currencyExchange.addVendor(["v1"])
        vendor = self.currencyExchange.getExchangeRate("GBP")
        self.assertTrue((vendor[0] == "" or vendor[0] in self.currencyExchange.vendorList) and vendor[1] >= 0)
        
    def test_get_max_curency_rate_from_2_vendors_from_the_actual_web_service(self):
        self.currencyExchange.addVendor(["v1", "v2"])
        vendor = self.currencyExchange.getExchangeRate("GBP")
        self.assertTrue((vendor[0] == "" or vendor[0] in self.currencyExchange.vendorList) and vendor[1] >= 0)

    def test_get_max_curency_rate_from_3_vendors_from_the_actual_web_service(self):
        self.currencyExchange.addVendor(["v1", "v2", "v3"])
        vendor = self.currencyExchange.getExchangeRate("GBP")
        self.assertTrue((vendor[0] == "" or vendor[0] in self.currencyExchange.vendorList) and vendor[1] >= 0)    
    
    def test_get_rate_from_web_when_server_is_down(self):
        urllib.urlopen = MagicMock(side_effect = IOError())
        self.assertEquals(0.0, self.currencyExchange.getRateFromWeb("v1", "GBP"))
    
if __name__ == '__main__':
    unittest.main()
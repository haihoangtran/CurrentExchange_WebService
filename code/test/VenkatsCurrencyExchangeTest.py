import unittest
from CurrencyExchange import *


class VenkatsCurrencyExchangeTest(unittest.TestCase):

    def test_adjusted_high_rate_no_vendors(self):
      self.assert_vendor_and_rate("", 0.0, self.adjusted_high_rate([]))

    def test_adjusted_high_rate_with_one_vendor(self):
      self.assert_vendor_and_rate("GamaInternational", 2.94,
        self.adjusted_high_rate(["GamaInternational"]))

    def test_adjusted_high_rate_with_two_vendors(self):
      self.assert_vendor_and_rate("BetaInternational", 3.92,
        self.adjusted_high_rate(["GamaInternational", "BetaInternational"]))

  
    def test_adjusted_high_rate_with_three_vendors(self):
      self.assert_vendor_and_rate("AlphaInternational", 4.90,
        self.adjusted_high_rate(
          ["GamaInternational", "AlphaInternational", "BetaInternational"]))

    def test_adjusted_high_rate_with_four_vendors(self):
      self.assert_vendor_and_rate("AlphaInternational", 4.90,
        self.adjusted_high_rate(["GamaInternational", "AlphaInternational", 
          "BetaInternational", "MinusInternational"]))

    def test_adjusted_high_rate_with_five_vendors(self):
      self.assert_vendor_and_rate("AlphaInternational", 4.90,
        self.adjusted_high_rate(["GamaInternational", "AlphaInternational",
          "BetaInternational", "MinusInternational", "ErrInternational"]))

    def test_adjusted_high_rate_with_six_vendors(self):
      self.assert_vendor_and_rate("AlphaInternational", 4.90,
        self.adjusted_high_rate(["GamaInternational", "AlphaInternational", 
        "BetaInternational", "MinusInternational", 
        "ErrInternational", "FiveInternational"]))

    def test_adjusted_high_rate_duplicate_vendor(self):
      self.assert_vendor_and_rate("AlphaInternational", 4.90,
        self.adjusted_high_rate(["AlphaInternational", "AlphaInternational", 
          "BetaInternational"]))

    def test_adjusted_high_rate_duplicate_vendor_non_high(self):
      self.assert_vendor_and_rate("AlphaInternational", 4.90,
        self.adjusted_high_rate(["AlphaInternational", "BetaInternational", 
          "BetaInternational"]))

    def test_adjusted_high_rate_withFiveInternational(self):
      self.assert_vendor_and_rate("", 0.0,
        self.adjusted_high_rate(["FiveInternational"]))


    ###########################################################
    #Mapping of tests to code written by individual pairs

    def adjusted_high_rate(self, vendorNames):
      currencyExchange = CurrencyExchange()
      currencyExchange.addVendor(vendorNames)
      return currencyExchange.getExchangeRate("GBP")

    def assert_vendor_and_rate(self, vendorName, rate, result):
      assert vendorName == result[0]
      assert rate == result[1]

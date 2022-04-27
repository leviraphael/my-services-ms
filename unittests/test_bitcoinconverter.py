import unittest


from bicointer_converter import BitcoinConverter,Currency


class TestBitcoinConverter(unittest.TestCase):

    _bc_converter = BitcoinConverter()

    # API is working correctly no exception raise
    def test_result_from_convert(self):
        res = TestBitcoinConverter._bc_converter.convert(Currency.USD)
        self.assertEqual(type(res), int)

    # Converter rate is called with the correct currency
    def test_result_from_convert_different_currency(self):
        res_usd = TestBitcoinConverter._bc_converter.convert(Currency.USD)
        res_eur = TestBitcoinConverter._bc_converter.convert(Currency.EUR)
        self.assertNotEqual(res_usd, res_eur)

    # Convert to USD - no Currency error
    def test_convert_to_usd(self):
        res_usd = TestBitcoinConverter._bc_converter.convert(Currency.USD)
        res = TestBitcoinConverter._bc_converter.convert_to_usd()
        # Almost equal in case there is a different convert rate between the 2 calls
        self.assertAlmostEqual(res, res_usd,places=-2)

    # TODO add more tests here

if __name__ == '__main__':
    unittest.main()

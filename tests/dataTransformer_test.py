import unittest
from dataTransformer import allByUserTransform, netMerchantTransform


class TestDataTransformerFunctions(unittest.TestCase):

    def test_allByUserTransform(self):
        # Test case with multiple transaction records
        res = [
            (1, 1000, '2023-06-01 10:00:00', 123),
            (1, 2000, '2023-06-02 10:00:00', 456),
            (1, 3000, '2023-06-03 10:00:00', 789)
        ]
        expected_json = '[{"user_id":1,"datetime":"2023-06-01 10:00:00","merchant_type_code":123,' \
                        '"amount_in_dollars":10.0},' \
                        '{"user_id":1,"datetime":"2023-06-02 10:00:00","merchant_type_code":456,' \
                        '"amount_in_dollars":20.0},' \
                        '{"user_id":1,"datetime":"2023-06-03 10:00:00","merchant_type_code":789,' \
                        '"amount_in_dollars":30.0}]'
        result = allByUserTransform(res)
        self.assertEqual(result, expected_json)

        # Test case with empty transaction records
        res = []
        expected_json = '[]'
        result = allByUserTransform(res)
        self.assertEqual(result, expected_json)

    def test_allByUserTransform_Empty(self):
        # Test case with multiple transaction records
        res = []
        expected_json = '[]'
        result = allByUserTransform(res)
        self.assertEqual(result, expected_json)

        # Test case with empty transaction records
        res = []
        expected_json = '[]'
        result = allByUserTransform(res)
        self.assertEqual(result, expected_json)

    def test_netMerchantTransform(self):
        # Test case with multiple net merchant records
        res = [
            ('2023-06-01', 5000, 123),
            ('2023-06-02', 3000, 123),
            ('2023-06-03', 2000, 123)
        ]
        expected_json = '[{"date":"2023-06-01","merchant_type_code":123,"net_amount_in_dollars":50.0},' \
                        '{"date":"2023-06-02","merchant_type_code":123,"net_amount_in_dollars":30.0},' \
                        '{"date":"2023-06-03","merchant_type_code":123,"net_amount_in_dollars":20.0}]'
        result = netMerchantTransform(res)
        self.assertEqual(result, expected_json)

        # Test case with empty net merchant records
        res = []
        expected_json = '[]'
        result = netMerchantTransform(res)
        self.assertEqual(result, expected_json)

    def test_netMerchantTransform_Empty(self):
        # Test case with multiple net merchant records
        res = []
        expected_json = '[]'
        result = netMerchantTransform(res)
        self.assertEqual(result, expected_json)

        # Test case with empty net merchant records
        res = []
        expected_json = '[]'
        result = netMerchantTransform(res)
        self.assertEqual(result, expected_json)


if __name__ == '__main__':
    unittest.main()

# coding: utf-8

"""
    UE Dataset API

    API definition for UE activity dataset.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.ue import UE

class TestUE(unittest.TestCase):
    """UE unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UE:
        """Test UE
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UE`
        """
        model = UE()
        if include_optional:
            return UE(
                id = 0,
                imsi = 'imsi-208930000008888',
                arrival_time = 1.38,
                applications = [
                    openapi_client.models.app_interval.AppInterval(
                        app_id = 1, 
                        start_time = 16.3, 
                        end_time = 163.52, )
                    ],
                leave_time = 82.25
            )
        else:
            return UE(
        )
        """

    def testUE(self):
        """Test UE"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()

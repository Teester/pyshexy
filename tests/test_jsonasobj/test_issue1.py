
import unittest


class ByteArrayTestCase(unittest.TestCase):
    def test_bytearray(self):
        from jsonasobj import load
        load("http://hl7.org/fhir/Patient/f201")


if __name__ == '__main__':
    unittest.main()

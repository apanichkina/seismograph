import unittest
import sys, os
from mock import *
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/'+'../..')
from seismograph.program import *
import seismograph.program as _program

class ProgramContextTests(unittest.TestCase):
    def setUp(self):
        self.testContext = ProgramContext('setup', 'teardown')

    def testSetupSaving(self):
        self.assertEqual('setup', self.testContext.setup_callbacks[0])

    def testTeardownSaving(self):
        self.assertEqual('teardown', self.testContext.teardown_callbacks[0])

    def testLayers(self):
        userLayers = [ Mock(enabled = False),  Mock(enabled = True),  Mock(enabled = True)]
        self.testContext.add_layers(userLayers)

        layerGenerator = self.testContext.layers

        for layer in userLayers:
            if layer.enabled:
                self.assertEqual(layer, layerGenerator.next())
        self.testContext = ProgramContext('setup', 'teardown')

    def testDefaultLayers(self):
        defaultLayers = [ Mock(enabled = True),  Mock(enabled = False),  Mock(enabled = True)]
        _program.DEFAULT_LAYERS.extend(defaultLayers)

        layerGenerator = self.testContext.layers

        for layer in defaultLayers:
            if layer.enabled:
                self.assertEqual(layer, layerGenerator.next())

        _program.DEFAULT_LAYERS = []


    def testLayersDefaultAndCustom(self):
        userLayers = [ Mock(enabled = False),  Mock(enabled = True),  Mock(enabled = True), Mock(enabled = False), Mock(enabled = True)]
        defaultLayers = [ Mock(enabled = True),  Mock(enabled = False),  Mock(enabled = True), Mock(enabled = False), Mock(enabled = True)]

        _program.DEFAULT_LAYERS.extend(defaultLayers)
        self.testContext.add_layers(userLayers)

        layerGenerator = self.testContext.layers

        for layer in defaultLayers:
            if layer.enabled:
                self.assertEqual(layer, layerGenerator.next())
        for layer in userLayers:
            if layer.enabled:
                self.assertEqual(layer, layerGenerator.next())

        _program.DEFAULT_LAYERS = []
        self.testContext = ProgramContext('setup', 'teardown')

    # @patch('seismograph.utils.common.call_to_chain')
    # @patch('seismograph.runnable.class_name')
    # @patch('seismograph.program.logger')
    # @patch('seismograph.program.Program')
    # def testStartContextLog(self, mock_program, mock_logger, mock_runnable, mock_call_to_chain):
    #     program = mock_program()
    #     print(mock_call_to_chain)
    #     self.testContext.start_context(program)
    #     mock_logger.debug.assert_called_with("Your log message here")




    def tearDown(self):
        pass
if __name__ == '__main__':
    print("\n")
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(FooTests)
    # unittest.TextTestRunner(verbosity=2).run(suite)

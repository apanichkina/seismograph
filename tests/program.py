import unittest
import sys
import os

from mock import Mock, patch, call

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/' + '..')
import seismograph.program as _program


class ProgramContextInitTests(unittest.TestCase):
    def setUp(self):
        self.setup = Mock(callable)
        self.testContext = _program.ProgramContext(self.setup, 'teardown')

    def testSetupSaving(self):
        self.assertEqual(self.setup, self.testContext.setup_callbacks[0])

    def testTeardownSaving(self):
        self.assertEqual('teardown', self.testContext.teardown_callbacks[0])

    def tearDown(self):
        pass


class ProgramContextLayersTests(unittest.TestCase):
    def setUp(self):
        self.setup = Mock(callable)
        self.testContext = _program.ProgramContext(self.setup, 'teardown')

        self.userLayers = getattr(self.testContext, '_' + self.testContext.__class__.__name__ + '__layers')
        userLayers = [Mock(enabled=True), Mock(enabled=True), Mock(enabled=True), Mock(enabled=False),
                      Mock(enabled=True)]
        self.userLayers.extend(userLayers[:])

        self.defaultLayers = [Mock(enabled=True), Mock(enabled=False), Mock(enabled=True), Mock(enabled=False),
                              Mock(enabled=True)]

        filteredLayers = []
        for layer in self.defaultLayers:
            if layer.enabled:
                filteredLayers.append(layer)
        for layer in self.userLayers:
            if layer.enabled:
                filteredLayers.append(layer)
        self.filteredLayersGenerator = (n for n in filteredLayers)

        _program.DEFAULT_LAYERS = self.defaultLayers[:]

        self.program = Mock()
        self.returned_value = "Mock"
        self.program.__class_name__ = Mock(return_value=self.returned_value)

    def testAddLayers(self):
        userLayers = [Mock(enabled=False), Mock(enabled=True), Mock(enabled=True)]
        list = self.userLayers[:]
        self.testContext.add_layers(userLayers)
        list.extend(userLayers)

        self.assertEqual(list, self.userLayers)

    def testDefaultLayers(self):
        layerGenerator = self.testContext.layers

        for layer in self.defaultLayers:
            if layer.enabled:
                self.assertEqual(layer, layerGenerator.next())

        _program.DEFAULT_LAYERS = []

    def testLayersDefaultAndCustom(self):
        layerGenerator = self.testContext.layers

        for layer in self.defaultLayers:
            if layer.enabled:
                self.assertEqual(layer, layerGenerator.next())
        for layer in self.userLayers:
            if layer.enabled:
                self.assertEqual(layer, layerGenerator.next())

        _program.DEFAULT_LAYERS = []
        self.testContext = _program.ProgramContext('setup', 'teardown')

    def tearDown(self):
        pass


class ProgramContextStartTests(unittest.TestCase):
    def setUp(self):
        self.setup = Mock(callable)
        self.testContext = _program.ProgramContext(self.setup, 'teardown')
        self.program = Mock()
        self.returned_value = "Mock"
        self.program.__class_name__ = Mock(return_value=self.returned_value)

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testStartContextLog(self, mock_logger, mock_to_chain):
        self.testContext.start_context(self.program)
        mock_logger.debug.assert_called_with('Start context of program "{}"'.format(self.returned_value))

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testStartContextChainCall(self, mock_logger, mock_to_chain):
        self.testContext.start_context(self.program)
        calls = [call([self.setup], None)]
        self.assertEqual(mock_to_chain.call_count, 2)
        mock_to_chain.assert_has_calls(calls, any_order=True)

    @patch('seismograph.program.runnable')
    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testStartContextBaseExceptionRaise(self, mock_logger, mock_to_chain, mock_runnable):
        mock_to_chain.side_effect = BaseException()
        mock_runnable.stopped_on = Mock()
        self.assertRaises(BaseException, self.testContext.start_context, self.program)

    @patch('seismograph.program.runnable')
    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testStartContextExceptionStoppedOn(self, mock_logger, mock_to_chain, mock_runnable):
        mock_to_chain.side_effect = BaseException()
        mock_runnable.stopped_on = Mock()
        try:
            self.testContext.start_context(self.program)
        except:
            pass
        mock_runnable.stopped_on.assert_called_once_with(self.program, "start_context")

    def tearDown(self):
        pass


class ProgramContextStopTests(unittest.TestCase):
    def setUp(self):
        self.setup = Mock(callable)
        self.testContext = _program.ProgramContext(self.setup, 'teardown')
        self.program = Mock()
        self.returned_value = "Mock"
        self.program.__class_name__ = Mock(return_value=self.returned_value)

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testStopContextLog(self, mock_logger, mock_to_chain):
        self.testContext.stop_context(self.program)
        mock_logger.debug.assert_called_with('Stop context of program "{}"'.format(self.returned_value))

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testStopContextChainCall(self, mock_logger, mock_to_chain):
        self.testContext.stop_context(self.program)
        self.assertEqual(mock_to_chain.call_count, 2)

    @patch('seismograph.program.runnable')
    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testStopContextBaseExceptionRaise(self, mock_logger, mock_to_chain, mock_runnable):
        mock_to_chain.side_effect = BaseException()
        mock_runnable.stopped_on = Mock()
        self.assertRaises(BaseException, self.testContext.stop_context, self.program)

    @patch('seismograph.program.runnable')
    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testStopContextExceptionStoppedOn(self, mock_logger, mock_to_chain, mock_runnable):
        mock_to_chain.side_effect = BaseException()
        mock_runnable.stopped_on = Mock()
        try:
            self.testContext.stop_context(self.program)
        except:
            pass
        mock_runnable.stopped_on.assert_called_once_with(self.program, "stop_context")

    def tearDown(self):
        pass


class ProgramContextOnInitTests(unittest.TestCase):
    def setUp(self):
        self.setup = Mock(callable)
        self.testContext = _program.ProgramContext(self.setup, 'teardown')
        self.program = Mock()
        self.returned_value = "Mock"
        self.program.__class_name__ = Mock(return_value=self.returned_value)

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testOnInitLog(self, mock_logger, mock_to_chain):
        self.testContext.on_init(self.program)
        mock_logger.debug.assert_called_with(
            'Call to chain callbacks "on_init" of program "{}"'.format(self.returned_value))

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testOnInitChainCall(self, mock_logger, mock_to_chain):
        self.testContext.on_init(self.program)
        self.assertEqual(mock_to_chain.call_count, 1)

    def tearDown(self):
        pass


class ProgramContextOnConfigTests(unittest.TestCase):
    def setUp(self):
        self.setup = Mock(callable)
        self.testContext = _program.ProgramContext(self.setup, 'teardown')
        self.program = Mock()
        self.returned_value = "Mock"
        self.program.__class_name__ = Mock(return_value=self.returned_value)

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testOnConfigLog(self, mock_logger, mock_to_chain):
        config1 = Mock(callable)
        config2 = Mock(callable)
        self.testContext.on_config(self.program, [config1, config2])
        mock_logger.debug.assert_called_with(
            'Call to chain callbacks "on_config" of program "{}"'.format(self.returned_value))

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testOnConfigChainCall(self, mock_logger, mock_to_chain):
        config1 = Mock(callable)
        config2 = Mock(callable)
        self.testContext.on_config(self.program, [config1, config2])
        self.assertEqual(mock_to_chain.call_count, 1)

    def tearDown(self):
        pass


class ProgramContextErrorTests(unittest.TestCase):
    def setUp(self):
        self.setup = Mock(callable)
        self.testContext = _program.ProgramContext(self.setup, 'teardown')
        self.program = Mock()
        self.returned_value = "Mock"
        self.program.__class_name__ = Mock(return_value=self.returned_value)

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testErrorContextLog(self, mock_logger, mock_to_chain):
        self.testContext.on_error('TestError', self.program, 'TestResult')
        mock_logger.debug.assert_called_with(
            'Call to chain callbacks "on_error" of program "{}"'.format(self.returned_value))

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testErrorContextChainCall(self, mock_logger, mock_to_chain):
        self.testContext.on_error('TestError', self.program, 'TestResult')
        calls = [call([self.setup], None)]
        self.assertEqual(mock_to_chain.call_count, 1)

    @patch('seismograph.program.runnable')
    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testErrorContextBaseExceptionRaise(self, mock_logger, mock_to_chain, mock_runnable):
        mock_to_chain.side_effect = BaseException()
        mock_runnable.stopped_on = Mock()
        self.assertRaises(BaseException, self.testContext.on_error, 'TestError', self.program, 'TestResult')

    def tearDown(self):
        pass


class ProgramContextOnOptionTests(unittest.TestCase):
    def setUp(self):
        self.setup = Mock(callable)
        self.testContext = _program.ProgramContext(self.setup, 'teardown')
        self.program = Mock()
        self.returned_value = "Mock"
        self.program.__class_name__ = Mock(return_value=self.returned_value)

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testOnOptionLog(self, mock_logger, mock_to_chain):
        self.testContext.on_option_parser('TestParser')
        mock_logger.debug.assert_called_with('Call to chain callbacks "on_option_parser" of program')

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testOnOptionChainCall(self, mock_logger, mock_to_chain):
        self.testContext.on_option_parser('TestParser')
        self.assertEqual(mock_to_chain.call_count, 1)

    def tearDown(self):
        pass


class ProgramContextOnRunTests(unittest.TestCase):
    def setUp(self):
        self.setup = Mock(callable)
        self.testContext = _program.ProgramContext(self.setup, 'teardown')
        self.program = Mock()
        self.returned_value = "Mock"
        self.program.__class_name__ = Mock(return_value=self.returned_value)

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testOnRunContextLog(self, mock_logger, mock_to_chain):
        self.testContext.on_run(self.program)
        mock_logger.debug.assert_called_with(
            'Call to chain callbacks "on_run" of program "{}"'.format(self.returned_value))

    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testOnRunContextChainCall(self, mock_logger, mock_to_chain):
        self.testContext.on_run(self.program)
        calls = [call([self.setup], None)]
        self.assertEqual(mock_to_chain.call_count, 1)

    @patch('seismograph.program.runnable')
    @patch('seismograph.program.call_to_chain')
    @patch('seismograph.program.logger')
    def testOnRunContextBaseExceptionRaise(self, mock_logger, mock_to_chain, mock_runnable):
        mock_to_chain.side_effect = BaseException()
        mock_runnable.stopped_on = Mock()
        self.assertRaises(BaseException, self.testContext.on_run, self.program)

    def tearDown(self):
        pass


@patch('seismograph.program.extensions')
@patch('seismograph.program.ext')
@patch('seismograph.program.ProgramContext')
class ProgramInit(unittest.TestCase):
    def setUp(self):
        self.patcherConfig = patch('seismograph.program.config')
        self.mockConfig = self.patcherConfig.start()
        _program.Program.__config_class__ = Mock(OUTPUT=Mock())
        self.parser = Mock()
        self.parser.parse_args = Mock(return_value=('TestOptions', None))
        self.mockConfig.create_option_parser = Mock(return_value=self.parser)

    @patch('seismograph.program.Program.register_scripts')
    @patch('seismograph.program.Program.register_suites')
    @patch('seismograph.program.Program._make_result')
    def testInitArgv(self, mockMakeResult, mockRegisterSuites, mockRegisterScripts, mockContext, mockExt,
                     mockExtensions):
        newargs = ['TestArg1', 'TestArg2']
        args = sys.argv[:]
        _program.Program(argv=newargs)
        args.extend(newargs)
        self.assertEqual(args, sys.argv)

    @patch('seismograph.program.Program.register_scripts')
    @patch('seismograph.program.Program.register_suites')
    @patch('seismograph.program.Program._make_result')
    def testInit__Layers__(self, mockMakeResult, mockRegisterSuites, mockRegisterScripts, mockContext, mockExt,
                           mockExtensions):
        progContextObject = Mock()
        progContextObject.add_layers = Mock()
        mockContext.return_value = progContextObject
        newargs = ['TestArg1', 'TestArg2']
        _program.Program.__layers__ = newargs
        _program.Program()
        progContextObject.add_layers.assert_called_once_with(newargs)

    @patch('seismograph.program.Program.register_scripts')
    @patch('seismograph.program.Program.register_suites')
    @patch('seismograph.program.Program._make_result')
    def testInitLayers(self, mockMakeResult, mockRegisterSuites, mockRegisterScripts, mockContext, mockExt,
                       mockExtensions):
        progContextObject = Mock()
        progContextObject.add_layers = Mock()
        mockContext.return_value = progContextObject
        newargs = ['TestArg1', 'TestArg2']
        _program.Program(layers=newargs)
        progContextObject.add_layers.assert_called_once_with(newargs)

    @patch('seismograph.program.Program.register_scripts')
    @patch('seismograph.program.Program.register_suites')
    @patch('seismograph.program.Program._make_result')
    def testInitExtensionsAdd(self, mockMakeResult, mockRegisterSuites, mockRegisterScripts, mockContext, mockExt,
                              mockExtensions):
        extensions = [Mock(), Mock(), Mock()]
        mockExt.TO_INIT = extensions[:]
        _program.Program()
        calls = []
        for extension in extensions:
            calls.append(call(extension, self.parser))
        mockExtensions.add_options.assert_has_calls(calls, any_order=True)

    @patch('seismograph.program.Program.register_scripts')
    @patch('seismograph.program.Program.register_suites')
    @patch('seismograph.program.Program._make_result')
    def testInitSuitesAdd(self, mockMakeResult, mockRegisterSuites, mockRegisterScripts, mockContext, mockExt,
                          mockExtensions):
        suites = [Mock(), Mock(), Mock()]
        _program.Program(suites=suites)
        mockRegisterSuites.assert_called_with(suites)

    @patch('seismograph.program.Program.register_scripts')
    @patch('seismograph.program.Program.register_suites')
    @patch('seismograph.program.Program._make_result')
    def testInitScriptAdd(self, mockMakeResult, mockRegisterSuites, mockRegisterScripts, mockContext, mockExt,
                          mockExtensions):
        scripts = [Mock(), Mock(), Mock()]
        _program.Program(scripts=scripts)
        mockRegisterScripts.assert_called_with(scripts)

    @patch('seismograph.program.loader.load_suites_from_path')
    @patch('seismograph.program.loader.load_suites_from_module')
    @patch('seismograph.program.loader')
    @patch('seismograph.program.Program._make_result')
    def testLoadSuitesNoPath(self,mockMakeResult ,mock_loader, load_module, load_path, mockContext, mockExt, mockExtensions):
        self.program = _program.Program()
        self.program.load_suites()
        assert load_module.called

    @patch('seismograph.program.loader.load_suites_from_path')
    @patch('seismograph.program.loader.load_suites_from_module')
    @patch('seismograph.program.loader')
    @patch('seismograph.program.Program._make_result')
    def testLoadSuitesWithPath(self,mockMakeResult ,mock_loader, load_module, load_path, mockContext, mockExt, mockExtensions):
        self.program = _program.Program()
        self.program.load_suites('lol')
        assert load_path.called

    def tearDown(self):
        self.patcherConfig.stop()

@patch('seismograph.program.extensions')
@patch('seismograph.program.ext')
@patch('seismograph.program.ProgramContext')
class ProgramMethods(unittest.TestCase):
    def setUp(self):
        # self.patcherConfig = patch('seismograph.program.config')
        # self.mockConfig = self.patcherConfig.start()

        self.config = Mock(OUTPUT='Test.txt')
        _program.Program.__layers__ = None
        _program.Program.__config_class__ = Mock(return_value=self.config)
        # self.program = Program()
        self.parser = Mock()
        self.parser.parse_args = Mock(return_value=('TestOptions', None))

    def testProgramNoSuitesAndScripts(self, mockContext, mockExt, mockExtensions):
        self.program = _program.Program()
        self.assertRaises(RuntimeError, self.program.__run__)

    def testSuiteGroupClass(self, mockContext, mockExt, mockExtensions):
        self.program = _program.Program()
        suiteGroup = Mock()
        self.program.__suite_group_class__ = Mock(return_value = suiteGroup)
        a = self.program._make_group()
        self.assertEqual(suiteGroup, a)

    @patch('seismograph.groups.gevent.GeventSuiteGroup')
    def testGeventSuite(self, mockGevent, mockContext, mockExt, mockExtensions):
        self.program = _program.Program()
        self.program.__suite_group_class__ = None
        geventGroup = Mock()
        mockGevent.return_value = geventGroup
        self.program.config.GEVENT = 1
        self.assertEqual(geventGroup, self.program._make_group())

    @patch('seismograph.groups.threading.ThreadingSuiteGroup')
    def testThreadingSuite(self, mockThreading, mockContext, mockExt, mockExtensions):
        self.program = _program.Program()
        self.program.__suite_group_class__ = None
        threadingGroup = Mock()
        mockThreading.return_value = threadingGroup
        self.program.config.GEVENT = None
        self.program.config.THREADING = 1
        self.assertEqual(threadingGroup, self.program._make_group())

    @patch('seismograph.groups.multiprocessing.MultiprocessingSuiteGroup')
    def testMultiProcessingSuite(self, mockProcessing, mockContext, mockExt, mockExtensions):
        self.program = _program.Program()
        self.program.__suite_group_class__ = None
        processingGroup = Mock()
        mockProcessing.return_value = processingGroup
        self.program.config.GEVENT = None
        self.program.config.THREADING = None
        self.program.config.PROCESSING = 1
        self.assertEqual(processingGroup, self.program._make_group())

    def tearDown(self):
       pass



if __name__ == '__main__':
    print("\n")
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(FooTests)
    # unittest.TextTestRunner(verbosity=2).run(suite)

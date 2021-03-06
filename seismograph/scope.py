# -*- coding: utf-8 -*-

"""
Module for configuration global context
"""

import seismograph.case as _case
import seismograph.xunit as _xunit
import seismograph.suite as _suite
import seismograph.loader as _loader
import seismograph.program as _program
import seismograph.runnable as _runnable


shared_data = _program.Program.shared_data
shared_extension = _program.Program.shared_extension


def match_suite_to_layer(cls, layer):
    _suite.MATCH_SUITE_TO_LAYER[cls] = layer


def match_case_to_layer(cls, layer):
    _case.MATCH_CASE_TO_LAYER[cls] = layer


def set_default_case_layers(*layers):
    _case.DEFAULT_LAYERS.extend(layers)


def set_default_suite_layers(*layers):
    _suite.DEFAULT_LAYERS.extend(layers)


def set_default_program_layers(*layers):
    _program.DEFAULT_LAYERS.extend(layers)


def configure(
        round_runtime=None,
        config_env_name=None,
        test_name_prefix=None,
        case_group_class=None,
        suite_group_class=None,
        default_test_name=None,
        skip_attribute_name=None,
        skip_why_attribute_name=None,
        use_static_test_functions=False):
    """
    Configure global context

    :param round_runtime:
    :param config_env_name:
    :param test_name_prefix:
    :param case_group_class:
    :param suite_group_class:
    :param default_test_name:
    :param skip_attribute_name:
    :param skip_why_attribute_name:
    :param use_static_test_functions:
    """
    if round_runtime:
        assert type(round_runtime) == int
        _xunit.ROUND_RUNTIME = round_runtime

    if use_static_test_functions:
        _case.Case.__static__ = True

    if config_env_name:
        _program.CONFIG_ENV_NAME = config_env_name

    if test_name_prefix:
        _loader.TEST_NAME_PREFIX = test_name_prefix

    if default_test_name:
        _loader.DEFAULT_TEST_NAME = default_test_name

    if skip_attribute_name:
        _case.SKIP_ATTRIBUTE_NAME = skip_attribute_name

    if skip_why_attribute_name:
        _case.SKIP_WHY_ATTRIBUTE_NAME = skip_why_attribute_name

    if case_group_class:
        assert issubclass(case_group_class, _runnable.RunnableGroup)
        _suite.Suite.__case_group_class__ = case_group_class

    if suite_group_class:
        assert issubclass(suite_group_class, _runnable.RunnableGroup)
        _program.Program.__suite_group_class__ = suite_group_class

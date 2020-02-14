# Most of the tests for the config code are in the integration tests as they require running
# arango and auth instances

import os
import shutil
import tempfile
import yaml
from pytest import raises, fixture
from jsonschema.exceptions import ValidationError

from core import test_utils
from core.test_utils import assert_exception_correct
from SampleService.core.config import get_validators


@fixture(scope='module')
def temp_dir():
    tempdir = test_utils.get_temp_dir()
    yield tempdir

    if test_utils.get_delete_temp_files():
        shutil.rmtree(test_utils.get_temp_dir())


def _write_config(cfg, temp_dir):
    tf = tempfile.mkstemp('.tmp.cfg', 'config_test_', dir=temp_dir)
    os.close(tf[0])
    with open(tf[1], 'w') as temp:
        yaml.dump(cfg, temp)
    return tf[1]


def test_config_get_validators(temp_dir):
    cfg = {'key1': [{'module': 'core.config_test_vals',
                     'callable-builder': 'val1'
                     }],
           'key2': [{'module': 'core.config_test_vals',
                     'callable-builder': 'val2',
                     'parameters': {'max-len': 7, 'foo': 'bar'}
                     },
                    {'module': 'core.config_test_vals',
                     'callable-builder': 'val2',
                     'parameters': {'max-len': 5, 'foo': 'bar'},
                     'prefix': False
                     }],
           'key3': [{'module': 'core.config_test_vals',
                     'callable-builder': 'val1',
                     'parameters': {'foo': 'bat'}
                     }],
           'key4': [{'module': 'core.config_test_vals',
                     'callable-builder': 'pval1',
                     'prefix': True
                     }],
           'key5': [{'module': 'core.config_test_vals',
                     'callable-builder': 'pval2',
                     'parameters': {'max-len': 7, 'foo': 'bar'},
                     'prefix': True,
                     },
                    {'module': 'core.config_test_vals',
                     'callable-builder': 'pval2',
                     'prefix': True,
                     'parameters': {'max-len': 5, 'foo': 'bar'}
                     }],
           'key6': [{'module': 'core.config_test_vals',
                     'callable-builder': 'pval1',
                     'prefix': True,
                     'parameters': {'foo': 'bat'}
                     }]
           }
    tf = _write_config(cfg, temp_dir)
    vals = get_validators('file://' + tf)
    assert len(vals.keys()) == 3
    assert len(vals.prefix_keys()) == 3
    # the test validators always fail
    assert vals.validator_count('key1') == 1
    assert vals.call_validator('key1', 0, {'a': 'b'}) == "1, key1, {}, {'a': 'b'}"

    assert vals.validator_count('key2') == 2
    assert vals.call_validator(
        'key2', 0, {'a': 'd'}) == "2, key2, {'foo': 'bar', 'max-len': 7}, {'a': 'd'}"
    assert vals.call_validator(
        'key2', 1, {'a': 'd'}) == "2, key2, {'foo': 'bar', 'max-len': 5}, {'a': 'd'}"

    assert vals.validator_count('key3') == 1
    assert vals.call_validator('key3', 0, {'a': 'c'}) == "1, key3, {'foo': 'bat'}, {'a': 'c'}"

    assert vals.prefix_validator_count('key4') == 1
    assert vals.call_prefix_validator(
        'key4', 0, 'key4stuff', {'a': 'b'}) == "1, key4, key4stuff, {}, {'a': 'b'}"

    assert vals.prefix_validator_count('key5') == 2
    assert vals.call_prefix_validator(
        'key5', 0, 'key5s', {'a': 'd'}
        ) == "2, key5, key5s, {'foo': 'bar', 'max-len': 7}, {'a': 'd'}"
    assert vals.call_prefix_validator(
        'key5', 1, 'key5s1', {'a': 'd'}
        ) == "2, key5, key5s1, {'foo': 'bar', 'max-len': 5}, {'a': 'd'}"

    assert vals.prefix_validator_count('key6') == 1
    assert vals.call_prefix_validator(
        'key6', 0, 'key6s', {'a': 'c'}) == "1, key6, key6s, {'foo': 'bat'}, {'a': 'c'}"

    # noop entry
    cfg = {}
    tf = _write_config(cfg, temp_dir)
    vals = get_validators('file://' + tf)
    assert len(vals.keys()) == 0
    assert len(vals.prefix_keys()) == 0


def test_config_get_validators_fail_bad_file(temp_dir):
    tf = _write_config({}, temp_dir)
    os.remove(tf)
    with raises(Exception) as got:
        get_validators('file://' + tf)
    assert_exception_correct(got.value, ValueError(
        f"Failed to open validator configuration file at file://{tf}: " +
        f"[Errno 2] No such file or directory: '{tf}'"))


def test_config_get_validators_fail_bad_yaml(temp_dir):
    # calling str() on ValidationErrors returns more detailed into about the error
    tf = tempfile.mkstemp('.tmp.cfg', 'config_test_bad_yaml', dir=temp_dir)
    os.close(tf[0])
    with open(tf[1], 'w') as temp:
        temp.write('[bad yaml')
    with raises(Exception) as got:
        get_validators('file://' + tf[1])
    assert_exception_correct(got.value, ValueError(
        f'Failed to open validator configuration file at file://{tf[1]}: while parsing a ' +
        'flow sequence\n  in "<urllib response>", line 1, column 1\nexpected \',\' or \']\', ' +
        'but got \'<stream end>\'\n  in "<urllib response>", line 1, column 10'
    ))


def test_config_get_validators_fail_bad_params(temp_dir):
    # calling str() on ValidationErrors returns more detailed into about the error
    _config_get_validators_fail(
        '', temp_dir,
        ValidationError("'' is not of type 'object'"))
    _config_get_validators_fail(
        ['foo', 'bar'], temp_dir,
        ValidationError("['foo', 'bar'] is not of type 'object'"))
    _config_get_validators_fail(
        {'key': 'y'}, temp_dir,
        ValidationError("'y' is not of type 'array'"))
    _config_get_validators_fail(
        {'key': ['foo']}, temp_dir,
        ValidationError("'foo' is not of type 'object'"))
    _config_get_validators_fail(
        {'key': [{}]}, temp_dir,
        ValidationError("'module' is a required property"))
    _config_get_validators_fail(
        {'key': [{'module': 'foo'}]}, temp_dir,
        ValidationError("'callable-builder' is a required property"))
    _config_get_validators_fail(
        {'key': [{'module': 'foo', 'callable-builder': 'bar', 'xtraprop': 1}]}, temp_dir,
        ValidationError("Additional properties are not allowed ('xtraprop' was unexpected)"))
    _config_get_validators_fail(
        {'key': [{'module': ['foo'], 'callable-builder': 'bar'}]}, temp_dir,
        ValidationError("['foo'] is not of type 'string'"))
    _config_get_validators_fail(
        {'key': [{'module': 'foo', 'callable-builder': ['bar']}]}, temp_dir,
        ValidationError("['bar'] is not of type 'string'"))
    _config_get_validators_fail(
        {'key': [{'module': 'foo', 'callable-builder': 'bar', 'parameters': 'foo'}]}, temp_dir,
        ValidationError("'foo' is not of type 'object'"))
    _config_get_validators_fail(
        {'key': [{'module': 'foo', 'callable-builder': 'bar', 'prefix': 0}]}, temp_dir,
        ValidationError("0 is not of type 'boolean'"))


def test_config_get_validators_fail_no_module(temp_dir):
    _config_get_validators_fail(
        {'key': [{'module': 'no_modules_here', 'callable-builder': 'foo'}]}, temp_dir,
        ModuleNotFoundError("No module named 'no_modules_here'"))


def test_config_get_validators_fail_no_function(temp_dir):
    _config_get_validators_fail(
        {'x': [{'module': 'core.config_test_vals', 'callable-builder': 'foo'}]}, temp_dir,
        ValueError("Metadata validator callable build #0 failed for key x: " +
                   "module 'core.config_test_vals' has no attribute 'foo'"))


def test_config_get_validators_fail_function_exception(temp_dir):
    _config_get_validators_fail(
        {'x': [{'module': 'core.config_test_vals', 'callable-builder': 'val1'},
               {'module': 'core.config_test_vals', 'callable-builder': 'fail_val'}]},
        temp_dir,
        ValueError("Metadata validator callable build #1 failed for key x: " +
                   "we've no functions 'ere"))


def test_config_get_prefix_validators_fail_function_exception(temp_dir):
    _config_get_validators_fail(
        {'p': [{'module': 'core.config_test_vals',
                'callable-builder': 'val1',
                'prefix': True},
               {'module': 'core.config_test_vals',
                'callable-builder': 'val1',
                'prefix': True},
               {'module': 'core.config_test_vals',
                'callable-builder': 'fail_prefix_val',
                'prefix': True}
               ]},
        temp_dir,
        ValueError("Metadata validator callable build #2 failed for key p: " +
                   "we've no prefix functions 'ere"))


def _config_get_validators_fail(cfg, temp_dir, expected):
    tf = _write_config(cfg, temp_dir)
    with raises(Exception) as got:
        get_validators('file://' + tf)
    assert_exception_correct(got.value, expected)

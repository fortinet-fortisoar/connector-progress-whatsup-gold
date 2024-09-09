# Edit the config_and_params.json file and add the necessary parameter values.
"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import os
import sys
import json
import pytest
import logging
import importlib
from connectors.core.connector import ConnectorError

with open('tests/config_and_params.json', 'r') as file:
    params = json.load(file)

current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
grandparent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
sys.path.insert(0, str(grandparent_directory))

module_name = 'progress-whatsup-gold_1_0_0.operations'
conn_operations_module = importlib.import_module(module_name)
operations = conn_operations_module.operations

with open('info.json', 'r') as file:
    info_json = json.load(file)

logger = logging.getLogger(__name__)
    

# To test with different configuration values, adjust the index in the list below.
@pytest.fixture(scope="module")
def valid_configuration():
    return params.get('config')[0]
    
    
@pytest.fixture(scope="module")
def valid_configuration_with_token(valid_configuration):
    config = valid_configuration.copy()
    try:
        operations['check_health'](config)
    except TypeError:
        connector_info = config['connector_info']
        operations['check_health'](config, connector_info)
    return config
    

@pytest.mark.checkhealth     
def test_check_health_success(valid_configuration):
    config = valid_configuration.copy()
    try:
        result = operations['check_health'](config)
    except TypeError:
        connector_info = config['connector_info']
        result = operations['check_health'](config, connector_info)
    assert result  
    

@pytest.mark.checkhealth     
def test_check_health_invalid_username(valid_configuration):
    invalid_config = valid_configuration.copy()
    invalid_config['username'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        try:
            operations['check_health'](invalid_config)
        except TypeError:
            connector_info = invalid_config['connector_info']
            operations['check_health'](invalid_config, connector_info)
    

@pytest.mark.checkhealth     
def test_check_health_invalid_password(valid_configuration):
    invalid_config = valid_configuration.copy()
    invalid_config['password'] = params.get('invalid_params')['password']
    with pytest.raises(ConnectorError):
        try:
            operations['check_health'](invalid_config)
        except TypeError:
            connector_info = invalid_config['connector_info']
            operations['check_health'](invalid_config, connector_info)
    

@pytest.mark.checkhealth     
def test_check_health_invalid_resource(valid_configuration):
    invalid_config = valid_configuration.copy()
    invalid_config['resource'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        try:
            operations['check_health'](invalid_config)
        except TypeError:
            connector_info = invalid_config['connector_info']
            operations['check_health'](invalid_config, connector_info)
    

@pytest.mark.get_device_attributes
@pytest.mark.parametrize("input_params", params['get_device_attributes'])
def test_get_device_attributes_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_device_attributes'](valid_configuration_with_token.copy(), input_params.copy())
  
    
# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_device_attributes
@pytest.mark.schema_validation
def test_validate_get_device_attributes_output_schema(valid_configuration_with_token):
    input_params = params.get('get_device_attributes')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_device_attributes':
            if operation.get('conditional_output_schema'):
                pytest.skip("Skipping test because conditional_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    resp = operations['get_device_attributes'](valid_configuration_with_token.copy(), input_params)
    if isinstance(resp, dict) and isinstance(schema, dict):
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")
    

@pytest.mark.get_device_attributes     
def test_get_device_attributes_invalid_device_id(valid_configuration_with_token):
    input_params = params.get('get_device_attributes')[0].copy()
    input_params['device_id'] = params.get('invalid_params')['integer']
    assert operations['get_device_attributes'](valid_configuration_with_token.copy(), input_params) == {"message": "Not Found"}
    

@pytest.mark.get_device_attributes     
def test_get_device_attributes_invalid_pageId(valid_configuration_with_token):
    input_params = params.get('get_device_attributes')[0].copy()
    input_params['pageId'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        operations['get_device_attributes'](valid_configuration_with_token.copy(), input_params)
    

@pytest.mark.get_device_attributes     
def test_get_device_attributes_invalid_limit(valid_configuration_with_token):
    input_params = params.get('get_device_attributes')[0].copy()
    input_params['limit'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        operations['get_device_attributes'](valid_configuration_with_token.copy(), input_params)
    

@pytest.mark.get_device_groups
@pytest.mark.parametrize("input_params", params['get_device_groups'])
def test_get_device_groups_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_device_groups'](valid_configuration_with_token.copy(), input_params.copy())
  
    
# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_device_groups
@pytest.mark.schema_validation
def test_validate_get_device_groups_output_schema(valid_configuration_with_token):
    input_params = params.get('get_device_groups')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_device_groups':
            if operation.get('conditional_output_schema'):
                pytest.skip("Skipping test because conditional_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    resp = operations['get_device_groups'](valid_configuration_with_token.copy(), input_params)
    if isinstance(resp, dict) and isinstance(schema, dict):
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")
    

@pytest.mark.get_device_groups     
def test_get_device_groups_invalid_device_id(valid_configuration_with_token):
    input_params = params.get('get_device_groups')[0].copy()
    input_params['device_id'] = params.get('invalid_params')['integer']
    assert operations['get_device_groups'](valid_configuration_with_token.copy(), input_params) == {"message": "Not Found"}
    

@pytest.mark.get_device_groups     
def test_get_device_groups_invalid_pageId(valid_configuration_with_token):
    input_params = params.get('get_device_groups')[0].copy()
    input_params['pageId'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        operations['get_device_groups'](valid_configuration_with_token.copy(), input_params)
    

@pytest.mark.get_device_groups     
def test_get_device_groups_invalid_limit(valid_configuration_with_token):
    input_params = params.get('get_device_groups')[0].copy()
    input_params['limit'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        operations['get_device_groups'](valid_configuration_with_token.copy(), input_params)
    

@pytest.mark.get_device_monitors
@pytest.mark.parametrize("input_params", params['get_device_monitors'])
def test_get_device_monitors_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_device_monitors'](valid_configuration_with_token.copy(), input_params.copy())
  
    
# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_device_monitors
@pytest.mark.schema_validation
def test_validate_get_device_monitors_output_schema(valid_configuration_with_token):
    input_params = params.get('get_device_monitors')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_device_monitors':
            if operation.get('conditional_output_schema'):
                pytest.skip("Skipping test because conditional_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    resp = operations['get_device_monitors'](valid_configuration_with_token.copy(), input_params)
    if isinstance(resp, dict) and isinstance(schema, dict):
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")
    

@pytest.mark.get_device_monitors     
def test_get_device_monitors_invalid_device_id(valid_configuration_with_token):
    input_params = params.get('get_device_monitors')[0].copy()
    input_params['device_id'] = params.get('invalid_params')['integer']
    assert operations['get_device_monitors'](valid_configuration_with_token.copy(), input_params) == {"message": "Not Found"}
    

@pytest.mark.get_device_monitors     
def test_get_device_monitors_invalid_pageId(valid_configuration_with_token):
    input_params = params.get('get_device_monitors')[0].copy()
    input_params['pageId'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        operations['get_device_monitors'](valid_configuration_with_token.copy(), input_params)
    

@pytest.mark.get_device_monitors     
def test_get_device_monitors_invalid_limit(valid_configuration_with_token):
    input_params = params.get('get_device_monitors')[0].copy()
    input_params['limit'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        operations['get_device_monitors'](valid_configuration_with_token.copy(), input_params)
    

@pytest.mark.get_device_polling_configuration
@pytest.mark.parametrize("input_params", params['get_device_polling_configuration'])
def test_get_device_polling_configuration_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_device_polling_configuration'](valid_configuration_with_token.copy(), input_params.copy())
  
    
# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_device_polling_configuration
@pytest.mark.schema_validation
def test_validate_get_device_polling_configuration_output_schema(valid_configuration_with_token):
    input_params = params.get('get_device_polling_configuration')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_device_polling_configuration':
            if operation.get('conditional_output_schema'):
                pytest.skip("Skipping test because conditional_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    resp = operations['get_device_polling_configuration'](valid_configuration_with_token.copy(), input_params)
    if isinstance(resp, dict) and isinstance(schema, dict):
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")
    

@pytest.mark.get_device_polling_configuration     
def test_get_device_polling_configuration_invalid_device_id(valid_configuration_with_token):
    input_params = params.get('get_device_polling_configuration')[0].copy()
    input_params['device_id'] = params.get('invalid_params')['integer']
    assert operations['get_device_polling_configuration'](valid_configuration_with_token.copy(), input_params) == {"message": "Not Found"}
    

@pytest.mark.get_device_summary
@pytest.mark.parametrize("input_params", params['get_device_summary'])
def test_get_device_summary_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_device_summary'](valid_configuration_with_token.copy(), input_params.copy())
  
    
# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_device_summary
@pytest.mark.schema_validation
def test_validate_get_device_summary_output_schema(valid_configuration_with_token):
    input_params = params.get('get_device_summary')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_device_summary':
            if operation.get('conditional_output_schema'):
                pytest.skip("Skipping test because conditional_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    resp = operations['get_device_summary'](valid_configuration_with_token.copy(), input_params)
    if isinstance(resp, dict) and isinstance(schema, dict):
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")
    

@pytest.mark.get_device_summary     
def test_get_device_summary_invalid_device_id(valid_configuration_with_token):
    input_params = params.get('get_device_summary')[0].copy()
    input_params['device_id'] = params.get('invalid_params')['integer']
    assert operations['get_device_summary'](valid_configuration_with_token.copy(), input_params) == {"message": "Not Found"}
    

@pytest.mark.get_device_overview
@pytest.mark.parametrize("input_params", params['get_device_overview'])
def test_get_device_overview_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_device_overview'](valid_configuration_with_token.copy(), input_params.copy())
  
    
# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_device_overview
@pytest.mark.schema_validation
def test_validate_get_device_overview_output_schema(valid_configuration_with_token):
    input_params = params.get('get_device_overview')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_device_overview':
            if operation.get('conditional_output_schema'):
                pytest.skip("Skipping test because conditional_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    resp = operations['get_device_overview'](valid_configuration_with_token.copy(), input_params)
    if isinstance(resp, dict) and isinstance(schema, dict):
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")
    

@pytest.mark.get_device_overview     
def test_get_device_overview_invalid_device_id(valid_configuration_with_token):
    input_params = params.get('get_device_overview')[0].copy()
    input_params['device_id'] = params.get('invalid_params')['integer']
    assert operations['get_device_overview'](valid_configuration_with_token.copy(), input_params) == {"message": "Not Found"}
    

@pytest.mark.get_device_report
@pytest.mark.parametrize("input_params", params['get_device_report'])
def test_get_device_report_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_device_report'](valid_configuration_with_token.copy(), input_params.copy())
  
    
# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_device_report
@pytest.mark.schema_validation
def test_validate_get_device_report_output_schema(valid_configuration_with_token):
    input_params = params.get('get_device_report')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_device_report':
            if operation.get('conditional_output_schema'):
                pytest.skip("Skipping test because conditional_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    logger.info("output_schema: {0}".format(schema))
    resp = operations['get_device_report'](valid_configuration_with_token.copy(), input_params)
    if isinstance(resp, dict) and isinstance(schema, dict):
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")
    

@pytest.mark.get_device_report     
def test_get_device_report_invalid_device_id(valid_configuration_with_token):
    input_params = params.get('get_device_report')[0].copy()
    input_params['device_id'] = params.get('invalid_params')['integer']
    assert operations['get_device_report'](valid_configuration_with_token.copy(), input_params) == {"message": "Not Found"}
    

@pytest.mark.get_device_report     
def test_get_device_report_invalid_pageId(valid_configuration_with_token):
    input_params = params.get('get_device_report')[0].copy()
    input_params['pageId'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        operations['get_device_report'](valid_configuration_with_token.copy(), input_params)
    

@pytest.mark.get_device_report     
def test_get_device_report_invalid_limit(valid_configuration_with_token):
    input_params = params.get('get_device_report')[0].copy()
    input_params['limit'] = params.get('invalid_params')['integer']
    with pytest.raises(ConnectorError):
        operations['get_device_report'](valid_configuration_with_token.copy(), input_params)
    

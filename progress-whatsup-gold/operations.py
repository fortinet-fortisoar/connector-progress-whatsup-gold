"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""


import requests
from .constants import *
from .whatsup_gold_api_auth import *
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('progress-whatsup-gold')


class ProgressWhatsUpGold(object):
    def __init__(self, config):
        self.server_url = config.get('resource', '').strip('/')
        if not self.server_url.startswith('https://') and not self.server_url.startswith('http://'):
            self.server_url = 'https://' + self.server_url
        self.verify_ssl = config.get('verify_ssl')
        self.wg_auth = WhatsUpGoldAuth(config)
        self.connector_info = config.pop('connector_info', '')

    def make_rest_call(self, config, endpoint=None, params=None, json_body=None, payload=None, method='GET'):
        token = self.wg_auth.validate_token(config, self.connector_info)
        headers = {'Authorization': token, 'Accept': 'application/json'}
        service_url = f'{self.server_url}/api/v1/{endpoint}'
        logger.debug('Request URL {0}'.format(service_url))
        try:
            response = requests.request(method, service_url, data=payload, headers=headers, json=json_body,
                                        params=params, verify=self.verify_ssl)
            if response.ok:
                if response.status_code == 204:
                    return response
                content_type = response.headers.get('Content-Type')
                if response.text != "" and 'application/json' in content_type:
                    return response.json()
                else:
                    return response.content
            elif response.status_code == 404:
                return {"message": "Not Found"}
            else:
                if response.text != "":
                    err_resp = response.json()
                    if err_resp and 'error_description' in err_resp:
                        failure_msg = err_resp.get('error_description')
                        error_msg = 'Response {0}: {1} Error Message: {2}'.format(response.status_code,
                                                                                  response.reason,
                                                                                  failure_msg if failure_msg else '')
                        raise ConnectorError(error_msg)
                    elif err_resp and 'error' in err_resp and isinstance(err_resp.get('error'), dict):
                        failure_msg = err_resp.get('error').get('message')
                        error_msg = 'Response {0}: {1} Error Message: {2}'.format(response.status_code,
                                                                                  response.reason,
                                                                                  failure_msg if failure_msg else '')
                        raise ConnectorError(error_msg)
                else:
                    error_msg = '{0}: {1}'.format(response.status_code, response.reason)
                    raise ConnectorError(error_msg)
        except requests.exceptions.SSLError:
            logger.error('An SSL error occurred')
            raise ConnectorError('An SSL error occurred')
        except requests.exceptions.ConnectionError:
            logger.error('A connection error occurred')
            raise ConnectorError('A connection error occurred')
        except requests.exceptions.Timeout:
            logger.error('The request timed out')
            raise ConnectorError('The request timed out')
        except requests.exceptions.RequestException:
            logger.error('There was an error while handling the request')
            raise ConnectorError('There was an error while handling the request')
        except Exception as e:
            logger.error('{0}'.format(e))
            raise ConnectorError('{0}'.format(e))


def build_params(params):
    return {k: v for k, v in params.items() if v is not None and v != ''}


def build_query_param(param_name, param_value):
    return f'&{param_name}='.join([item.strip(" ") for item in param_value.split(',')])


def get_device_attributes(config, params):
    wg = ProgressWhatsUpGold(config)
    params = build_params(params)
    device_id = params.pop('device_id')
    if params.get('names') and ',' in params.get('names'):
        params['names'] = build_query_param('names', params.get('names'))
    endpoint = f'devices/{device_id}/attributes/-'
    resp = wg.make_rest_call(config, endpoint=endpoint, params=params)
    return resp


def get_device_groups(config, params):
    wg = ProgressWhatsUpGold(config)
    params = build_params(params)
    device_id = params.pop('device_id')
    if params.get('view'):
        params['view'] = params.get('view').lower()
    endpoint = f'devices/{device_id}/group/-'
    resp = wg.make_rest_call(config, endpoint=endpoint, params=params)
    return resp


def get_device_monitors(config, params):
    wg = ProgressWhatsUpGold(config)
    params = build_params(params)
    device_id = params.pop('device_id')
    endpoint = f'devices/{device_id}/monitors/-'
    resp = wg.make_rest_call(config, endpoint=endpoint, params=params)
    return resp


def get_device_polling_configuration(config, params):
    wg = ProgressWhatsUpGold(config)
    device_id = params.pop('device_id')
    endpoint = f'devices/{device_id}/config/polling'
    resp = wg.make_rest_call(config, endpoint=endpoint)
    return resp


def get_device_summary(config, params):
    wg = ProgressWhatsUpGold(config)
    device_id = params.pop('device_id')
    endpoint = f'devices/{device_id}/config/template'
    resp = wg.make_rest_call(config, endpoint=endpoint)
    return resp


def get_device_overview(config, params):
    wg = ProgressWhatsUpGold(config)
    device_id = params.pop('device_id')
    endpoint = f'devices/{device_id}'
    resp = wg.make_rest_call(config, endpoint=endpoint)
    return resp


def get_device_report(config, params):
    wg = ProgressWhatsUpGold(config)
    params = build_params(params)
    if params.get('range'):
        params['range'] = report_duration.get(params.get('range'))
    device_id = params.pop('device_id')
    endpoint = f"devices/{device_id}/reports/{endpoints.get(params.pop('report_type'))}"
    resp = wg.make_rest_call(config, endpoint=endpoint, params=params)
    return resp


def check_health_ex(config, connector_info):
    try:
        return check(config, connector_info)
    except Exception as err:
        raise ConnectorError(str(err))


operations = {
    'get_device_attributes': get_device_attributes,
    'get_device_groups': get_device_groups,
    'get_device_monitors': get_device_monitors,
    'get_device_polling_configuration': get_device_polling_configuration,
    'get_device_summary': get_device_summary,
    'get_device_overview': get_device_overview,
    'get_device_report': get_device_report,
    'check_health': check_health_ex
}

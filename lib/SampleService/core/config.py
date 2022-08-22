'''
Configuration parsing and creation for the sample service.
'''

# Because creating the samples instance involves contacting arango and the auth service,
# this code is mostly tested in the integration tests.

import importlib
from typing import Dict, Optional, List, Tuple
from typing import cast as _cast
import urllib.request as _request
from urllib.error import URLError as _URLError
import yaml as _yaml
from yaml.parser import ParserError as _ParserError
from jsonschema import validate as _validate
import arango as _arango
from github import Github as _Github

from SampleService.core.validator.metadata_validator import MetadataValidatorSet
from SampleService.core.validator.metadata_validator import MetadataValidator as _MetadataValidator
from SampleService.core.samples import Samples
from SampleService.core.storage.arango_sample_storage import ArangoSampleStorage \
    as _ArangoSampleStorage
from SampleService.core.arg_checkers import (
    check_string as _check_string,
    check_bool as _check_bool
)
from SampleService.core.notification import KafkaNotifier as _KafkaNotifer
from SampleService.core.user_lookup import KBaseUserLookup
from SampleService.core.workspace import WS as _WS
from SampleService.core.errors import MissingParameterError as _MissingParameterError

from installed_clients.WorkspaceClient import Workspace as _Workspace


def build_samples(config: Dict[str, str]) -> Tuple[Samples, KBaseUserLookup, List[str]]:
    '''
    Build the sample service instance from the SDK server provided parameters.

    :param cfg: The SDK generated configuration.
    :returns: A samples instance.
    '''
    if not config:
        raise ValueError('config is empty, cannot start service')
    arango_url = _check_string_req(config.get('arango-url'), 'config param arango-url')
    arango_db = _check_string_req(config.get('arango-db'), 'config param arango-db')
    arango_user = _check_string_req(config.get('arango-user'), 'config param arango-user')
    arango_pwd = _check_string_req(config.get('arango-pwd'), 'config param arango-pwd')

    col_sample = _check_string_req(config.get('sample-collection'),
                                   'config param sample-collection')
    col_version = _check_string_req(
        config.get('version-collection'), 'config param version-collection')
    col_ver_edge = _check_string_req(
        config.get('version-edge-collection'), 'config param version-edge-collection')
    col_node = _check_string_req(config.get('node-collection'), 'config param node-collection')
    col_node_edge = _check_string_req(
        config.get('node-edge-collection'), 'config param node-edge-collection')
    col_data_link = _check_string_req(
        config.get('data-link-collection'), 'config param data-link-collection')
    col_ws_obj_ver = _check_string_req(
        config.get('workspace-object-version-shadow-collection'),
        'config param workspace-object-version-shadow-collection')
    col_schema = _check_string_req(config.get('schema-collection'),
                                   'config param schema-collection')

    auth_root_url = _check_string_req(config.get('auth-root-url'), 'config param auth-root-url')
    auth_token = _check_string_req(config.get('auth-token'), 'config param auth-token')
    full_roles = split_value(config, 'auth-full-admin-roles')
    read_roles = split_value(config, 'auth-read-admin-roles')
    read_exempt_roles = split_value(config, 'auth-read-exempt-roles')

    ws_url = _check_string_req(config.get('workspace-url'), 'config param workspace-url')
    ws_token = _check_string_req(config.get('workspace-read-admin-token'),
                                 'config param workspace-read-admin-token')

    kafka_servers = _check_string(config.get('kafka-bootstrap-servers'),
                                  'config param kafka-bootstrap-servers',
                                  optional=True)
    kafka_topic = None
    if kafka_servers:  # have to start the server twice to test no kafka scenario
        kafka_topic = _check_string(config.get('kafka-topic'), 'config param kafka-topic')

    metaval_repo = _check_string(config.get('metadata-validator-config-repo'),
                                'config param metadata-validator-config-repo',
                                optional=True)
    
    metaval_filename = _check_string(config.get('metadata-validator-config-filename'),
                                'config param metadata-validator-config-filename',
                                optional=True)

    if metaval_repo and not metaval_filename:
        raise _MissingParameterError(metaval_filename)

    metaval_release_tag = _check_string(config.get('metadata-validator-config-release-tag'),
                                'config param metadata-validator-config-release-tag',
                                optional=True)
    
    metaval_prelease_ok = _check_bool(config.get('metadata-validator-config-prerelease'),
                                'config param metadata-validator-config-prerelease',
                                optional=True) or False

    metaval_url = _check_string(config.get('metadata-validator-config-url'),
                                'config param metadata-validator-config-url',
                                optional=True)

    github_token = _check_string(config.get('github-token'),
                                'config param github-token',
                                optional=True)

    # meta params may have info that shouldn't be logged so don't log any for now.
    # Add code to deal with this later if needed
    print(f'''
        Starting server with config:
            arango-url: {arango_url}
            arango-db: {arango_db}
            arango-user: {arango_user}
            arango-pwd: [REDACTED FOR YOUR SAFETY AND COMFORT]
            sample-collection: {col_sample}
            version-collection: {col_version}
            version-edge-collection: {col_ver_edge}
            node-collection: {col_node}
            node-edge-collection: {col_node_edge}
            data-link-collection: {col_data_link}
            workspace-object-version-shadow-collection: {col_ws_obj_ver}
            schema-collection: {col_schema}
            auth-root-url: {auth_root_url}
            auth-token: [REDACTED FOR YOUR CONVENIENCE AND ENJOYMENT]
            auth-full-admin-roles: {', '.join(full_roles)}
            auth-read-admin-roles: {', '.join(read_roles)}
            auth-read-exempt-roles: {', '.join(read_exempt_roles)}
            workspace-url: {ws_url}
            workspace-read-admin-token: [REDACTED FOR YOUR ULTIMATE PLEASURE]
            kafka-bootstrap-servers: {kafka_servers}
            kafka-topic: {kafka_topic}
            metadata-validator-config-repo: {metaval_repo}
            metadata-validator-config-filename: {metaval_filename}
            metadata-validator-config-prerelease: {metaval_prelease_ok}
            metadata-validator-config-release-tag: {metaval_release_tag}
            metadata-validator-config-url: {metaval_url}
            github-token: [REDACTED]
    ''')

    # build the validators before trying to connect to arango
    if (metaval_url or metaval_repo):
        metaval = get_validators(
            repo_path=metaval_repo,
            repo_asset=metaval_filename,
            tag=metaval_release_tag,
            prerelease_ok=metaval_prelease_ok,
            url=metaval_url,
            token=github_token
            )
    else:
        metaval = MetadataValidatorSet()

    arangoclient = _arango.ArangoClient(hosts=arango_url)
    arango_db = arangoclient.db(
        arango_db, username=arango_user, password=arango_pwd, verify=True)
    storage = _ArangoSampleStorage(
        arango_db,
        col_sample,
        col_version,
        col_ver_edge,
        col_node,
        col_node_edge,
        col_ws_obj_ver,
        col_data_link,
        col_schema,
    )
    storage.start_consistency_checker()
    kafka = _KafkaNotifer(kafka_servers, _cast(str, kafka_topic)) if kafka_servers else None
    user_lookup = KBaseUserLookup(auth_root_url, auth_token, full_roles, read_roles)
    ws = _WS(_Workspace(ws_url, token=ws_token))
    return Samples(storage, user_lookup, metaval, ws, kafka), user_lookup, read_exempt_roles


def split_value(d: Dict[str, str], key: str):
    '''
    Get a list of comma separated values given a string taken from a configuration dict.
    :param config: The configuration dict containing the string to be processed as a value.
    :param key: The key in the dict containing the value.
    :returns: a list of strings split from the source comma separated string, or an empty list
    if the key does not exist or contains only whitespace.
    :raises ValueError: if the value contains control characters.
    '''
    if d is None:
        raise ValueError('d cannot be None')
    rstr = _check_string(d.get(key), 'config param ' + key, optional=True)
    if not rstr:
        return []
    return [x.strip() for x in rstr.split(',') if x.strip()]


def _check_string_req(s: Optional[str], name: str) -> str:
    return _cast(str, _check_string(s, name))


# TODO may need a versioning scheme
# If this structure is updated, please update the README file.
_META_VAL_JSONSCHEMA = {
    'type': 'object',
    'definitions': {
        'validator_set': {
            'type': 'object',
            # validate values only
            'additionalProperties': {
                'type': 'object',
                'properties': {
                    'key_metadata': {
                        'type': 'object',
                        'additionalProperties': {
                            'type': ['array', 'object', 'number', 'boolean', 'string', 'null']
                        }
                    },
                    'validators': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'module': {'type': 'string'},
                                'callable_builder': {'type': 'string'},
                                'parameters': {'type': 'object'}
                            },
                            'additionalProperties': False,
                            'required': ['module', 'callable_builder']
                        }

                    }
                },
                'required': ['validators']
            }
        },
        'additionalProperties': False,
    },
    'properties': {
        'validators': {'$ref': '#/definitions/validator_set'},
        'prefix_validators': {'$ref': '#/definitions/validator_set'},
    },
    'additionalProperties': False
}


def get_validators(
    repo_path: Optional[str] = None, 
    repo_asset: Optional[str] = None, 
    tag: Optional[str] = None,
    prerelease_ok: bool = False, 
    url: Optional[str] = None, 
    token: Optional[str] = None
    ) -> MetadataValidatorSet:
    '''
    Given a github repo or url pointing to a config file, initialize any metadata 
    validators present in the configuration. repo_path or url must be specified.
    If a github repo is specified, pull config from the release asset repo_asset.

    :param repo_path: github repo path (i.e. kbase/sample_service_validator_config)
    :param repo_asset: release asset filename containing validator config
    :param tag: Tag specifying a specific release to load the config from (deafult is latest)
    :param prerelease_ok: If false, ignores pre-releases when pulling validators from github
    :param url: The URL for a config file for the metadata validators.
    :param token: The token to be used when querying github
    :returns: A set of metadata validators.
    '''
    # TODO VALIDATOR make validator CLI

    try:
        config_asset = None
        if url:
            config_url = url
        elif not repo_path:
            raise ValueError(f'No metadata validator config URL or repo path.')
        else:
            if not repo_asset:
                raise ValueError(f'No repo_asset name provided for repo "{repo_path}"')
            try: 
                repo = _Github(login_or_token=token).get_repo(repo_path)
                releases = [rel for rel in repo.get_releases() if prerelease_ok or not rel.prerelease]
            except Exception as e:
                raise RuntimeError(f'Fetching releases from repo "{repo_path}" failed.') from e

            if not releases:
                raise ValueError(f'No releases found in validator config repo "{repo_path}"')

            if tag:
                target_release = next((r for r in releases if r.tag_name==tag), None)
                if not target_release:
                    raise ValueError(f'No release with tag "{tag}" found in validator config repo "{repo_path}"')
            else:
                # Use the latest release
                target_release = releases[0]

            assets = target_release.get_assets()
            if not assets:
                raise ValueError(f'No assets found in validator config repo "{repo_path}", '+
                    f'release tag "{target_release.tag_name}"')

            config_asset = next((a for a in assets if a.name==repo_asset), None)
            if not config_asset:
                raise ValueError(f'No config asset "{repo_asset}" found in validator config '+
                    f'repo "{repo_path}", release tag "{target_release.tag_name}"')

            config_url = config_asset.url

        req = _request.Request(config_url)
        req.add_header('Accept', 'application/octet-stream')
        if token:
            req.add_header('Authorization', f'token {token}')
        with _request.urlopen(req) as response:
            cfg = _yaml.safe_load(response)

    except _URLError as e:
        if config_asset:
            raise ValueError(f'Error downloading config asset from repo "{repo_path}" '+
                f'tag "{tag}" asset "{config_asset.url}": {str(e.reason)}') from e
        else:
            raise ValueError(f'Error downloading config asset from {url}: {str(e.reason)}') from e
    except _ParserError as e:
        if config_asset:
            raise ValueError(
                f'Failed to open validator configuration file from repo "{repo_path}" '+
                    f'tag "{tag}" asset "{config_asset.url}": {str(e)}') from e
        else:
            raise ValueError(
                f'Failed to open validator configuration file from {url}: {str(e)}') from e

    _validate(instance=cfg, schema=_META_VAL_JSONSCHEMA)

    mvals = _get_validators(
        cfg.get('validators', {}),
        'Metadata',
        lambda k, v, m: _MetadataValidator(k, v, metadata=m))
    mvals.extend(_get_validators(
        cfg.get('prefix_validators', {}),
        'Prefix metadata',
        lambda k, v, m: _MetadataValidator(k, prefix_validators=v, metadata=m)))
    return MetadataValidatorSet(mvals)


def _get_validators(cfg, name_, metaval_func) -> List[_MetadataValidator]:
    mvals = []
    for key, keyval in cfg.items():
        meta = keyval.get('key_metadata')
        lvals = []
        for i, val in enumerate(keyval['validators']):
            m = importlib.import_module(val['module'])
            p = val.get('parameters', {})
            try:
                build_func = getattr(m, val['callable_builder'])
                lvals.append(build_func(p))
            except Exception as e:
                raise ValueError(
                    f'{name_} validator callable build #{i} failed for key {key}: {e.args[0]}'
                    ) from e
        mvals.append(metaval_func(key, lvals, meta))
    return mvals

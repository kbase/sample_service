import datetime
import uuid
import time

from pytest import raises, fixture
from core import test_utils
from core.test_utils import assert_exception_correct
from arango_controller import ArangoController
from SampleService.core.acls import SampleACL
from SampleService.core.data_link import DataLink
from SampleService.core.sample import SavedSample, SampleNode, SubSampleType, SampleNodeAddress
from SampleService.core.sample import SampleAddress
from SampleService.core.errors import MissingParameterError, NoSuchSampleError, ConcurrencyError
from SampleService.core.errors import NoSuchSampleVersionError, DataLinkExistsError
from SampleService.core.errors import TooManyDataLinksError, NoSuchLinkError
from SampleService.core.storage.arango_sample_storage import ArangoSampleStorage
from SampleService.core.storage.errors import SampleStorageError, StorageInitError
from SampleService.core.storage.errors import OwnerChangedError
from SampleService.core.user import UserID
from SampleService.core.workspace import UPA, DataUnitID

TEST_NODE = SampleNode('foo')

TEST_DB_NAME = 'test_sample_service'
TEST_COL_SAMPLE = 'samples'
TEST_COL_VERSION = 'versions'
TEST_COL_VER_EDGE = 'ver_to_sample'
TEST_COL_NODES = 'nodes'
TEST_COL_NODE_EDGE = 'node_edges'
TEST_COL_WS_OBJ_VER = 'ws_obj_ver'
TEST_COL_DATA_LINK = 'data_link'
TEST_COL_SCHEMA = 'schema'
TEST_USER = 'user1'
TEST_PWD = 'password1'


@fixture(scope='module')
def arango():
    arangoexe = test_utils.get_arango_exe()
    arangojs = test_utils.get_arango_js()
    tempdir = test_utils.get_temp_dir()
    arango = ArangoController(arangoexe, arangojs, tempdir)
    create_test_db(arango)
    print('running arango on port {} in dir {}'.format(arango.port, arango.temp_dir))
    yield arango
    del_temp = test_utils.get_delete_temp_files()
    print('shutting down arango, delete_temp_files={}'.format(del_temp))
    arango.destroy(del_temp)


def create_test_db(arango):
    systemdb = arango.client.db(verify=True)  # default access to _system db
    systemdb.create_database(TEST_DB_NAME, [{'username': TEST_USER, 'password': TEST_PWD}])
    return arango.client.db(TEST_DB_NAME, TEST_USER, TEST_PWD)


@fixture
def samplestorage(arango):
    return samplestorage_method(arango)


def clear_db_and_recreate(arango):
    arango.clear_database(TEST_DB_NAME, drop_indexes=True)
    db = create_test_db(arango)
    db.create_collection(TEST_COL_SAMPLE)
    db.create_collection(TEST_COL_VERSION)
    db.create_collection(TEST_COL_VER_EDGE, edge=True)
    db.create_collection(TEST_COL_NODES)
    db.create_collection(TEST_COL_NODE_EDGE, edge=True)
    db.create_collection(TEST_COL_WS_OBJ_VER)
    db.create_collection(TEST_COL_DATA_LINK, edge=True)
    db.create_collection(TEST_COL_SCHEMA)
    return db


def samplestorage_method(arango):
    clear_db_and_recreate(arango)
    return ArangoSampleStorage(
        arango.client.db(TEST_DB_NAME, TEST_USER, TEST_PWD),
        TEST_COL_SAMPLE,
        TEST_COL_VERSION,
        TEST_COL_VER_EDGE,
        TEST_COL_NODES,
        TEST_COL_NODE_EDGE,
        TEST_COL_WS_OBJ_VER,
        TEST_COL_DATA_LINK,
        TEST_COL_SCHEMA)


def nw():
    return datetime.datetime.fromtimestamp(1, tz=datetime.timezone.utc)


def test_startup_and_check_config_doc(samplestorage):
    # this is very naughty
    assert samplestorage._col_schema.count() == 1
    cfgdoc = samplestorage._col_schema.find({}).next()
    assert cfgdoc['_key'] == 'schema'
    assert cfgdoc['schemaver'] == 1
    assert cfgdoc['inupdate'] is False

    # check startup works with cfg object in place
    # this is also very naughty
    ss = ArangoSampleStorage(
        samplestorage._db,
        samplestorage._col_sample.name,
        samplestorage._col_version.name,
        samplestorage._col_ver_edge.name,
        samplestorage._col_nodes.name,
        samplestorage._col_node_edge.name,
        samplestorage._col_ws.name,
        samplestorage._col_data_link.name,
        samplestorage._col_schema.name)

    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    n = SampleNode('rootyroot')
    assert ss.save_sample(SavedSample(id_, UserID('u'), [n], dt(1), 'foo')) is True
    assert ss.get_sample(id_) == SavedSample(id_, UserID('u'), [n], dt(1), 'foo', version=1)


def test_startup_with_extra_config_doc(arango):
    db = clear_db_and_recreate(arango)

    scol = db.collection('schema')
    scol.insert_many([{'_key': 'schema', 'schemaver': 1, 'inupdate': False},
                      {'schema': 'schema', 'schemaver': 2, 'inupdate': False}])

    s = TEST_COL_SAMPLE
    v = TEST_COL_VERSION
    ve = TEST_COL_VER_EDGE
    n = TEST_COL_NODES
    ne = TEST_COL_NODE_EDGE
    ws = TEST_COL_WS_OBJ_VER
    dl = TEST_COL_DATA_LINK
    sc = TEST_COL_SCHEMA

    _fail_startup(db, s, v, ve, n, ne, ws, dl, sc, nw, StorageInitError(
        'Multiple config objects found ' +
        'in the database. This should not happen, something is very wrong.'))


def test_startup_with_bad_schema_version(arango):
    db = clear_db_and_recreate(arango)
    col = db.collection(TEST_COL_SCHEMA)
    col.insert({'_key': 'schema', 'schemaver': 4, 'inupdate': False})

    s = TEST_COL_SAMPLE
    v = TEST_COL_VERSION
    ve = TEST_COL_VER_EDGE
    n = TEST_COL_NODES
    ne = TEST_COL_NODE_EDGE
    ws = TEST_COL_WS_OBJ_VER
    dl = TEST_COL_DATA_LINK
    sc = TEST_COL_SCHEMA

    _fail_startup(db, s, v, ve, n, ne, ws, dl, sc, nw, StorageInitError(
        'Incompatible database schema. Server is v1, DB is v4'))


def test_startup_in_update(arango):
    db = clear_db_and_recreate(arango)
    col = db.collection(TEST_COL_SCHEMA)
    col.insert({'_key': 'schema', 'schemaver': 1, 'inupdate': True})

    s = TEST_COL_SAMPLE
    v = TEST_COL_VERSION
    ve = TEST_COL_VER_EDGE
    n = TEST_COL_NODES
    ne = TEST_COL_NODE_EDGE
    ws = TEST_COL_WS_OBJ_VER
    dl = TEST_COL_DATA_LINK
    sc = TEST_COL_SCHEMA

    _fail_startup(db, s, v, ve, n, ne, ws, dl, sc, nw, StorageInitError(
        'The database is in the middle of an update from v1 of the schema. Aborting startup.'))


def test_startup_with_unupdated_version_and_node_docs(samplestorage):
    # this test simulates a server coming up after a dirty shutdown, where version and
    # node doc integer versions have not been updated
    n1 = SampleNode('root')
    n2 = SampleNode('kid1', SubSampleType.TECHNICAL_REPLICATE, 'root')
    n3 = SampleNode('kid2', SubSampleType.SUB_SAMPLE, 'kid1')
    n4 = SampleNode('kid3', SubSampleType.TECHNICAL_REPLICATE, 'root')

    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')

    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [n1, n2, n3, n4], dt(1), 'foo')) is True

    # this is very naughty
    # checked that these modifications actually work by viewing the db contents
    samplestorage._col_version.update_match({}, {'ver': -1})
    samplestorage._col_nodes.update_match({'name': 'kid2'}, {'ver': -1})

    # this is also very naughty
    ArangoSampleStorage(
        samplestorage._db,
        samplestorage._col_sample.name,
        samplestorage._col_version.name,
        samplestorage._col_ver_edge.name,
        samplestorage._col_nodes.name,
        samplestorage._col_node_edge.name,
        samplestorage._col_ws.name,
        samplestorage._col_data_link.name,
        samplestorage._col_schema.name)

    assert samplestorage._col_version.count() == 1
    assert samplestorage._col_ver_edge.count() == 1
    assert samplestorage._col_nodes.count() == 4
    assert samplestorage._col_node_edge.count() == 4

    for v in samplestorage._col_version.all():
        assert v['ver'] == 1

    for v in samplestorage._col_nodes.all():
        assert v['ver'] == 1


def test_startup_with_unupdated_node_docs(samplestorage):
    # this test simulates a server coming up after a dirty shutdown, where
    # node doc integer versions have not been updated
    # version doc cannot be modified such that ver = -1 or the version check will also correct the
    # node docs, negating the point of this test
    n1 = SampleNode('root')
    n2 = SampleNode('kid1', SubSampleType.TECHNICAL_REPLICATE, 'root')
    n3 = SampleNode('kid2', SubSampleType.SUB_SAMPLE, 'kid1')
    n4 = SampleNode('kid3', SubSampleType.TECHNICAL_REPLICATE, 'root')

    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')

    assert samplestorage.save_sample(
        SavedSample(id_, UserID('u'), [n1, n2, n3, n4], dt(1), 'foo')) is True

    assert samplestorage.save_sample_version(
        SavedSample(id_, UserID('u'), [n1, n2, n3, n4], dt(1), 'bar')) == 2

    # this is very naughty
    sample = samplestorage._col_sample.find({}).next()
    uuidver2 = sample['vers'][1]

    # checked that these modifications actually work by viewing the db contents
    samplestorage._col_nodes.update_match({'uuidver': uuidver2, 'name': 'kid2'}, {'ver': -1})

    # this is also very naughty
    ArangoSampleStorage(
        samplestorage._db,
        samplestorage._col_sample.name,
        samplestorage._col_version.name,
        samplestorage._col_ver_edge.name,
        samplestorage._col_nodes.name,
        samplestorage._col_node_edge.name,
        samplestorage._col_ws.name,
        samplestorage._col_data_link.name,
        samplestorage._col_schema.name)

    assert samplestorage._col_version.count() == 2
    assert samplestorage._col_ver_edge.count() == 2
    assert samplestorage._col_nodes.count() == 8
    assert samplestorage._col_node_edge.count() == 8

    for v in samplestorage._col_version.all():
        assert v['ver'] == 2 if v['uuidver'] == uuidver2 else 1

    for v in samplestorage._col_nodes.all():
        assert v['ver'] == 2 if v['uuidver'] == uuidver2 else 1


def test_startup_with_no_sample_doc(samplestorage):
    # this test simulates a server coming up after a dirty shutdown, where version and
    # node docs were saved but the sample document was not while saving the first version of
    # a sample
    n1 = SampleNode('root')
    n2 = SampleNode('kid1', SubSampleType.TECHNICAL_REPLICATE, 'root')
    n3 = SampleNode('kid2', SubSampleType.SUB_SAMPLE, 'kid1')
    n4 = SampleNode('kid3', SubSampleType.TECHNICAL_REPLICATE, 'root')

    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    id2 = uuid.UUID('1234567890abcdef1234567890abcdea')

    assert samplestorage.save_sample(
        SavedSample(id1, UserID('u'), [n1, n2, n3, n4], dt(1), 'foo')) is True

    assert samplestorage.save_sample(
        SavedSample(id2, UserID('u'), [n1, n2, n3, n4], dt(1000), 'foo')) is True

    # this is very naughty
    assert samplestorage._col_version.count() == 2
    assert samplestorage._col_ver_edge.count() == 2
    assert samplestorage._col_nodes.count() == 8
    assert samplestorage._col_node_edge.count() == 8

    samplestorage._col_sample.delete({'_key': str(id2)})
    # if the sample document hasn't been saved, then none of the integer versions for the
    # sample can have been updated to 1
    samplestorage._col_version.update_match({'id': str(id2)}, {'ver': -1})
    samplestorage._col_nodes.update_match({'id': str(id2)}, {'ver': -1})

    # first test that bringing up the server before the 1hr deletion time limit doesn't change the
    # db:
    # this is also very naughty
    ArangoSampleStorage(
        samplestorage._db,
        samplestorage._col_sample.name,
        samplestorage._col_version.name,
        samplestorage._col_ver_edge.name,
        samplestorage._col_nodes.name,
        samplestorage._col_node_edge.name,
        samplestorage._col_ws.name,
        samplestorage._col_data_link.name,
        samplestorage._col_schema.name,
        now=lambda: datetime.datetime.fromtimestamp(4600, tz=datetime.timezone.utc))

    assert samplestorage._col_version.count() == 2
    assert samplestorage._col_ver_edge.count() == 2
    assert samplestorage._col_nodes.count() == 8
    assert samplestorage._col_node_edge.count() == 8

    # now test that bringing up the server after the limit deletes the docs:
    ArangoSampleStorage(
        samplestorage._db,
        samplestorage._col_sample.name,
        samplestorage._col_version.name,
        samplestorage._col_ver_edge.name,
        samplestorage._col_nodes.name,
        samplestorage._col_node_edge.name,
        samplestorage._col_ws.name,
        samplestorage._col_data_link.name,
        samplestorage._col_schema.name,
        now=lambda: datetime.datetime.fromtimestamp(4601, tz=datetime.timezone.utc))

    assert samplestorage._col_sample.count() == 1
    assert samplestorage._col_version.count() == 1
    assert samplestorage._col_ver_edge.count() == 1
    assert samplestorage._col_nodes.count() == 4
    assert samplestorage._col_node_edge.count() == 4

    sample = samplestorage._col_sample.find({}).next()
    assert sample['id'] == str(id1)
    uuidver = sample['vers'][0]

    assert len(list(samplestorage._col_version.find({'uuidver': uuidver}))) == 1
    assert len(list(samplestorage._col_ver_edge.find({'uuidver': uuidver}))) == 1
    assert len(list(samplestorage._col_nodes.find({'uuidver': uuidver}))) == 4
    assert len(list(samplestorage._col_node_edge.find({'uuidver': uuidver}))) == 4


def test_startup_with_no_version_in_sample_doc(samplestorage):
    # this test simulates a server coming up after a dirty shutdown, where version and
    # node docs were saved but the sample document was not updated while saving the second
    # version of # a sample
    n1 = SampleNode('root')
    n2 = SampleNode('kid1', SubSampleType.TECHNICAL_REPLICATE, 'root')
    n3 = SampleNode('kid2', SubSampleType.SUB_SAMPLE, 'kid1')
    n4 = SampleNode('kid3', SubSampleType.TECHNICAL_REPLICATE, 'root')

    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')

    assert samplestorage.save_sample(
        SavedSample(id1, UserID('u'), [n1, n2, n3, n4], dt(1), 'foo')) is True

    assert samplestorage.save_sample_version(
        SavedSample(id1, UserID('u'), [n1, n2, n3, n4], dt(2000), 'foo')) == 2

    # this is very naughty
    assert samplestorage._col_sample.count() == 1
    assert samplestorage._col_version.count() == 2
    assert samplestorage._col_ver_edge.count() == 2
    assert samplestorage._col_nodes.count() == 8
    assert samplestorage._col_node_edge.count() == 8

    sample = samplestorage._col_sample.find({}).next()
    samplestorage._col_sample.update_match({}, {'vers': sample['vers'][:1]})
    uuidver2 = sample['vers'][1]

    # if the sample document hasn't been updated, then none of the integer versions for the
    # sample can have been updated to 1
    samplestorage._col_version.update_match({'uuidver': uuidver2}, {'ver': -1})
    samplestorage._col_nodes.update_match({'uuidver': uuidver2}, {'ver': -1})

    # first test that bringing up the server before the 1hr deletion time limit doesn't change the
    # db:
    # this is also very naughty
    ArangoSampleStorage(
        samplestorage._db,
        samplestorage._col_sample.name,
        samplestorage._col_version.name,
        samplestorage._col_ver_edge.name,
        samplestorage._col_nodes.name,
        samplestorage._col_node_edge.name,
        samplestorage._col_ws.name,
        samplestorage._col_data_link.name,
        samplestorage._col_schema.name,
        now=lambda: datetime.datetime.fromtimestamp(5600, tz=datetime.timezone.utc))

    assert samplestorage._col_version.count() == 2
    assert samplestorage._col_ver_edge.count() == 2
    assert samplestorage._col_nodes.count() == 8
    assert samplestorage._col_node_edge.count() == 8

    # now test that bringing up the server after the limit deletes the docs:
    ArangoSampleStorage(
        samplestorage._db,
        samplestorage._col_sample.name,
        samplestorage._col_version.name,
        samplestorage._col_ver_edge.name,
        samplestorage._col_nodes.name,
        samplestorage._col_node_edge.name,
        samplestorage._col_ws.name,
        samplestorage._col_data_link.name,
        samplestorage._col_schema.name,
        now=lambda: datetime.datetime.fromtimestamp(5601, tz=datetime.timezone.utc))

    assert samplestorage._col_version.count() == 1
    assert samplestorage._col_ver_edge.count() == 1
    assert samplestorage._col_nodes.count() == 4
    assert samplestorage._col_node_edge.count() == 4

    uuidver1 = sample['vers'][0]

    assert len(list(samplestorage._col_version.find({'uuidver': uuidver1}))) == 1
    assert len(list(samplestorage._col_ver_edge.find({'uuidver': uuidver1}))) == 1
    assert len(list(samplestorage._col_nodes.find({'uuidver': uuidver1}))) == 4
    assert len(list(samplestorage._col_node_edge.find({'uuidver': uuidver1}))) == 4


def test_fail_startup_bad_args(arango):
    samplestorage_method(arango)
    db = arango.client.db(TEST_DB_NAME, TEST_USER, TEST_PWD)

    s = TEST_COL_SAMPLE
    v = TEST_COL_VERSION
    ve = TEST_COL_VER_EDGE
    n = TEST_COL_NODES
    ne = TEST_COL_NODE_EDGE
    ws = TEST_COL_WS_OBJ_VER
    dl = TEST_COL_DATA_LINK
    sc = TEST_COL_SCHEMA

    def nw():
        datetime.datetime.fromtimestamp(1, tz=datetime.timezone.utc)

    _fail_startup(None, s, v, ve, n, ne, ws, dl, sc, nw,
                  ValueError('db cannot be a value that evaluates to false'))
    _fail_startup(db, '', v, ve, n, ne, ws, dl, sc, nw, MissingParameterError('sample_collection'))
    _fail_startup(db, s, '', ve, n, ne, ws, dl, sc, nw, MissingParameterError(
        'version_collection'))
    _fail_startup(db, s, v, '', n, ne, ws, dl, sc, nw, MissingParameterError(
        'version_edge_collection'))
    _fail_startup(db, s, v, ve, '', ne, ws, dl, sc, nw, MissingParameterError('node_collection'))
    _fail_startup(db, s, v, ve, n, '', ws, dl, sc, nw, MissingParameterError(
        'node_edge_collection'))
    _fail_startup(db, s, v, ve, n, ne, '', dl, sc, nw, MissingParameterError(
        'workspace_object_version_shadow_collection'))
    _fail_startup(db, s, v, ve, n, ne, ws, '', sc, nw, MissingParameterError(
        'data_link_collection'))
    _fail_startup(db, s, v, ve, n, ne, ws, dl, '', nw, MissingParameterError('schema_collection'))
    _fail_startup(db, s, v, ve, n, ne, ws, dl, sc, None,
                  ValueError('now cannot be a value that evaluates to false'))


def test_fail_startup_incorrect_collection_type(arango):
    samplestorage_method(arango)
    db = arango.client.db(TEST_DB_NAME, TEST_USER, TEST_PWD)
    db.create_collection('sampleedge', edge=True)

    s = TEST_COL_SAMPLE
    v = TEST_COL_VERSION
    ve = TEST_COL_VER_EDGE
    n = TEST_COL_NODES
    ne = TEST_COL_NODE_EDGE
    ws = TEST_COL_WS_OBJ_VER
    dl = TEST_COL_DATA_LINK
    sc = TEST_COL_SCHEMA

    def nw():
        datetime.datetime.fromtimestamp(1, tz=datetime.timezone.utc)

    _fail_startup(db, 'sampleedge', v, ve, n, ne, ws, dl, sc, nw, StorageInitError(
        'sample collection sampleedge is not a vertex collection'))
    _fail_startup(db, s, ve, ve, n, ne, ws, dl, sc, nw, StorageInitError(
        'version collection ver_to_sample is not a vertex collection'))
    _fail_startup(db, s, v, v, n, ne, ws, dl, sc, nw, StorageInitError(
        'version edge collection versions is not an edge collection'))
    _fail_startup(db, s, v, ve, ne, ne, ws, dl, sc, nw, StorageInitError(
        'node collection node_edges is not a vertex collection'))
    _fail_startup(db, s, v, ve, n, n, ws, dl, sc, nw, StorageInitError(
        'node edge collection nodes is not an edge collection'))
    _fail_startup(db, s, v, ve, n, ne, dl, dl, sc, nw, StorageInitError(
        'workspace object version shadow collection data_link is not a vertex collection'))
    _fail_startup(db, s, v, ve, n, ne, ws, ws, sc, nw, StorageInitError(
        'data link collection ws_obj_ver is not an edge collection'))
    _fail_startup(db, s, v, ve, n, ne, ws, dl, ne, nw, StorageInitError(
        'schema collection node_edges is not a vertex collection'))


def _fail_startup(
        db,
        colsample,
        colver,
        colveredge,
        colnode,
        colnodeedge,
        colws,
        coldatalink,
        colschema,
        now,
        expected):

    with raises(Exception) as got:
        ArangoSampleStorage(
            db,
            colsample,
            colver,
            colveredge,
            colnode,
            colnodeedge,
            colws,
            coldatalink,
            colschema,
            now=now)
    assert_exception_correct(got.value, expected)


def test_indexes_created(samplestorage):
    # Shoudn't reach into the internals but only testing
    # Purpose here is to make tests fail if collections are added so devs are reminded to
    # set up any necessary indexes and add index tests
    cols = sorted([x['name'] for x in samplestorage._db.collections()
                   if not x['name'].startswith('_')])
    assert cols == [
        'data_link',
        'node_edges',
        'nodes',
        'samples',
        'schema',
        'ver_to_sample',
        'versions',
        'ws_obj_ver']

    indexes = samplestorage._col_sample.indexes()
    assert len(indexes) == 1
    assert indexes[0]['fields'] == ['_key']

    indexes = samplestorage._col_nodes.indexes()
    assert len(indexes) == 3
    assert indexes[0]['fields'] == ['_key']
    _check_index(indexes[1], ['uuidver'])
    _check_index(indexes[2], ['ver'])

    indexes = samplestorage._col_version.indexes()
    assert len(indexes) == 3
    assert indexes[0]['fields'] == ['_key']
    _check_index(indexes[1], ['uuidver'])
    _check_index(indexes[2], ['ver'])

    indexes = samplestorage._col_node_edge.indexes()
    assert len(indexes) == 3
    assert indexes[0]['fields'] == ['_key']
    assert indexes[1]['fields'] == ['_from', '_to']
    _check_index(indexes[2], ['uuidver'])

    indexes = samplestorage._col_ver_edge.indexes()
    assert len(indexes) == 3
    assert indexes[0]['fields'] == ['_key']
    assert indexes[1]['fields'] == ['_from', '_to']
    _check_index(indexes[2], ['uuidver'])

    # Don't add indexes here, Relation engine is responsible for setting up indexes
    # Sample service doesn't use the collection other than verifying it exists
    indexes = samplestorage._col_ws.indexes()
    assert len(indexes) == 1
    assert indexes[0]['fields'] == ['_key']

    indexes = samplestorage._col_data_link.indexes()
    assert len(indexes) == 5
    assert indexes[0]['fields'] == ['_key']
    assert indexes[1]['fields'] == ['_from', '_to']
    _check_index(indexes[2], ['id'])
    _check_index(indexes[3], ['wsid', 'objid', 'objver'])
    _check_index(indexes[4], ['samuuidver'])

    indexes = samplestorage._col_schema.indexes()
    assert len(indexes) == 1
    assert indexes[0]['fields'] == ['_key']


def _check_index(index, fields):
    assert index['fields'] == fields
    assert index['deduplicate'] is True
    assert index['sparse'] is False
    assert index['type'] == 'persistent'
    assert index['unique'] is False


def test_start_consistency_checker_fail_bad_args(samplestorage):
    with raises(Exception) as got:
        samplestorage.start_consistency_checker(interval_sec=0)
    assert_exception_correct(got.value, ValueError('interval_sec must be > 0'))


def test_consistency_checker_run(samplestorage):
    # here we just test that stopping and starting the checker will clean up the db.
    # The cleaning functionality is tested thoroughly above.
    # The db could be in an unclean state if a sample server does down mid save and doesn't
    # come back up.
    n1 = SampleNode('root')
    n2 = SampleNode('kid1', SubSampleType.TECHNICAL_REPLICATE, 'root')
    n3 = SampleNode('kid2', SubSampleType.SUB_SAMPLE, 'kid1')
    n4 = SampleNode('kid3', SubSampleType.TECHNICAL_REPLICATE, 'root')

    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')

    assert samplestorage.save_sample(
        SavedSample(id_, UserID('u'), [n1, n2, n3, n4], dt(1), 'foo')) is True

    assert samplestorage.save_sample_version(
        SavedSample(id_, UserID('u'), [n1, n2, n3, n4], dt(1), 'bar')) == 2

    # this is very naughty
    sample = samplestorage._col_sample.find({}).next()
    uuidver2 = sample['vers'][1]

    samplestorage._col_nodes.update_match({'uuidver': uuidver2, 'name': 'kid2'}, {'ver': -1})

    samplestorage.start_consistency_checker(interval_sec=1)
    samplestorage.start_consistency_checker(interval_sec=1)  # test that running twice does nothing

    time.sleep(0.5)

    assert samplestorage._col_nodes.find({'uuidver': uuidver2, 'name': 'kid2'}).next()['ver'] == -1

    time.sleep(1)

    assert samplestorage._col_version.count() == 2
    assert samplestorage._col_ver_edge.count() == 2
    assert samplestorage._col_nodes.count() == 8
    assert samplestorage._col_node_edge.count() == 8

    for v in samplestorage._col_version.all():
        assert v['ver'] == 2 if v['uuidver'] == uuidver2 else 1

    for v in samplestorage._col_nodes.all():
        assert v['ver'] == 2 if v['uuidver'] == uuidver2 else 1

    # test that pausing stops updating
    samplestorage.stop_consistency_checker()
    samplestorage.stop_consistency_checker()  # test that running twice in a row does nothing

    samplestorage._col_nodes.update_match({'uuidver': uuidver2, 'name': 'kid2'}, {'ver': -1})

    time.sleep(1.5)
    assert samplestorage._col_nodes.find({'uuidver': uuidver2, 'name': 'kid2'}).next()['ver'] == -1

    samplestorage.start_consistency_checker(1)

    time.sleep(1.5)

    assert samplestorage._col_nodes.find({'uuidver': uuidver2, 'name': 'kid2'}).next()['ver'] == 2

    # leaving the checker running can occasionally interfere with other tests, deleting documents
    # that are in the middle of the save process. Stop the checker and wait until the job must've
    # run.
    samplestorage.stop_consistency_checker()
    time.sleep(1)


def dt(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)


def test_save_and_get_sample(samplestorage):
    n1 = SampleNode('root')
    n2 = SampleNode(
        'kid1', SubSampleType.TECHNICAL_REPLICATE, 'root',
        {'a': {'b': 'c', 'd': 'e'}, 'f': {'g': 'h'}},
        {'m': {'n': 'o'}})
    n3 = SampleNode('kid2', SubSampleType.SUB_SAMPLE, 'kid1', {'a': {'b': 'c'}})
    n4 = SampleNode('kid3', SubSampleType.TECHNICAL_REPLICATE, 'root',
                    user_metadata={'f': {'g': 'h'}})

    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')

    assert samplestorage.save_sample(
        SavedSample(id_, UserID('auser'), [n1, n2, n3, n4], dt(8), 'foo')) is True

    assert samplestorage.get_sample(id_) == SavedSample(
        id_, UserID('auser'), [n1, n2, n3, n4], dt(8), 'foo', 1)

    assert samplestorage.get_sample_acls(id_) == SampleACL(UserID('auser'))


def test_save_sample_fail_bad_input(samplestorage):
    with raises(Exception) as got:
        samplestorage.save_sample(None)
    assert_exception_correct(
        got.value, ValueError('sample cannot be a value that evaluates to false'))


def test_save_sample_fail_duplicate(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user1'), [TEST_NODE], dt(1), 'foo')) is True

    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user1'), [TEST_NODE], dt(1), 'bar')) is False


def test_save_sample_fail_duplicate_race_condition(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True

    # this is a very bad and naughty thing to do
    assert samplestorage._save_sample_pt2(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'bar')) is False


def test_get_sample_with_non_updated_version_doc(samplestorage):
    # simulates the case where a save failed part way through. The version UUID was added to the
    # sample doc but the node and version doc updates were not completed
    n1 = SampleNode('root')
    n2 = SampleNode('kid1', SubSampleType.TECHNICAL_REPLICATE, 'root')
    n3 = SampleNode('kid2', SubSampleType.SUB_SAMPLE, 'kid1')
    n4 = SampleNode('kid3', SubSampleType.TECHNICAL_REPLICATE, 'root')

    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')

    assert samplestorage.save_sample(
        SavedSample(id_, UserID('auser'), [n1, n2, n3, n4], dt(1), 'foo')) is True

    # this is very naughty
    # checked that these modifications actually work by viewing the db contents
    samplestorage._col_version.update_match({}, {'ver': -1})
    samplestorage._col_nodes.update_match({'name': 'kid2'}, {'ver': -1})

    assert samplestorage.get_sample(id_) == SavedSample(
        id_, UserID('auser'), [n1, n2, n3, n4], dt(1), 'foo', 1)

    for v in samplestorage._col_version.all():
        assert v['ver'] == 1

    for v in samplestorage._col_nodes.all():
        assert v['ver'] == 1


def test_get_sample_with_non_updated_node_doc(samplestorage):
    # simulates the case where a save failed part way through. The version UUID was added to the
    # sample doc but the node doc updates were not completed
    # the version doc update *must* have been updated for this test to exercise the
    # node checking logic because a non-updated version doc will cause the nodes to be updated
    # immediately.
    n1 = SampleNode('root')
    n2 = SampleNode('kid1', SubSampleType.TECHNICAL_REPLICATE, 'root')
    n3 = SampleNode('kid2', SubSampleType.SUB_SAMPLE, 'kid1')
    n4 = SampleNode('kid3', SubSampleType.TECHNICAL_REPLICATE, 'root')

    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')

    assert samplestorage.save_sample(
        SavedSample(id_, UserID('auser'), [n1, n2, n3, n4], dt(1), 'foo')) is True

    # this is very naughty
    # checked that these modifications actually work by viewing the db contents
    samplestorage._col_nodes.update_match({'name': 'kid1'}, {'ver': -1})

    assert samplestorage.get_sample(id_) == SavedSample(
        id_, UserID('auser'), [n1, n2, n3, n4], dt(1), 'foo', 1)

    for v in samplestorage._col_nodes.all():
        assert v['ver'] == 1


def test_get_sample_fail_bad_input(samplestorage):
    with raises(Exception) as got:
        samplestorage.get_sample(None)
    assert_exception_correct(
        got.value, ValueError('id_ cannot be a value that evaluates to false'))


def test_get_sample_fail_no_sample(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True

    with raises(Exception) as got:
        samplestorage.get_sample(uuid.UUID('1234567890abcdef1234567890abcdea'))
    assert_exception_correct(
        got.value, NoSuchSampleError('12345678-90ab-cdef-1234-567890abcdea'))


def test_get_sample_fail_no_such_version(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True

    with raises(Exception) as got:
        samplestorage.get_sample(uuid.UUID('1234567890abcdef1234567890abcdef'), version=2)
    assert_exception_correct(
        got.value, NoSuchSampleVersionError('12345678-90ab-cdef-1234-567890abcdef ver 2'))

    assert samplestorage.save_sample_version(
        SavedSample(id_, UserID('user2'), [TEST_NODE], dt(1), 'bar')) == 2

    assert samplestorage.get_sample(id_) == SavedSample(
        id_, UserID('user2'), [TEST_NODE], dt(1), 'bar', 2)

    with raises(Exception) as got:
        samplestorage.get_sample(uuid.UUID('1234567890abcdef1234567890abcdef'), version=3)
    assert_exception_correct(
        got.value, NoSuchSampleVersionError('12345678-90ab-cdef-1234-567890abcdef ver 3'))


def test_get_sample_fail_no_version_doc_1_version(samplestorage):
    # This should be impossible in practice unless someone actively deletes records from the db.
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True

    # this is very naughty
    verdoc_filters = {'id': '12345678-90ab-cdef-1234-567890abcdef', 'ver': 1}
    verdoc = samplestorage._col_version.find(verdoc_filters).next()
    samplestorage._col_version.delete_match(verdoc_filters)

    with raises(Exception) as got:
        samplestorage.get_sample(uuid.UUID('1234567890abcdef1234567890abcdef'), version=1)
    assert_exception_correct(
        got.value, SampleStorageError(f'Corrupt DB: Missing version {verdoc["uuidver"]} ' +
                                      'for sample 12345678-90ab-cdef-1234-567890abcdef'))


def test_get_sample_fail_no_version_doc_2_versions(samplestorage):
    # This should be impossible in practice unless someone actively deletes records from the db.
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True
    assert samplestorage.save_sample_version(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'bar')) == 2

    # this is very naughty
    verdoc_filters = {'id': '12345678-90ab-cdef-1234-567890abcdef', 'ver': 2}
    verdoc = samplestorage._col_version.find(verdoc_filters).next()
    samplestorage._col_version.delete_match(verdoc_filters)

    assert samplestorage.get_sample(id_, version=1) == SavedSample(
        id_, UserID('user'), [TEST_NODE], dt(1), 'foo', 1)

    with raises(Exception) as got:
        samplestorage.get_sample(uuid.UUID('1234567890abcdef1234567890abcdef'), version=2)
    assert_exception_correct(
        got.value, SampleStorageError(f'Corrupt DB: Missing version {verdoc["uuidver"]} ' +
                                      'for sample 12345678-90ab-cdef-1234-567890abcdef'))


def test_get_sample_fail_no_node_docs_1_version(samplestorage):
    # This should be impossible in practice unless someone actively deletes records from the db.
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True

    # this is very naughty
    nodedoc_filters = {'id': '12345678-90ab-cdef-1234-567890abcdef', 'ver': 1}
    nodedoc = samplestorage._col_nodes.find(nodedoc_filters).next()
    samplestorage._col_nodes.delete_match(nodedoc_filters)

    with raises(Exception) as got:
        samplestorage.get_sample(uuid.UUID('1234567890abcdef1234567890abcdef'), version=1)
    assert_exception_correct(
        got.value, SampleStorageError(
            f'Corrupt DB: Missing nodes for version {nodedoc["uuidver"]} of sample ' +
            '12345678-90ab-cdef-1234-567890abcdef'))


def test_get_sample_fail_no_node_docs_2_versions(samplestorage):
    # This should be impossible in practice unless someone actively deletes records from the db.
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True
    assert samplestorage.save_sample_version(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'bar')) == 2

    # this is very naughty
    nodedoc_filters = {'id': '12345678-90ab-cdef-1234-567890abcdef', 'ver': 2}
    nodedoc = samplestorage._col_nodes.find(nodedoc_filters).next()
    samplestorage._col_nodes.delete_match(nodedoc_filters)

    assert samplestorage.get_sample(id_, version=1) == SavedSample(
        id_, UserID('user'), [TEST_NODE], dt(1), 'foo', 1)

    with raises(Exception) as got:
        samplestorage.get_sample(uuid.UUID('1234567890abcdef1234567890abcdef'), version=2)
    assert_exception_correct(
        got.value, SampleStorageError(
            f'Corrupt DB: Missing nodes for version {nodedoc["uuidver"]} of sample ' +
            '12345678-90ab-cdef-1234-567890abcdef'))


def test_save_and_get_sample_version(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(42), 'foo')) is True

    n1 = SampleNode('root')
    n2 = SampleNode(
        'kid1', SubSampleType.TECHNICAL_REPLICATE, 'root',
        {'a': {'b': 'c', 'd': 'e'}, 'f': {'g': 'h'}},
        {'m': {'n': 'o'}})
    n3 = SampleNode('kid2', SubSampleType.SUB_SAMPLE, 'kid1', {'a': {'b': 'c'}})
    n4 = SampleNode('kid3', SubSampleType.TECHNICAL_REPLICATE, 'root',
                    user_metadata={'f': {'g': 'h'}})

    assert samplestorage.save_sample_version(
        SavedSample(id_, UserID('user2'), [n1, n2, n3, n4], dt(86), 'bar')) == 2
    assert samplestorage.save_sample_version(
        SavedSample(id_, UserID('user3'), [n1], dt(7), 'whiz', version=6)) == 3

    assert samplestorage.get_sample(id_, version=1) == SavedSample(
        id_, UserID('user'), [TEST_NODE], dt(42), 'foo', 1)

    assert samplestorage.get_sample(id_, version=2) == SavedSample(
        id_, UserID('user2'), [n1, n2, n3, n4], dt(86), 'bar', 2)

    expected = SavedSample(id_, UserID('user3'), [n1], dt(7), 'whiz', 3)
    assert samplestorage.get_sample(id_) == expected
    assert samplestorage.get_sample(id_, version=3) == expected


def test_save_sample_version_fail_bad_input(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    s = SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')

    _save_sample_version_fail(samplestorage, None, None, ValueError(
        'sample cannot be a value that evaluates to false'))
    _save_sample_version_fail(samplestorage, s, 0, ValueError(
        'prior_version must be > 0'))


def _save_sample_version_fail(samplestorage, sample, prior_version, expected):
    with raises(Exception) as got:
        samplestorage.save_sample_version(sample, prior_version)
    assert_exception_correct(got.value, expected)


def test_save_sample_version_fail_no_sample(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True

    id2 = uuid.UUID('1234567890abcdef1234567890abcdea')
    with raises(Exception) as got:
        samplestorage.save_sample_version(
            SavedSample(id2, UserID('user'), [TEST_NODE], dt(1), 'whiz'))
    assert_exception_correct(got.value, NoSuchSampleError('12345678-90ab-cdef-1234-567890abcdea'))


def test_save_sample_version_fail_prior_version(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True
    assert samplestorage.save_sample_version(
        SavedSample(id_, UserID('user'), [SampleNode('bat')], dt(1), 'bar')) == 2

    with raises(Exception) as got:
        samplestorage.save_sample_version(
            SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'whiz'), prior_version=1)
    assert_exception_correct(got.value, ConcurrencyError(
        'Version required for sample ' +
        '12345678-90ab-cdef-1234-567890abcdef is 1, but current version is 2'))

    # this is naughty, but need to check race condition
    with raises(Exception) as got:
        samplestorage._save_sample_version_pt2(
            SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'whiz'), 1)
    assert_exception_correct(got.value, ConcurrencyError(
        'Version required for sample ' +
        '12345678-90ab-cdef-1234-567890abcdef is 1, but current version is 2'))


def test_sample_version_update(samplestorage):
    # tests that the versions on node and version documents are updated correctly
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [SampleNode('baz')], dt(1), 'foo')) is True

    assert samplestorage.save_sample_version(
        SavedSample(id_, UserID('user'), [SampleNode('bat')], dt(1), 'bar')) == 2

    assert samplestorage.get_sample(id_, version=1) == SavedSample(
        id_, UserID('user'), [SampleNode('baz')], dt(1), 'foo', 1)

    assert samplestorage.get_sample(id_) == SavedSample(
        id_, UserID('user'), [SampleNode('bat')], dt(1), 'bar', 2)

    idstr = '12345678-90ab-cdef-1234-567890abcdef'
    vers = set()
    # this is naughty
    for n in samplestorage._col_version.find({'id': idstr}):
        vers.add((n['name'], n['ver']))
    assert vers == {('foo', 1), ('bar', 2)}

    nodes = set()
    # this is naughty
    for n in samplestorage._col_nodes.find({'id': idstr}):
        nodes.add((n['name'], n['ver']))
    assert nodes == {('baz', 1), ('bat', 2)}


def test_get_sample_acls_fail_bad_input(samplestorage):
    with raises(Exception) as got:
        samplestorage.get_sample_acls(None)
    assert_exception_correct(
        got.value, ValueError('id_ cannot be a value that evaluates to false'))


def test_get_sample_acls_fail_no_sample(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True

    with raises(Exception) as got:
        samplestorage.get_sample_acls(uuid.UUID('1234567890abcdef1234567890abcdea'))
    assert_exception_correct(
        got.value, NoSuchSampleError('12345678-90ab-cdef-1234-567890abcdea'))


def test_replace_sample_acls(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True

    samplestorage.replace_sample_acls(id_, SampleACL(
        UserID('user'),
        [UserID('foo'), UserID('bar')],
        [UserID('baz'), UserID('bat')],
        [UserID('whoo')]))

    assert samplestorage.get_sample_acls(id_) == SampleACL(
        UserID('user'),
        [UserID('foo'), UserID('bar')],
        [UserID('baz'), UserID('bat')],
        [UserID('whoo')])

    samplestorage.replace_sample_acls(id_, SampleACL(UserID('user'), write=[UserID('baz')]))

    assert samplestorage.get_sample_acls(id_) == SampleACL(UserID('user'), write=[UserID('baz')])


def test_replace_sample_acls_fail_bad_args(samplestorage):
    with raises(Exception) as got:
        samplestorage.replace_sample_acls(None, SampleACL(UserID('user')))
    assert_exception_correct(got.value, ValueError(
        'id_ cannot be a value that evaluates to false'))

    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    with raises(Exception) as got:
        samplestorage.replace_sample_acls(id_, None)
    assert_exception_correct(got.value, ValueError(
        'acls cannot be a value that evaluates to false'))


def test_replace_sample_acls_fail_no_sample(samplestorage):
    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id1, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True

    id2 = uuid.UUID('1234567890abcdef1234567890abcdea')

    with raises(Exception) as got:
        samplestorage.replace_sample_acls(id2, SampleACL(UserID('user')))
    assert_exception_correct(got.value, NoSuchSampleError(str(id2)))


def test_replace_sample_acls_fail_owner_changed(samplestorage):
    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [TEST_NODE], dt(1), 'foo')) is True

    # this is naughty
    samplestorage._db.aql.execute(
        '''
        FOR s IN @@col
            UPDATE s WITH {acls: MERGE(s.acls, @acls)} IN @@col
            RETURN s
        ''',
        bind_vars={'@col': 'samples', 'acls': {'owner': 'user2'}})

    with raises(Exception) as got:
        samplestorage.replace_sample_acls(id_, SampleACL(UserID('user'), write=[UserID('foo')]))
    assert_exception_correct(got.value, OwnerChangedError())


def test_create_and_get_data_link(samplestorage):
    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    id2 = uuid.UUID('1234567890abcdef1234567890abcdee')
    assert samplestorage.save_sample(
        SavedSample(id1, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True
    assert samplestorage.save_sample_version(
        SavedSample(id1, UserID('user'), [SampleNode('mynode1')], dt(2), 'foo')) == 2
    assert samplestorage.save_sample(
        SavedSample(id2, UserID('user'), [SampleNode('mynode2')], dt(3), 'foo')) is True

    samplestorage.create_data_link(DataLink(
        uuid.UUID('1234567890abcdef1234567890abcde1'),
        DataUnitID(UPA('5/89/32')),
        SampleNodeAddress(SampleAddress(id1, 2), 'mynode1'),
        dt(500),
        UserID('usera'))
    )

    # test different workspace object and different sample version
    samplestorage.create_data_link(DataLink(
        uuid.UUID('1234567890abcdef1234567890abcde2'),
        DataUnitID(UPA('42/42/42'), 'dataunit1'),
        SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
        dt(600),
        UserID('userb'))
    )

    # test data unit vs just UPA, different sample, and expiration date
    samplestorage.create_data_link(DataLink(
        uuid.UUID('1234567890abcdef1234567890abcde3'),
        DataUnitID(UPA('5/89/32'), 'dataunit2'),
        SampleNodeAddress(SampleAddress(id2, 1), 'mynode2'),
        dt(700),
        UserID('u'))
    )

    # test data units don't collide if they have different names
    samplestorage.create_data_link(DataLink(
        uuid.UUID('1234567890abcdef1234567890abcde4'),
        DataUnitID(UPA('5/89/32'), 'dataunit1'),
        SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
        dt(800),
        UserID('userd'))
    )

    # this is naughty
    verdoc1 = samplestorage._col_version.find({'id': str(id1), 'ver': 1}).next()
    verdoc2 = samplestorage._col_version.find({'id': str(id1), 'ver': 2}).next()
    verdoc3 = samplestorage._col_version.find({'id': str(id2), 'ver': 1}).next()
    nodedoc1 = samplestorage._col_nodes.find({'name': 'mynode'}).next()
    nodedoc2 = samplestorage._col_nodes.find({'name': 'mynode1'}).next()
    nodedoc3 = samplestorage._col_nodes.find({'name': 'mynode2'}).next()

    assert samplestorage._col_data_link.count() == 4

    # check arango documents correct, particularly _* values
    link1 = samplestorage._col_data_link.get('5_89_32')
    assert link1 == {
        '_key': '5_89_32',
        '_id': 'data_link/5_89_32',
        '_from': 'ws_obj_ver/5:89:32',
        '_to': nodedoc2['_id'],
        '_rev': link1['_rev'],  # no need to test this
        'id': '12345678-90ab-cdef-1234-567890abcde1',
        'wsid': 5,
        'objid': 89,
        'objver': 32,
        'dataid': None,
        'sampleid': '12345678-90ab-cdef-1234-567890abcdef',
        'samuuidver': verdoc2['uuidver'],
        'samintver': 2,
        'node': 'mynode1',
        'created': 500,
        'createby': 'usera',
        'expired': 9007199254740991,
        'expireby': None
    }

    link2 = samplestorage._col_data_link.get('42_42_42_bc7324de86d54718dd0dc29c55c6d53a')
    assert link2 == {
        '_key': '42_42_42_bc7324de86d54718dd0dc29c55c6d53a',
        '_id': 'data_link/42_42_42_bc7324de86d54718dd0dc29c55c6d53a',
        '_from': 'ws_obj_ver/42:42:42',
        '_to': nodedoc1['_id'],
        '_rev': link2['_rev'],  # no need to test this
        'id': '12345678-90ab-cdef-1234-567890abcde2',
        'wsid': 42,
        'objid': 42,
        'objver': 42,
        'dataid': 'dataunit1',
        'sampleid': '12345678-90ab-cdef-1234-567890abcdef',
        'samuuidver': verdoc1['uuidver'],
        'samintver': 1,
        'node': 'mynode',
        'created': 600,
        'createby': 'userb',
        'expired': 9007199254740991,
        'expireby': None
    }

    link3 = samplestorage._col_data_link.get('5_89_32_3735ce9bbe59e7ec245da484772f9524')
    assert link3 == {
        '_key': '5_89_32_3735ce9bbe59e7ec245da484772f9524',
        '_id': 'data_link/5_89_32_3735ce9bbe59e7ec245da484772f9524',
        '_from': 'ws_obj_ver/5:89:32',
        '_to': nodedoc3['_id'],
        '_rev': link3['_rev'],  # no need to test this
        'id': '12345678-90ab-cdef-1234-567890abcde3',
        'wsid': 5,
        'objid': 89,
        'objver': 32,
        'dataid': 'dataunit2',
        'sampleid': '12345678-90ab-cdef-1234-567890abcdee',
        'samuuidver': verdoc3['uuidver'],
        'samintver': 1,
        'node': 'mynode2',
        'created': 700,
        'createby': 'u',
        'expired': 9007199254740991,
        'expireby': None
    }

    link4 = samplestorage._col_data_link.get('5_89_32_bc7324de86d54718dd0dc29c55c6d53a')
    assert link4 == {
        '_key': '5_89_32_bc7324de86d54718dd0dc29c55c6d53a',
        '_id': 'data_link/5_89_32_bc7324de86d54718dd0dc29c55c6d53a',
        '_from': 'ws_obj_ver/5:89:32',
        '_to': nodedoc1['_id'],
        '_rev': link4['_rev'],  # no need to test this
        'id': '12345678-90ab-cdef-1234-567890abcde4',
        'wsid': 5,
        'objid': 89,
        'objver': 32,
        'dataid': 'dataunit1',
        'sampleid': '12345678-90ab-cdef-1234-567890abcdef',
        'samuuidver': verdoc1['uuidver'],
        'samintver': 1,
        'node': 'mynode',
        'created': 800,
        'createby': 'userd',
        'expired': 9007199254740991,
        'expireby': None
    }

    # test get method
    dl1 = samplestorage.get_data_link(uuid.UUID('12345678-90ab-cdef-1234-567890abcde1'))
    assert dl1 == DataLink(
                    uuid.UUID('12345678-90ab-cdef-1234-567890abcde1'),
                    DataUnitID(UPA('5/89/32')),
                    SampleNodeAddress(
                        SampleAddress(uuid.UUID('12345678-90ab-cdef-1234-567890abcdef'), 2),
                        'mynode1'),
                    dt(500),
                    UserID('usera')
                    )

    dl2 = samplestorage.get_data_link(uuid.UUID('12345678-90ab-cdef-1234-567890abcde2'))
    assert dl2 == DataLink(
                    uuid.UUID('12345678-90ab-cdef-1234-567890abcde2'),
                    DataUnitID(UPA('42/42/42'), 'dataunit1'),
                    SampleNodeAddress(
                        SampleAddress(uuid.UUID('12345678-90ab-cdef-1234-567890abcdef'), 1),
                        'mynode'),
                    dt(600),
                    UserID('userb')
                    )

    dl3 = samplestorage.get_data_link(uuid.UUID('12345678-90ab-cdef-1234-567890abcde3'))
    assert dl3 == DataLink(
                    uuid.UUID('12345678-90ab-cdef-1234-567890abcde3'),
                    DataUnitID(UPA('5/89/32'), 'dataunit2'),
                    SampleNodeAddress(
                        SampleAddress(uuid.UUID('12345678-90ab-cdef-1234-567890abcdee'), 1),
                        'mynode2'),
                    dt(700),
                    UserID('u')
                    )

    dl4 = samplestorage.get_data_link(uuid.UUID('12345678-90ab-cdef-1234-567890abcde4'))
    assert dl4 == DataLink(
                    uuid.UUID('12345678-90ab-cdef-1234-567890abcde4'),
                    DataUnitID(UPA('5/89/32'), 'dataunit1'),
                    SampleNodeAddress(
                        SampleAddress(uuid.UUID('12345678-90ab-cdef-1234-567890abcdef'), 1),
                        'mynode'),
                    dt(800),
                    UserID('userd')
                    )


def test_create_data_link_correct_missing_versions(samplestorage):
    '''
    Checks that the version correction code runs when needed on creating a data link.
    Since the method is tested extensively in the get_sample tests, we only run one test here
    to ensure the method is called.
    This test simulates a server coming up after a dirty shutdown, where version and
    node doc integer versions have not been updated
    '''
    n1 = SampleNode('root')
    n2 = SampleNode('kid1', SubSampleType.TECHNICAL_REPLICATE, 'root')
    n3 = SampleNode('kid2', SubSampleType.SUB_SAMPLE, 'kid1')
    n4 = SampleNode('kid3', SubSampleType.TECHNICAL_REPLICATE, 'root')

    id_ = uuid.UUID('1234567890abcdef1234567890abcdef')

    assert samplestorage.save_sample(
        SavedSample(id_, UserID('user'), [n1, n2, n3, n4], dt(1), 'foo')) is True

    # this is very naughty
    # checked that these modifications actually work by viewing the db contents
    samplestorage._col_version.update_match({}, {'ver': -1})
    samplestorage._col_nodes.update_match({'name': 'kid2'}, {'ver': -1})

    samplestorage.create_data_link(DataLink(
        uuid.uuid4(),
        DataUnitID(UPA('5/89/32')),
        SampleNodeAddress(SampleAddress(id_, 1), 'kid1'),
        dt(500),
        UserID('user'))
    )

    assert samplestorage._col_version.count() == 1
    assert samplestorage._col_ver_edge.count() == 1
    assert samplestorage._col_nodes.count() == 4
    assert samplestorage._col_node_edge.count() == 4

    for v in samplestorage._col_version.all():
        assert v['ver'] == 1

    for v in samplestorage._col_nodes.all():
        assert v['ver'] == 1


def test_create_data_link_fail_no_link(samplestorage):
    _create_data_link_fail(samplestorage, None, ValueError(
        'link cannot be a value that evaluates to false'))


def test_create_data_link_fail_expired(samplestorage):
    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id1, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    _create_data_link_fail(
        samplestorage,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1')),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(-100),
            UserID('user'),
            dt(0),
            UserID('user')),
        ValueError('link cannot be expired')
        )


def test_create_data_link_fail_no_sample(samplestorage):
    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    id2 = uuid.UUID('1234567890abcdef1234567890abcdee')
    assert samplestorage.save_sample(
        SavedSample(id1, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    _create_data_link_fail(
        samplestorage,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1')),
            SampleNodeAddress(SampleAddress(id2, 1), 'mynode'),
            dt(1),
            UserID('user')),
        NoSuchSampleError(str(id2))
        )


def test_create_data_link_fail_no_sample_version(samplestorage):
    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id1, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True
    assert samplestorage.save_sample_version(
        SavedSample(id1, UserID('user'), [SampleNode('mynode1')], dt(2), 'foo')) == 2

    _create_data_link_fail(
        samplestorage,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1')),
            SampleNodeAddress(SampleAddress(id1, 3), 'mynode'),
            dt(1),
            UserID('user')),
        NoSuchSampleVersionError('12345678-90ab-cdef-1234-567890abcdef ver 3')
        )


def test_create_data_link_fail_link_exists(samplestorage):
    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(id1, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    samplestorage.create_data_link(DataLink(
        uuid.uuid4(),
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
        dt(500),
        UserID('user'))
    )

    samplestorage.create_data_link(DataLink(
        uuid.uuid4(),
        DataUnitID(UPA('1/1/1'), 'du1'),
        SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
        dt(500),
        UserID('user'))
    )

    _create_data_link_fail(
        samplestorage,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1')),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(1),
            UserID('user')),
        DataLinkExistsError('1/1/1')
        )

    _create_data_link_fail(
        samplestorage,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1'), 'du1'),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(1),
            UserID('user')),
        DataLinkExistsError('1/1/1:du1')
        )


def test_create_data_link_fail_too_many_links_from_ws_obj_basic(samplestorage):
    ss = _samplestorage_with_max_links(samplestorage, 3)

    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    id2 = uuid.UUID('1234567890abcdef1234567890abcde3')
    assert ss.save_sample(
        SavedSample(id1, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True
    assert ss.save_sample(
        SavedSample(id2, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    ss.create_data_link(DataLink(
        uuid.uuid4(),
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
        dt(500),
        UserID('user'))
    )

    ss.create_data_link(DataLink(
        uuid.uuid4(),
        DataUnitID(UPA('1/1/1'), '1'),
        SampleNodeAddress(SampleAddress(id2, 1), 'mynode'),
        dt(500),
        UserID('user'))
    )

    ss.create_data_link(DataLink(
        uuid.uuid4(),
        DataUnitID(UPA('1/1/1'), '2'),
        SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
        dt(500),
        UserID('user'))
    )

    _create_data_link_fail(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1'), '3'),
            SampleNodeAddress(SampleAddress(id2, 1), 'mynode'),
            dt(1),
            UserID('user')),
        TooManyDataLinksError('More than 3 links from workpace object 1/1/1')
        )


def test_create_data_link_fail_too_many_links_from_sample_ver_basic(samplestorage):
    ss = _samplestorage_with_max_links(samplestorage, 2)

    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert ss.save_sample(SavedSample(
        id1, UserID('user'), [SampleNode('mynode'), SampleNode('mynode2')], dt(1), 'foo')) is True

    ss.create_data_link(DataLink(
        uuid.uuid4(),
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
        dt(500),
        UserID('user'))
    )

    ss.create_data_link(DataLink(
        uuid.uuid4(),
        DataUnitID(UPA('1/1/2')),
        SampleNodeAddress(SampleAddress(id1, 1), 'mynode2'),
        dt(500),
        UserID('user'))
    )

    _create_data_link_fail(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/3')),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(1),
            UserID('user')),
        TooManyDataLinksError(
            'More than 2 links from sample 12345678-90ab-cdef-1234-567890abcdef version 1')
        )


def test_create_data_link_fail_too_many_links_from_ws_obj_time_travel(samplestorage):
    # tests that links that do not co-exist with the new link are not counted against the total.
    ss = _samplestorage_with_max_links(samplestorage, 3)

    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert ss.save_sample(
        SavedSample(id1, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True
    assert ss.save_sample_version(
        SavedSample(id1, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) == 2

    # completely outside the new sample time range.
    _create_and_expire_data_link(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1')),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(100),
            UserID('user')),
        dt(299),
        UserID('user')
    )

    # expire matches create
    _create_and_expire_data_link(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1'), '1'),
            SampleNodeAddress(SampleAddress(id1, 2), 'mynode'),
            dt(100),
            UserID('user')),
        dt(300),
        UserID('user')
    )

    # overlaps create
    _create_and_expire_data_link(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1'), '2'),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(250),
            UserID('user')),
        dt(350),
        UserID('user')
    )

    # contained inside
    _create_and_expire_data_link(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1'), '3'),
            SampleNodeAddress(SampleAddress(id1, 2), 'mynode'),
            dt(325),
            UserID('user')),
        dt(375),
        UserID('user')
    )

    _create_data_link_fail(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1'), '8'),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(300),
            UserID('user')),
        TooManyDataLinksError('More than 3 links from workpace object 1/1/1')
        )


def test_create_data_link_fail_too_many_links_from_sample_ver_time_travel(samplestorage):
    # tests that links that do not co-exist with the new link are not counted against the total.
    ss = _samplestorage_with_max_links(samplestorage, 3)

    id1 = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert ss.save_sample(
        SavedSample(id1, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    # completely outside the new sample time range.
    _create_and_expire_data_link(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/1')),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(100),
            UserID('user')),
        dt(299),
        UserID('user')
    )

    # expire matches create
    _create_and_expire_data_link(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/2')),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(100),
            UserID('user')),
        dt(300),
        UserID('user')
    )

    # overlaps create
    _create_and_expire_data_link(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/3')),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(250),
            UserID('user')),
        dt(350),
        UserID('user')
    )

    # contained inside
    _create_and_expire_data_link(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/4')),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(325),
            UserID('user')),
        dt(375),
        UserID('user')
    )

    _create_data_link_fail(
        ss,
        DataLink(
            uuid.uuid4(),
            DataUnitID(UPA('1/1/9')),
            SampleNodeAddress(SampleAddress(id1, 1), 'mynode'),
            dt(300),
            UserID('user')),
        TooManyDataLinksError('More than 3 links from sample ' +
                              '12345678-90ab-cdef-1234-567890abcdef version 1')
        )


def _create_and_expire_data_link(samplestorage, link, expired, user):
    samplestorage.create_data_link(link)
    samplestorage.expire_data_link(expired, user, link.id)


def _samplestorage_with_max_links(samplestorage, max_links):
    # this is very naughty
    return ArangoSampleStorage(
        samplestorage._db,
        samplestorage._col_sample.name,
        samplestorage._col_version.name,
        samplestorage._col_ver_edge.name,
        samplestorage._col_nodes.name,
        samplestorage._col_node_edge.name,
        samplestorage._col_ws.name,
        samplestorage._col_data_link.name,
        samplestorage._col_schema.name,
        max_links=max_links)


def _create_data_link_fail(samplestorage, link, expected):
    with raises(Exception) as got:
        samplestorage.create_data_link(link)
    assert_exception_correct(got.value, expected)


def test_get_data_link_fail_no_id(samplestorage):
    _get_data_link_fail(samplestorage, None, ValueError(
        'id_ cannot be a value that evaluates to false'))


def test_get_data_link_fail_no_link(samplestorage):
    sid = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(sid, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    lid = uuid.UUID('1234567890abcdef1234567890abcde1')
    samplestorage.create_data_link(DataLink(
        lid,
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(100),
        UserID('user'))
    )

    _get_data_link_fail(
        samplestorage,
        uuid.UUID('1234567890abcdef1234567890abcde2'),
        NoSuchLinkError('12345678-90ab-cdef-1234-567890abcde2'))


def test_get_data_link_fail_too_many_links(samplestorage):
    sid = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(sid, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    lid = uuid.UUID('1234567890abcdef1234567890abcde1')
    samplestorage.create_data_link(DataLink(
        lid,
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(100),
        UserID('user'))
    )
    samplestorage.create_data_link(DataLink(
        lid,
        DataUnitID(UPA('1/1/2')),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(100),
        UserID('user'))
    )

    _get_data_link_fail(
        samplestorage, lid, SampleStorageError(
            'More than one data link found for ID 12345678-90ab-cdef-1234-567890abcde1'))


def _get_data_link_fail(samplestorage, id_, expected):
    with raises(Exception) as got:
        samplestorage.get_data_link(id_)
    assert_exception_correct(got.value, expected)


def test_expire_and_get_data_link_via_duid(samplestorage):
    _expire_and_get_data_link_via_duid(samplestorage, 600, None, '')


def test_expire_and_get_data_link_via_duid_with_dataid(samplestorage):
    _expire_and_get_data_link_via_duid(
        samplestorage, -100, 'foo', 'acbd18db4cc2f85cedef654fccc4a4d8_')


def _expire_and_get_data_link_via_duid(samplestorage, expired, dataid, expectedmd5):
    sid = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(sid, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    lid = uuid.UUID('1234567890abcdef1234567890abcde1')
    samplestorage.create_data_link(DataLink(
        lid,
        DataUnitID(UPA('1/1/1'), dataid),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(-100),
        UserID('userb'))
    )

    # this is naughty
    verdoc1 = samplestorage._col_version.find({'id': str(sid), 'ver': 1}).next()
    nodedoc1 = samplestorage._col_nodes.find({'name': 'mynode'}).next()

    assert samplestorage.expire_data_link(
        dt(expired), UserID('yay'), duid=DataUnitID(UPA('1/1/1'), dataid)) == DataLink(
            lid,
            DataUnitID(UPA('1/1/1'), dataid),
            SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
            dt(-100),
            UserID('userb'),
            dt(expired),
            UserID('yay')
            )

    assert samplestorage._col_data_link.count() == 1

    link = samplestorage._col_data_link.get(f'1_1_1_{expectedmd5}-100.0')
    assert link == {
        '_key': f'1_1_1_{expectedmd5}-100.0',
        '_id': f'data_link/1_1_1_{expectedmd5}-100.0',
        '_from': 'ws_obj_ver/1:1:1',
        '_to': nodedoc1['_id'],
        '_rev': link['_rev'],  # no need to test this
        'id': '12345678-90ab-cdef-1234-567890abcde1',
        'wsid': 1,
        'objid': 1,
        'objver': 1,
        'dataid': dataid,
        'sampleid': '12345678-90ab-cdef-1234-567890abcdef',
        'samuuidver': verdoc1['uuidver'],
        'samintver': 1,
        'node': 'mynode',
        'created': -100,
        'createby': 'userb',
        'expired': expired,
        'expireby': 'yay'
    }

    assert samplestorage.get_data_link(lid) == DataLink(
        lid,
        DataUnitID(UPA('1/1/1'), dataid),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(-100),
        UserID('userb'),
        dt(expired),
        UserID('yay')
    )


def test_expire_and_get_data_link_via_id(samplestorage):
    _expire_and_get_data_link_via_id(samplestorage, 1000, None, '')


def test_expire_and_get_data_link_via_id_with_dataid(samplestorage):
    _expire_and_get_data_link_via_id(samplestorage, 1, 'foo', 'acbd18db4cc2f85cedef654fccc4a4d8_')


def _expire_and_get_data_link_via_id(samplestorage, expired, dataid, expectedmd5):
    sid = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(sid, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    lid = uuid.UUID('1234567890abcdef1234567890abcde1')
    samplestorage.create_data_link(DataLink(
        lid,
        DataUnitID(UPA('1/1/1'), dataid),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(.00056211),
        UserID('usera'))
    )

    # this is naughty
    verdoc1 = samplestorage._col_version.find({'id': str(sid), 'ver': 1}).next()
    nodedoc1 = samplestorage._col_nodes.find({'name': 'mynode'}).next()

    assert samplestorage.expire_data_link(dt(expired), UserID('user'), id_=lid) == DataLink(
        lid,
        DataUnitID(UPA('1/1/1'), dataid),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(0.00056211),
        UserID('usera'),
        dt(expired),
        UserID('user')
        )

    assert samplestorage._col_data_link.count() == 1

    link = samplestorage._col_data_link.get(f'1_1_1_{expectedmd5}0.000562')
    assert link == {
        '_key': f'1_1_1_{expectedmd5}0.000562',
        '_id': f'data_link/1_1_1_{expectedmd5}0.000562',
        '_from': 'ws_obj_ver/1:1:1',
        '_to': nodedoc1['_id'],
        '_rev': link['_rev'],  # no need to test this
        'id': '12345678-90ab-cdef-1234-567890abcde1',
        'wsid': 1,
        'objid': 1,
        'objver': 1,
        'dataid': dataid,
        'sampleid': '12345678-90ab-cdef-1234-567890abcdef',
        'samuuidver': verdoc1['uuidver'],
        'samintver': 1,
        'node': 'mynode',
        'created': 0.000562,
        'createby': 'usera',
        'expired': expired,
        'expireby': 'user'
    }

    link = samplestorage.get_data_link(lid)
    expected = DataLink(
        lid,
        DataUnitID(UPA('1/1/1'), dataid),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(0.000562),
        UserID('usera'),
        dt(expired),
        UserID('user')
    )
    assert link == expected


def test_expire_data_link_fail_bad_args(samplestorage):
    ss = samplestorage
    e = dt(100)
    i = uuid.uuid4()
    d = DataUnitID('1/1/1')
    eb = datetime.datetime.fromtimestamp(400)
    u = UserID('u')

    _expire_data_link_fail(ss, None, u, i, None, ValueError(
        'expired cannot be a value that evaluates to false'))
    _expire_data_link_fail(ss, eb, u, None, d, ValueError('expired cannot be a naive datetime'))
    _expire_data_link_fail(ss, e, None, None, d, ValueError(
        'expired_by cannot be a value that evaluates to false'))
    _expire_data_link_fail(ss, e, u, i, d, ValueError(
        'exactly one of id_ or duid must be provided'))
    _expire_data_link_fail(ss, e, u, None, None, ValueError(
        'exactly one of id_ or duid must be provided'))


def test_expire_data_link_fail_no_id(samplestorage):
    sid = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(sid, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    lid = uuid.UUID('1234567890abcdef1234567890abcde1')
    samplestorage.create_data_link(DataLink(
        lid,
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(-100),
        UserID('user'))
    )

    _expire_data_link_fail(
        samplestorage, dt(1), UserID('u'), uuid.UUID('1234567890abcdef1234567890abcde2'), None,
        NoSuchLinkError('12345678-90ab-cdef-1234-567890abcde2'))


def test_expire_data_link_fail_with_id_expired(samplestorage):
    sid = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(sid, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    lid = uuid.UUID('1234567890abcdef1234567890abcde1')
    samplestorage.create_data_link(DataLink(
        lid,
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(-100),
        UserID('user'))
    )

    samplestorage.expire_data_link(dt(0), UserID('u'), lid)

    _expire_data_link_fail(
        samplestorage, dt(1), UserID('u'), lid, None,
        NoSuchLinkError('12345678-90ab-cdef-1234-567890abcde1'))


def test_expire_data_link_fail_with_id_too_many_links(samplestorage):
    sid = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(sid, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    lid = uuid.UUID('1234567890abcdef1234567890abcde1')
    samplestorage.create_data_link(DataLink(
        lid,
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(-100),
        UserID('usera'))
    )

    samplestorage.expire_data_link(dt(-50), UserID('u'), lid)

    samplestorage.create_data_link(DataLink(
        lid,
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(0),
        UserID('usera'))
    )

    _expire_data_link_fail(samplestorage, dt(1), UserID('u'), lid, None, SampleStorageError(
        'More than one data link found for ID 12345678-90ab-cdef-1234-567890abcde1'))


def test_expire_data_link_fail_no_duid(samplestorage):
    sid = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(sid, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    lid1 = uuid.UUID('1234567890abcdef1234567890abcde1')
    samplestorage.create_data_link(DataLink(
        lid1,
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(-100),
        UserID('usera'))
    )
    lid2 = uuid.UUID('1234567890abcdef1234567890abcde2')
    samplestorage.create_data_link(DataLink(
        lid2,
        DataUnitID(UPA('1/1/2'), 'foo'),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(-100),
        UserID('usera'))
    )

    _expire_data_link_fail(
        samplestorage, dt(1), UserID('u'), None, DataUnitID(UPA('1/2/1')),
        NoSuchLinkError('1/2/1'))

    _expire_data_link_fail(
        samplestorage, dt(1), UserID('u'), None, DataUnitID(UPA('1/1/2'), 'fo'),
        NoSuchLinkError('1/1/2:fo'))


def test_expire_data_link_fail_expire_before_create_by_id(samplestorage):
    sid = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(sid, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    lid1 = uuid.UUID('1234567890abcdef1234567890abcde1')
    samplestorage.create_data_link(DataLink(
        lid1,
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(100),
        UserID('someuser'))
    )

    _expire_data_link_fail(samplestorage, dt(99), UserID('u'), lid1, None, ValueError(
        'expired is < link created time: 100'))


def test_expire_data_link_fail_race_condition(samplestorage):
    '''
    Tests the case where a link is expire after pulling it from the DB in the first part of the
    method. See notes in the code.
    '''

    sid = uuid.UUID('1234567890abcdef1234567890abcdef')
    assert samplestorage.save_sample(
        SavedSample(sid, UserID('user'), [SampleNode('mynode')], dt(1), 'foo')) is True

    lid1 = uuid.UUID('1234567890abcdef1234567890abcde1')
    samplestorage.create_data_link(DataLink(
        lid1,
        DataUnitID(UPA('1/1/1')),
        SampleNodeAddress(SampleAddress(sid, 1), 'mynode'),
        dt(-100),
        UserID('usera'))
    )

    # ok, we have the link doc from the db. This is what part 1 of the code does, and then
    # passes to part 2.
    linkdoc = samplestorage._col_data_link.get(f'1_1_1')

    # Now we simulate a race condition by expiring that link and calling part 2 of the expire
    # method. Part 2 should fail without modifying the links collection.
    samplestorage.expire_data_link(dt(200), UserID('foo'), lid1)

    with raises(Exception) as got:
        samplestorage._expire_data_link_pt2(linkdoc, dt(300), UserID('foo'), 'some id')
    assert_exception_correct(got.value, NoSuchLinkError('some id'))


def _expire_data_link_fail(samplestorage, expire, user, id_, duid, expected):
    with raises(Exception) as got:
        samplestorage.expire_data_link(expire, user, id_, duid)
    assert_exception_correct(got.value, expected)

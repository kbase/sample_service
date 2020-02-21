'''
Core class for saving and getting samples.
'''

import datetime
import uuid as _uuid
from uuid import UUID

from typing import Optional, Callable, Tuple, List, cast as _cast

from SampleService.core.arg_checkers import not_falsy as _not_falsy
from SampleService.core.acls import SampleAccessType as _SampleAccessType
from SampleService.core.acls import SampleACL, SampleACLOwnerless
from SampleService.core.errors import UnauthorizedError as _UnauthorizedError
from SampleService.core.errors import IllegalParameterError as _IllegalParameterError
from SampleService.core.validator.metadata_validator import MetadataValidator
from SampleService.core.errors import MetadataValidationError as _MetadataValidationError
from SampleService.core.errors import NoSuchUserError as _NoSuchUserError
from SampleService.core.sample import Sample, SavedSample
from SampleService.core.user_lookup import KBaseUserLookup
from SampleService.core import user_lookup as _user_lookup_mod
from SampleService.core.storage.arango_sample_storage import ArangoSampleStorage
from SampleService.core.storage.errors import OwnerChangedError as _OwnerChangedError


# TODO remove own acls.

class Samples:
    '''
    Class implementing sample manipulation operations.
    '''

    def __init__(
            self,
            storage: ArangoSampleStorage,
            user_lookup: KBaseUserLookup,  # make an interface? YAGNI
            metadata_validator: MetadataValidator,
            now: Callable[[], datetime.datetime] = lambda: datetime.datetime.now(
                tz=datetime.timezone.utc),
            uuid_gen: Callable[[], UUID] = lambda: _uuid.uuid4()):
        '''
        Create the class.

        :param storage: the storage system to use.
        :param user_lookup: a service to verify usernames are valid and exist.
        :param metadata_validator: A validator for metadata.
        '''
        # don't publicize these params
        # :param now: A callable that returns the current time. Primarily used for testing.
        # :param uuid_gen: A callable that returns a random UUID. Primarily used for testing.
        # extract an interface from ASS if needed.
        self._storage = _not_falsy(storage, 'storage')
        self._user_lookup = _not_falsy(user_lookup, 'user_lookup')
        self._metaval = _not_falsy(metadata_validator, 'metadata_validator')
        self._now = _not_falsy(now, 'now')
        self._uuid_gen = _not_falsy(uuid_gen, 'uuid_gen')

    def save_sample(
            self,
            sample: Sample,
            user: str,
            id_: UUID = None,
            prior_version: Optional[int] = None) -> Tuple[UUID, int]:
        '''
        Save a sample.

        :param sample: the sample to save.
        :param user: the username of the user saving the sample.
        :param id_: if the sample is a new version of a sample, the ID of the sample which will
            get a new version.
        :prior_version: if id_ is included, specifying prior_version will ensure that the new
            sample is saved with version prior_version + 1 or not at all.
        :returns a tuple of the sample ID and version.
        :raises IllegalParameterError: if the prior version is < 1
        :raises UnauthorizedError: if the user does not have write permission to the sample when
            saving a new version.
        :raises NoSuchSampleError: if the sample does not exist when saving a new version.
        :raises SampleStorageError: if the sample could not be retrieved when saving a new version
            or if the sample fails to save.
        :raises ConcurrencyError: if the sample's version is not equal to prior_version.
        '''
        _not_falsy(sample, 'sample')
        _not_falsy(user, 'user')
        self._validate_metadata(sample)
        if id_:
            if prior_version is not None and prior_version < 1:
                raise _IllegalParameterError('Prior version must be > 0')
            self._check_perms(id_, user, _SampleAccessType.WRITE)
            swid = SavedSample(id_, user, list(sample.nodes), self._now(), sample.name)
            ver = self._storage.save_sample_version(swid, prior_version)
        else:
            id_ = self._uuid_gen()
            swid = SavedSample(id_, user, list(sample.nodes), self._now(), sample.name)
            # don't bother checking output since we created uuid
            self._storage.save_sample(swid)
            ver = 1
        return (id_, ver)

    def _validate_metadata(self, sample: Sample):
        for i, n in enumerate(sample.nodes):
            try:
                self._metaval.validate_metadata(n.controlled_metadata)
            except _MetadataValidationError as e:
                raise _MetadataValidationError(f'Node at index {i}: {e.message}') from e

    def _check_perms(
            self,
            id_: UUID,
            user: str,
            access: _SampleAccessType,
            acls: SampleACL = None,
            as_admin: bool = False):
        if as_admin:
            return
        if not acls:
            acls = self._storage.get_sample_acls(id_)
        if self._get_access_level(acls, user) < access:
            errmsg = f'User {user} {self._unauth_errmap[access]} sample {id_}'
            raise _UnauthorizedError(errmsg)

    _unauth_errmap = {_SampleAccessType.OWNER: 'does not own',
                      _SampleAccessType.ADMIN: 'cannot administrate',
                      _SampleAccessType.WRITE: 'cannot write to',
                      _SampleAccessType.READ: 'cannot read'}

    def _get_access_level(self, acls: SampleACL, user: str):
        if user == acls.owner:
            return _SampleAccessType.OWNER
        if user in acls.admin:
            return _SampleAccessType.ADMIN
        if user in acls.write:
            return _SampleAccessType.WRITE
        if user in acls.read:
            return _SampleAccessType.READ
        return _SampleAccessType.NONE

    def get_sample(
            self,
            id_: UUID,
            user: str,
            version: int = None,
            as_admin: bool = False) -> SavedSample:
        '''
        Get a sample.
        :param id_: the ID of the sample.
        :param user: the username of the user getting the sample.
        :param version: The version of the sample to retrieve. Defaults to the latest version.
        :param as_admin: Skip ACL checks.
        :returns: the sample.
        :raises IllegalParameterError: if version is supplied and is < 1
        :raises UnauthorizedError: if the user does not have read permission for the sample.
        :raises NoSuchSampleError: if the sample does not exist.
        :raises NoSuchSampleVersionError: if the sample version does not exist.
        :raises SampleStorageError: if the sample could not be retrieved.
        '''
        # TODO get sample via a workspace object linking to it, SampleSet or linked object
        if version is not None and version < 1:
            raise _IllegalParameterError('Version must be > 0')
        self._check_perms(_not_falsy(id_, 'id_'), _not_falsy(user, 'user'),
                          _SampleAccessType.READ, as_admin=as_admin)
        return self._storage.get_sample(id_, version)

    def get_sample_acls(self, id_: UUID, user: str, as_admin: bool = False) -> SampleACL:
        '''
        Get a sample's acls.
        :param id_: the ID of the sample.
        :param user: the username of the user getting the acls.
        :param as_admin: Skip ACL checks.
        :returns: the sample acls.
        :raises UnauthorizedError: if the user does not have read permission for the sample.
        :raises NoSuchSampleError: if the sample does not exist.
        :raises SampleStorageError: if the sample could not be retrieved.
        '''
        _not_falsy(user, 'user')
        acls = self._storage.get_sample_acls(_not_falsy(id_, 'id_'))
        self._check_perms(id_, user, _SampleAccessType.READ, acls, as_admin=as_admin)
        return acls

    def replace_sample_acls(self, id_: UUID, user: str, new_acls: SampleACLOwnerless) -> None:
        '''
        Completely replace a sample's ACLs. The owner cannot be changed.

        :param id_: the sample's ID.
        :param user: the user changing the ACLs.
        :param new_acls: the new ACLs.
        :raises NoSuchUserError: if any of the users in the ACLs do not exist.
        :raises NoSuchSampleError: if the sample does not exist.
        :raises UnauthorizedError: if the user does not have admin permission for the sample or
            the request attempts to change the owner.
        :raises SampleStorageError: if the sample could not be retrieved.
        '''
        _not_falsy(id_, 'id_')
        _not_falsy(user, 'user')
        _not_falsy(new_acls, 'new_acls')
        try:
            bad_users = self._user_lookup.are_valid_users(
                _cast(List[str], []) + list(new_acls.admin) +
                list(new_acls.write) + list(new_acls.read))
            # let authentication errors propagate, not much to do
            # could add retries to the client
        except _user_lookup_mod.InvalidUserError as e:
            raise _NoSuchUserError(e.args[0]) from e
        except _user_lookup_mod.InvalidTokenError:
            raise ValueError('user lookup token for KBase auth server is invalid, cannot continue')
        if bad_users:
            raise _NoSuchUserError(', '.join(bad_users[:5]))

        count = 0
        while count >= 0:
            if count >= 5:
                raise ValueError(f'Failed setting ACLs after 5 attempts for sample {id_}')
            acls = self._storage.get_sample_acls(id_)
            self._check_perms(id_, user, _SampleAccessType.ADMIN, acls)
            new_acls = SampleACL(acls.owner, new_acls.admin, new_acls.write, new_acls.read)
            try:
                self._storage.replace_sample_acls(id_, new_acls)
                count = -1
            except _OwnerChangedError:
                count += 1

    # TODO change owner. Probably needs a request/accept flow.

import datetime
import unittest

import protovalidate
from google.protobuf import timestamp_pb2

from api.wine import proto_validation_test
from api.wine.v1.geography import appellation_pb2


_APPELLATION_UUID = '00000000-0000-0000-0000-000000000000'
_COUNTRY_UUID = '11111111-1111-1111-1111-111111111111'
_INVALID_UUID = 'not-a-uuid'
_NAME_TOO_SHORT = ''
_NAME_TOO_LONG = (
  '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
  '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
  '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
)
_NAME = 'Some Appellation'
_TIME_TOO_EARLY = timestamp_pb2.Timestamp(
  seconds=int(datetime.datetime(year=1970, month=1, day=1).timestamp())
)
_TIME = timestamp_pb2.Timestamp(
  seconds=int(datetime.datetime(year=2026, month=3, day=1).timestamp())
)


def _build_appellation(
    *,
    id: str | None = _APPELLATION_UUID,
    country_id: str | None = _COUNTRY_UUID,
    region_id: str | None = None,
    subregion_id: str | None = None,
    name: str | None = _NAME,
    created_at: timestamp_pb2.Timestamp | None = _TIME,
    updated_at: timestamp_pb2.Timestamp | None = _TIME,
) -> appellation_pb2.Appellation:
  """Helper function to build Appellation protos with default valid values.

  Calling this function with no arguments will return a valid Appellation proto.

  Args:
    id: The UUID of the Appellation.
    country_id: The UUID of the Country container.
    region_id: The UUID of the Region container.
    subregion_id: The UUID of the Subregion container.
    name: The name of the Appellation.
    created_at: The timestamp at which the Appellation was created.
    updated_at: The timestamp at which the Appellation was last updated.

  Returns:
    An Appellation proto with the specified values.
  """
  appellation = appellation_pb2.Appellation()

  if id is not None:
    appellation.id = id

  if country_id is not None:
    appellation.country_id = country_id

  if region_id is not None:
    appellation.region_id = region_id

  if subregion_id is not None:
    appellation.subregion_id = subregion_id

  if name is not None:
    appellation.name = name

  if created_at is not None:
    appellation.created_at.CopyFrom(created_at)

  if updated_at is not None:
    appellation.updated_at.CopyFrom(updated_at)

  return appellation


class AppellationTest(proto_validation_test.ProtoValidationTest[appellation_pb2.Appellation]):

  def setUp(self):
    self.validator = protovalidate.Validator()

  def _validator(self) -> protovalidate.Validator:
    return self.validator

  def test_valid_appellation_passes(self):
    violations = self.validator.collect_violations(_build_appellation())

    self.assertEqual(len(violations), 0)

  def test_appellation_with_empty_id_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(id=None),
        field_name='id',
        violation='value is required',
    )

  def test_appellation_with_invalid_id_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(id=_INVALID_UUID),
        field_name='id',
        violation='value must be a valid UUID',
    )

  def test_appellation_with_no_container_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(country_id=None),
        field_name='container',
        violation='exactly one field is required in oneof',
    )

  def test_appellation_with_invalid_country_id_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(country_id=_INVALID_UUID),
        field_name='country_id',
        violation='value must be a valid UUID',
    )

  def test_appellation_with_invalid_region_id_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(country_id=None, region_id=_INVALID_UUID),
        field_name='region_id',
        violation='value must be a valid UUID',
    )

  def test_appellation_with_invalid_subregion_id_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(country_id=None, subregion_id=_INVALID_UUID),
        field_name='subregion_id',
        violation='value must be a valid UUID',
    )

  def test_appellation_with_name_too_short_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(name=_NAME_TOO_SHORT),
        field_name='name',
        violation='value is required',
    )

  def test_appellation_with_name_too_long_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(name=_NAME_TOO_LONG),
        field_name='name',
        violation='value length must be at most 255 characters',
    )

  def test_appellation_with_created_at_empty_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(created_at=None),
        field_name='created_at',
        violation='value is required',
    )

  def test_appellation_with_created_at_too_early_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(created_at=_TIME_TOO_EARLY),
        field_name='created_at',
        violation='value must be greater than or equal to 2026-01-01T00:00:00Z',
    )

  def test_appellation_with_updated_at_empty_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(updated_at=None),
        field_name='updated_at',
        violation='value is required',
    )

  def test_appellation_with_updated_at_too_early_fails(self):
    self.collect_and_assert_violations(
        _build_appellation(updated_at=_TIME_TOO_EARLY),
        field_name='updated_at',
        violation='value must be greater than or equal to 2026-01-01T00:00:00Z',
    )


if __name__ == '__main__':
  unittest.main()

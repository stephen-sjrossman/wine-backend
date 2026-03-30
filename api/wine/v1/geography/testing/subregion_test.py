import datetime
import unittest

import protovalidate
from google.protobuf import timestamp_pb2

from api.wine import proto_validation_test
from api.wine.v1.geography import subregion_pb2


_SUBREGION_UUID = '00000000-0000-0000-0000-000000000000'
_REGION_UUID = '11111111-1111-1111-1111-111111111111'
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


def _build_subregion(
    *,
    id: str | None = _SUBREGION_UUID,
    region_id: str | None = _REGION_UUID,
    name: str | None = _NAME,
    created_at: timestamp_pb2.Timestamp | None = _TIME,
    updated_at: timestamp_pb2.Timestamp | None = _TIME,
) -> subregion_pb2.Subregion:
  """Helper function to build Subregion protos with default valid values.

  Calling this function with no arguments will return a valid Subregion proto.

  Args:
    id: The UUID of the Subregion.
    region_id: The UUID of the Region container.
    name: The name of the Subregion.
    created_at: The timestamp at which the Subregion was created.
    updated_at: The timestamp at which the Subregion was last updated.

  Returns:
    A Subregion proto with the specified values.
  """
  subregion = subregion_pb2.Subregion()

  if id is not None:
    subregion.id = id

  if region_id is not None:
    subregion.region_id = region_id

  if name is not None:
    subregion.name = name

  if created_at is not None:
    subregion.created_at.CopyFrom(created_at)

  if updated_at is not None:
    subregion.updated_at.CopyFrom(updated_at)

  return subregion


class AppellationTest(proto_validation_test.ProtoValidationTest[subregion_pb2.Subregion]):

  def setUp(self):
    self.validator = protovalidate.Validator()

  def _validator(self) -> protovalidate.Validator:
    return self.validator

  def test_valid_subregion_passes(self):
    violations = self.validator.collect_violations(_build_subregion())

    self.assertEqual(len(violations), 0)

  def test_subregion_with_empty_id_fails(self):
    self.collect_and_assert_violations(
        _build_subregion(id=None),
        field_name='id',
        violation='value is required',
    )

  def test_subregion_with_invalid_id_fails(self):
    self.collect_and_assert_violations(
        _build_subregion(id=_INVALID_UUID),
        field_name='id',
        violation='value must be a valid UUID',
    )

  def test_subregion_with_empty_region_id_fails(self):
    self.collect_and_assert_violations(
        _build_subregion(region_id=None),
        field_name='region_id',
        violation='value is required',
    )

  def test_subregion_with_invalid_region_id_fails(self):
    self.collect_and_assert_violations(
        _build_subregion(region_id=_INVALID_UUID),
        field_name='region_id',
        violation='value must be a valid UUID',
    )

  def test_subregion_with_name_too_short_fails(self):
    self.collect_and_assert_violations(
        _build_subregion(name=_NAME_TOO_SHORT),
        field_name='name',
        violation='value is required',
    )

  def test_subregion_with_name_too_long_fails(self):
    self.collect_and_assert_violations(
        _build_subregion(name=_NAME_TOO_LONG),
        field_name='name',
        violation='value length must be at most 255 characters',
    )

  def test_subregion_with_empty_created_at_fails(self):
    self.collect_and_assert_violations(
        _build_subregion(created_at=None),
        field_name='created_at',
        violation='value is required',
    )

  def test_subregion_with_created_at_too_early_fails(self):
    self.collect_and_assert_violations(
        _build_subregion(created_at=_TIME_TOO_EARLY),
        field_name='created_at',
        violation='value must be greater than or equal to 2026-01-01T00:00:00Z',
    )

  def test_subregion_with_empty_updated_at_fails(self):
    self.collect_and_assert_violations(
        _build_subregion(updated_at=None),
        field_name='updated_at',
        violation='value is required',
    )

  def test_subregion_with_updated_at_too_early_fails(self):
    self.collect_and_assert_violations(
        _build_subregion(updated_at=_TIME_TOO_EARLY),
        field_name='updated_at',
        violation='value must be greater than or equal to 2026-01-01T00:00:00Z',
      )


if __name__ == '__main__':
  unittest.main()

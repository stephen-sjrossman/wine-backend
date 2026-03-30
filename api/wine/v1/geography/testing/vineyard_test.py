import datetime
import unittest

import protovalidate
from google.protobuf import timestamp_pb2

from api.wine import proto_validation_test
from api.wine.v1.geography import vineyard_pb2


_VINEYARD_UUID = '00000000-0000-0000-0000-000000000000'
_APPELLATION_UUID = '11111111-1111-1111-1111-111111111111'
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


def _build_vineyard(
    *,
    id: str | None = _VINEYARD_UUID,
    appellation_id: str | None = _APPELLATION_UUID,
    name: str | None = _NAME,
    created_at: timestamp_pb2.Timestamp | None = _TIME,
    updated_at: timestamp_pb2.Timestamp | None = _TIME,
) -> vineyard_pb2.Vineyard:
  """Helper function to build Vineyard protos with default valid values.

  Calling this function with no arguments will return a valid Vineyard proto.

  Args:
    id: The UUID of the Vineyard.
    appellation_id: The UUID of the Appellation container.
    name: The name of the Vineyard.
    created_at: The timestamp at which the Vineyard was created.
    updated_at: The timestamp at which the Vineyard was last updated.

  Returns:
    A Vineyard proto with the specified values.
  """
  vineyard = vineyard_pb2.Vineyard()

  if id is not None:
    vineyard.id = id

  if appellation_id is not None:
    vineyard.appellation_id = appellation_id

  if name is not None:
    vineyard.name = name

  if created_at is not None:
    vineyard.created_at.CopyFrom(created_at)

  if updated_at is not None:
    vineyard.updated_at.CopyFrom(updated_at)

  return vineyard


class AppellationTest(proto_validation_test.ProtoValidationTest[vineyard_pb2.Vineyard]):

  def setUp(self):
    self.validator = protovalidate.Validator()

  def _validator(self) -> protovalidate.Validator:
    return self.validator

  def test_valid_vineyard_passes(self):
    violations = self.validator.collect_violations(_build_vineyard())

    self.assertEqual(len(violations), 0)

  def test_vineyard_with_empty_id_fails(self):
    self.collect_and_assert_violations(
        _build_vineyard(id=None),
        field_name='id',
        violation='value is required',
    )

  def test_vineyard_with_invalid_id_fails(self):
    self.collect_and_assert_violations(
        _build_vineyard(id=_INVALID_UUID),
        field_name='id',
        violation='value must be a valid UUID',
    )

  def test_vineyard_with_empty_appellation_id_fails(self):
    self.collect_and_assert_violations(
        _build_vineyard(appellation_id=None),
        field_name='appellation_id',
        violation='value is required',
    )

  def test_vineyard_with_invalid_appellation_id_fails(self):
    self.collect_and_assert_violations(
        _build_vineyard(appellation_id=_INVALID_UUID),
        field_name='appellation_id',
        violation='value must be a valid UUID',
    )

  def test_vineyard_with_name_too_short_fails(self):
    self.collect_and_assert_violations(
        _build_vineyard(name=_NAME_TOO_SHORT),
        field_name='name',
        violation='value is required',
    )

  def test_vineyard_with_name_too_long_fails(self):
    self.collect_and_assert_violations(
        _build_vineyard(name=_NAME_TOO_LONG),
        field_name='name',
        violation='value length must be at most 255 characters',
    )

  def test_vineyard_with_empty_created_at_fails(self):
    self.collect_and_assert_violations(
        _build_vineyard(created_at=None),
        field_name='created_at',
        violation='value is required',
    )

  def test_vineyard_with_created_at_too_early_fails(self):
    self.collect_and_assert_violations(
        _build_vineyard(created_at=_TIME_TOO_EARLY),
        field_name='created_at',
        violation='value must be greater than or equal to 2026-01-01T00:00:00Z',
      )

  def test_vineyard_with_empty_updated_at_fails(self):
    self.collect_and_assert_violations(
        _build_vineyard(updated_at=None),
        field_name='updated_at',
        violation='value is required',
    )

  def test_vineyard_with_updated_at_too_early_fails(self):
    self.collect_and_assert_violations(
        _build_vineyard(updated_at=_TIME_TOO_EARLY),
        field_name='updated_at',
        violation='value must be greater than or equal to 2026-01-01T00:00:00Z',
      )


if __name__ == '__main__':
  unittest.main()

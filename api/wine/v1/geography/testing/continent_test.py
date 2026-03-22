import datetime
import unittest

import protovalidate
from google.protobuf import timestamp_pb2

from api.wine import proto_validation_test
from api.wine.v1.geography import continent_pb2


_CONTINENT_UUID = '00000000-0000-0000-0000-000000000000'
_INVALID_UUID = 'not-a-uuid'
_NAME_TOO_SHORT = ''
_NAME_TOO_LONG = (
  '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
  '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
  '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
)
_NAME = 'Some Continent'
_TIME_TOO_EARLY = timestamp_pb2.Timestamp(
  seconds=int(datetime.datetime(year=1970, month=1, day=1).timestamp())
)
_TIME = timestamp_pb2.Timestamp(
  seconds=int(datetime.datetime(year=2026, month=3, day=1).timestamp())
)


def _build_continent(
    *,
    id: str | None = _CONTINENT_UUID,
    name: str | None = _NAME,
    created_at: timestamp_pb2.Timestamp | None = _TIME,
    updated_at: timestamp_pb2.Timestamp | None = _TIME,
) -> continent_pb2.Continent:
  """Helper function to build Continent protos with default valid values.

  Calling this function with no arguments will return a valid Continent proto.

  Args:
    id: The UUID of the Continent.
    name: The name of the Continent.
    created_at: The timestamp at which the Continent was created.
    updated_at: The timestamp at which the Continent was last updated.

  Returns:
    A Continent proto with the specified values.
  """
  continent = continent_pb2.Continent()

  if id is not None:
    continent.id = id

  if name is not None:
    continent.name = name

  if created_at is not None:
    continent.created_at.CopyFrom(created_at)

  if updated_at is not None:
    continent.updated_at.CopyFrom(updated_at)

  return continent


class ContinentTest(proto_validation_test.ProtoValidationTest):

  def setUp(self):
    self.validator = protovalidate.Validator()

  def test_valid_continent_passes(self):
    violations = self.validator.collect_violations(_build_continent())

    self.assertEqual(len(violations), 0)

  def test_continent_with_empty_id_fails(self):
    continent = _build_continent(id=None)

    violations = self.validator.collect_violations(continent)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('id_violation'):
      self.match_violations(violations, 'id', ['value is required'])

  def test_continent_with_invalid_id_fails(self):
    continent = _build_continent(id=_INVALID_UUID)

    violations = self.validator.collect_violations(continent)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('id_violation'):
      self.match_violations(violations, 'id', ['value must be a valid UUID'])

  def test_continent_with_name_too_short_fails(self):
    continent = _build_continent(name=_NAME_TOO_SHORT)

    violations = self.validator.collect_violations(continent)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('name_violation'):
      self.match_violations(violations, 'name', ['value is required'])

  def test_continent_with_name_too_long_fails(self):
    continent = _build_continent(name=_NAME_TOO_LONG)

    violations = self.validator.collect_violations(continent)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('name_violation'):
      self.match_violations(violations, 'name', ['value length must be at most 255 characters'])

  def test_continent_with_created_at_empty_fails(self):
    continent = _build_continent(created_at=None)

    violations = self.validator.collect_violations(continent)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('created_at_violation'):
      self.match_violations(violations, 'created_at', ['value is required'])

  def test_continent_with_created_at_too_early_fails(self):
    continent = _build_continent(created_at=_TIME_TOO_EARLY)

    violations = self.validator.collect_violations(continent)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('created_at_violation'):
      self.match_violations(
          violations,
          'created_at',
          ['value must be greater than or equal to 2026-01-01T00:00:00Z'],
      )

  def test_continent_with_updated_at_empty_fails(self):
    continent = _build_continent(updated_at=None)

    violations = self.validator.collect_violations(continent)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('updated_at_violation'):
      self.match_violations(violations, 'updated_at', ['value is required'])

  def test_continent_with_updated_at_too_early_fails(self):
    continent = _build_continent(updated_at=_TIME_TOO_EARLY)

    violations = self.validator.collect_violations(continent)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('updated_at_violation'):
      self.match_violations(
          violations,
          'updated_at',
          ['value must be greater than or equal to 2026-01-01T00:00:00Z'],
      )


if __name__ == '__main__':
  unittest.main()

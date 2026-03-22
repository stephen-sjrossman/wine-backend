import datetime
import unittest

import protovalidate
from google.protobuf import timestamp_pb2

from api.wine import proto_validation_test
from api.wine.v1.geography import country_pb2


_COUNTRY_UUID = '00000000-0000-0000-0000-000000000000'
_CONTINENT_UUID = '11111111-1111-1111-1111-111111111111'
_INVALID_UUID = 'not-a-uuid'
_NAME_TOO_SHORT = ''
_NAME_TOO_LONG = (
  '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
  '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
  '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
)
_NAME = 'Some Appellation'
_ISO_CODE_TOO_SHORT = 'A'
_ISO_CODE_TOO_LONG = 'ABCDE'
_ISO_CODE_INVALID_CHARS = '12'
_ISO_CODE = 'US'
_FLAG_URL_INVALID = 'not-a-url'
_FLAG_URL = 'https://www.example.com/flag.png'
_TIME_TOO_EARLY = timestamp_pb2.Timestamp(
  seconds=int(datetime.datetime(year=1970, month=1, day=1).timestamp())
)
_TIME = timestamp_pb2.Timestamp(
  seconds=int(datetime.datetime(year=2026, month=3, day=1).timestamp())
)


def _build_country(
    *,
    id: str | None = _COUNTRY_UUID,
    continent_id: str | None = _CONTINENT_UUID,
    name: str | None = _NAME,
    iso_code: str | None = _ISO_CODE,
    flag_url: str | None = _FLAG_URL,
    created_at: timestamp_pb2.Timestamp | None = _TIME,
    updated_at: timestamp_pb2.Timestamp | None = _TIME,
) -> country_pb2.Country:
  """Helper function to build Country protos with default valid values.

  Calling this function with no arguments will return a valid Country proto.

  Args:
    id: The UUID of the Country.
    continent_id: The UUID of the Continent container.
    name: The name of the Country.
    created_at: The timestamp at which the Country was created.
    updated_at: The timestamp at which the Country was last updated.

  Returns:
    A Country proto with the specified values.
  """
  country = country_pb2.Country(
    metadata=country_pb2.Country.Metadata(),
  )

  if id is not None:
    country.id = id

  if continent_id is not None:
    country.continent_id = continent_id

  if name is not None:
    country.name = name

  if iso_code is not None:
    country.metadata.iso_code = iso_code

  if flag_url is not None:
    country.metadata.flag_url = flag_url

  if created_at is not None:
    country.created_at.CopyFrom(created_at)

  if updated_at is not None:
    country.updated_at.CopyFrom(updated_at)

  return country


class AppellationTest(proto_validation_test.ProtoValidationTest):

  def setUp(self):
    self.validator = protovalidate.Validator()

  def test_valid_country_passes(self):
    violations = self.validator.collect_violations(_build_country())

    self.assertEqual(len(violations), 0)

  def test_country_with_empty_id_fails(self):
    country = _build_country(id=None)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('id_violation'):
      self.match_violations(violations, 'id', ['value is required'])

  def test_country_with_invalid_id_fails(self):
    country = _build_country(id=_INVALID_UUID)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('id_violation'):
      self.match_violations(violations, 'id', ['value must be a valid UUID'])

  def test_country_with_empty_continent_id_fails(self):
    country = _build_country(continent_id=None)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('container_violation'):
      self.match_violations(violations, 'continent_id', ['value is required'])

  def test_country_with_invalid_continent_id_fails(self):
    country = _build_country(continent_id=_INVALID_UUID)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('continent_id_violation'):
      self.match_violations(violations, 'continent_id', ['value must be a valid UUID'])

  def test_country_with_name_too_short_fails(self):
    country = _build_country(name=_NAME_TOO_SHORT)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('name_violation'):
      self.match_violations(violations, 'name', ['value is required'])

  def test_country_with_name_too_long_fails(self):
    country = _build_country(name=_NAME_TOO_LONG)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('name_violation'):
      self.match_violations(violations, 'name', ['value length must be at most 255 characters'])

  def test_country_with_empty_iso_code_fails(self):
    country = _build_country(iso_code=None)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('iso_code_violation'):
      self.match_violations(violations, 'iso_code', ['value is required'])

  def test_country_with_iso_code_too_short_fails(self):
    country = _build_country(iso_code=_ISO_CODE_TOO_SHORT)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('iso_code_violation'):
      self.match_violations(
          violations,
          'iso_code',
          ['value does not match regex pattern `^[A-Z]{2}$`'],
      )

  def test_country_with_iso_code_too_long_fails(self):
    country = _build_country(iso_code=_ISO_CODE_TOO_LONG)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('iso_code_violation'):
      self.match_violations(
          violations,
          'iso_code',
          ['value does not match regex pattern `^[A-Z]{2}$`'],
      )

  def test_country_with_iso_code_containing_invalid_chars_fails(self):
    country = _build_country(iso_code=_ISO_CODE_INVALID_CHARS)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('iso_code_violation'):
      self.match_violations(
          violations,
          'iso_code',
          ['value does not match regex pattern `^[A-Z]{2}$`'],
      )

  def test_country_with_empty_flag_url_fails(self):
    country = _build_country(flag_url=None)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('flag_url_violation'):
      self.match_violations(violations, 'flag_url', ['value is required'])

  def test_country_with_invalid_flag_url_fails(self):
    country = _build_country(flag_url=_FLAG_URL_INVALID)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('flag_url_violation'):
      self.match_violations(
          violations,
          'flag_url',
          ['value must be a valid URI'],
      )

  def test_country_with_empty_metadata_fails(self):
    country = _build_country()
    country.ClearField('metadata')

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('metadata_violation'):
      self.match_violations(violations, 'metadata', ['value is required'])

  def test_country_with_empty_created_at_fails(self):
    country = _build_country(created_at=None)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('created_at_violation'):
      self.match_violations(violations, 'created_at', ['value is required'])

  def test_country_with_created_at_too_early_fails(self):
    country = _build_country(created_at=_TIME_TOO_EARLY)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('created_at_violation'):
      self.match_violations(
          violations,
          'created_at',
          ['value must be greater than or equal to 2026-01-01T00:00:00Z'],
      )

  def test_country_with_empty_updated_at_fails(self):
    country = _build_country(updated_at=None)

    violations = self.validator.collect_violations(country)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)

    with self.subTest('updated_at_violation'):
      self.match_violations(violations, 'updated_at', ['value is required'])

  def test_country_with_updated_at_too_early_fails(self):
    country = _build_country(updated_at=_TIME_TOO_EARLY)

    violations = self.validator.collect_violations(country)

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

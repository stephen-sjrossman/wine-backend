import abc
import unittest
from collections.abc import Sequence
from typing import Generic, TypeVar

import protovalidate
from buf.validate import validate_pb2
from google.protobuf import message
from protovalidate import validator


T = TypeVar('T', bound=message.Message)

class ProtoValidationTest(unittest.TestCase, Generic[T], abc.ABC):

  @abc.abstractmethod
  def _validator(self) -> protovalidate.Validator:
    """Returns the protovalidate.Validator to use for validation in the tests."""

  def match_violations(
      self,
      violations: list[validator.Violation],
      field_name: str,
      messages: Sequence[str],
  ) -> None:
    """Matches the given violations to the given field name & messages.

    Args:
      violations: The list of violations to match.
      field_name: The field name to match.
      messages: The list of messages to match.

    Raises:
      AssertionError: If the count of matching violations does not match
        the count of messages, or if any violation's message does not match
        the corresponding message in the list (order enforced).
    """
    matching_violation_messages = []
    for violation in violations:
      proto: validate_pb2.Violation = violation.proto
      for element in proto.field.elements:
        if element.field_name == field_name:
          matching_violation_messages.append(violation.proto.message)

    with self.subTest(f'{field_name}_violation_count'):
      self.assertEqual(len(matching_violation_messages), len(messages))
    with self.subTest(f'{field_name}_violation_messages'):
      self.assertSequenceEqual(matching_violation_messages, messages)

  def collect_and_assert_violations(
      self,
      proto: T,
      *,
      field_name: str,
      violation: str,
  ) -> None:
    """Collects violations for the message & asserts they match the violation passed.

    Args:
      message: The message to collect violations for.
      field_name: The field name to match in the violations.
      violation: The expected violation message.

    Raises:
      AssertionError: If the count of matching violations is not 1, or if the
        violation message does not match the expected violation.
    """
    violations = self._validator().collect_violations(proto)

    with self.subTest('violation_count'):
      self.assertEqual(len(violations), 1)
    with self.subTest('violation_content'):
      self.match_violations(violations, field_name, [violation])

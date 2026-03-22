import unittest
from collections.abc import Sequence

from protovalidate import validator


class ProtoValidationTest(unittest.TestCase):

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
      for element in violation.proto.field.elements:
        if element.field_name == field_name:
          matching_violation_messages.append(violation.proto.message)

    with self.subTest(f'{field_name}_violation_count'):
      self.assertEqual(len(matching_violation_messages), len(messages))
    with self.subTest(f'{field_name}_violation_messages'):
      self.assertSequenceEqual(matching_violation_messages, messages)

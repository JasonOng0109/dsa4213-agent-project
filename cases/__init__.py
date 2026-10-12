"""The case corpus: one module per case, registered below.

How to write a case: docs/authoring-rules.md.
"""

from . import m1

CASES = {case["case_id"]: case for case in (m1.CASE,)}

"""The case corpus: one module per case, registered below.

How to write a case: docs/authoring-rules.md.
"""

from . import m1, m3, m5

CASES = {case["case_id"]: case for case in (m1.CASE, m3.CASE, m5.CASE)}

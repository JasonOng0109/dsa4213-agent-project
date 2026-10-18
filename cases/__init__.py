"""The case corpus: one module per case, registered below.

How to write a case: docs/authoring-rules.md.
"""

from . import m1, m5, m4 

CASES = {case["case_id"]: case for case in (m1.CASE, m4.CASE, m5.CASE)}

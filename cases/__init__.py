"""The case corpus: one module per case, registered below.

How to write a case: docs/authoring-rules.md.
"""

from . import m1, m2, m3, m4, m5, m14, m15, m24, m30, m31, m32, m33

CASES = {case["case_id"]: case for case in (m1.CASE, m2.CASE, m3.CASE, m4.CASE, m5.CASE, m14.CASE, m15.CASE, m24.CASE, m30.CASE, m31.CASE, m32.CASE, m33.CASE)}
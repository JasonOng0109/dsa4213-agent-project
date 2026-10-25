"""The case corpus: one module per case, registered below.

How to write a case: docs/authoring-rules.md.
"""

from . import m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m20, m22, m23, m24, m25, m26, m27, m28, m30, m31, m32, m33, m34, m35, m36, m37, m38, m39, m40

CASES = {case["case_id"]: case for case in (m1.CASE, m2.CASE, m3.CASE, m4.CASE, m5.CASE, m6.CASE, m7.CASE, m8.CASE, m9.CASE, m10.CASE, m11.CASE, m12.CASE, m13.CASE, m14.CASE, m15.CASE, m16.CASE, m17.CASE, m20.CASE, m22.CASE, m23.CASE, m24.CASE, m25.CASE, m26.CASE, m27.CASE, m28.CASE, m30.CASE, m31.CASE, m32.CASE, m33.CASE, m34.CASE, m35.CASE, m36.CASE, m37.CASE, m38.CASE, m39.CASE, m40.CASE)}

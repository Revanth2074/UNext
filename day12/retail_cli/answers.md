# Project 2 Milestone Questions & Answers

This document details the answers to the "TRICKY" questions posed in the Day 12 Capstone Project Workbook.

---

## Milestone 2: Data Structures & OOP

### Q2.6 TRICKY
**Question:** Why is a `set` the right choice for tracking low-stock SKUs across a batch with repeated rows for the same SKU, rather than a `list`? What goes wrong with a `list` if the same unknown MSISDN (or SKU) appears in 50 CDRs (or sales transactions)?

**Answer:**
1. **Uniqueness / De-duplication:** A `set` only stores unique elements. If a low-stock SKU or unknown SKU is referenced in 50 different sales transactions within a single batch, a `set` will store it exactly once. A `list`, on the other hand, will add the SKU 50 times, resulting in duplicated alert outputs, redundant reports, and clutter.
2. **Performance:** Checking membership (e.g. `item in set`) is a constant time operation $O(1)$ on average. For a list, membership tests require scanning the list, which is a linear time operation $O(n)$.
3. **Semantic Correctness:** Conceptually, an alert flags a specific unique entity (the SKU) as needing attention. The entity either is or is not low-stock/unknown. A set mathematically models this binary property of containment without ordering or duplicates.

---

## Milestone 3: File Handling & Error Handling

### Q3.6 TRICKY
**Question:** Why is catching `ValueError` specifically in `load_sales` better than a broad `except Exception:`? What would broad-except hide if `sales.csv` had the wrong file encoding entirely, versus just one bad row?

**Answer:**
1. **Precision / Error Classification:** By catching `ValueError`, we target only the expected errors resulting from data parsing (e.g. attempting to convert a malformed discount string like `"invalid_discount"` to a float). This allows us to skip that specific row and proceed safely with the rest of the batch.
2. **Hiding Critical Errors:** A broad `except Exception:` catches all errors, including system-level issues like `PermissionError`, `MemoryError`, or `KeyboardInterrupt`. Most importantly:
   - If `sales.csv` has the wrong file encoding entirely (e.g. UTF-16 instead of UTF-8), it will raise a `UnicodeDecodeError` or standard decoder failure.
   - If we catch `Exception`, we would treat this file-level reading failure as a series of "malformed rows" or fail the batch silently under a generic message.
   - If the file doesn't exist, it raises `FileNotFoundError`. If we catch `Exception` inside the parsing routine, we might mask file access issues as data validation issues.
3. **Maintainability:** Coding standards (such as PEP8) discourage broad exceptions because they make debugging extremely difficult, hiding code bugs (like referencing an undefined variable, which raises a `NameError`) under the guise of an input data error.

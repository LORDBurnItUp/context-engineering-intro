# Task List

## Completed Tasks

### [2026-01-21] Fix bare except clause bug in RAG agent CLI
**Status:** ✅ Completed

**Description:**
Fixed a common anti-pattern in the RAG agent's CLI code where a bare `except:` clause was catching all exceptions, including system exits and keyboard interrupts. This is dangerous as it can mask critical errors.

**Changes Made:**
- Modified `/use-cases/agent-factory-with-subagents/agents/rag_agent/cli.py:246`
- Changed bare `except:` to `except ValueError:` to catch only the specific exception expected during type conversion
- Added comprehensive unit tests in `tests/test_cli.py` to test the value conversion logic:
  - Test for float conversion
  - Test for int conversion
  - Test for string preservation
  - Test for malformed input handling
  - Test for edge cases like negative numbers

**Impact:**
- Improved error handling and code safety
- System interrupts (Ctrl+C) will now work properly during value conversion
- More maintainable and Pythonic code

**Technical Details:**
The code was attempting to convert user input strings to float or int. The bare `except:` would catch any exception, including those that shouldn't be caught. The fix properly catches only `ValueError`, which is the expected exception when type conversion fails.

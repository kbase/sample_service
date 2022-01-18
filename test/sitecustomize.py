import coverage
import os

if "COVERAGE_PROCESS_START" in os.environ:
    print("COVERAGE_PROCESS_START: ", os.environ["COVERAGE_PROCESS_START"])

    coverage.process_startup()

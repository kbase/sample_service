import coverage
import os

if "COVERAGE_PROCESS_START" in os.environ:
    print(
        "[sitecustomize] coverage will run; COVERAGE_PROCESS_START: ",
        os.environ["COVERAGE_PROCESS_START"],
        flush=True,
    )

    coverage.process_startup()
else:
    print("[sitecustomize] coverage not running", flush=True)

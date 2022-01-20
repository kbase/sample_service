#!/bin/bash

echo '[ENTRYPOINT-TEST] starting'
echo "[ENTRYPOINT-TEST] using option ${1}"

script_dir=$(dirname "$(readlink -f "$0")")
export PYTHONPATH="${script_dir}/../lib:$PATH:$PYTHONPATH"

echo "[ENTRYPOINT-TEST] Python path: ${PYTHONPATH}"

if [ "${1}" = "bash" ] ; then
  export PYTHONPATH="$script_dir/..:$PYTHONPATH"
  echo "[ENTRYPOINT-TEST] shell mode with Python path: ${PYTHONPATH}"
  bash
elif [ "${1}" = "begin" ] ; then
  # Python path must include the test directory in order for the test validators
  # to be loadable.
  export PYTHONPATH="$script_dir/..:$PYTHONPATH"
  echo "[ENTRYPOINT-TEST] begin tests"
  make test-begin
elif [ "${1}" = "end" ] ; then
  # Python path must include the test directory in order for the test validators
  # to be loadable.
  export PYTHONPATH="$script_dir/..:$PYTHONPATH"
  echo "[ENTRYPOINT-TEST] end tests"
  make test-end
elif [ "${1}" = "unit" ] ; then
  # Python path must include the test directory in order for the test validators
  # to be loadable.
  export PYTHONPATH="$script_dir/..:$PYTHONPATH"
  echo "[ENTRYPOINT-TEST] unit-test mode with PythXon path: ${PYTHONPATH}"
  make test-unit
elif [ "${1}" = "integration" ] ; then
  # Python path must include the test directory in order for the test validators
  # to be loadable.
  export PYTHONPATH="$script_dir/..:$PYTHONPATH"
  echo "[ENTRYPOINT-TEST] integration test mode with Python path: ${PYTHONPATH}"
  make test-integration
elif [ "${1}" = "system" ] ; then
  # Python path must include the test directory in order for the test validators
  # to be loadable.
  export PYTHONPATH="$script_dir/..:$PYTHONPATH"
  echo "[ENTRYPOINT-TEST] system test mode with Python path: ${PYTHONPATH}"
  # Note that this is the internal address, so always port 5000.
  SAMPLE_SERVICE_URL=http://sampleservice:5000 make wait-for-sample-service
  make test-system
elif [ "${1}" = "prepare-arango" ] ; then
  echo "[ENTRYPOINT-TEST] Preparing arango..." 
  python "${script_dir}/../../lib/cli/prepare-arango.py"
  echo "[ENTRYPOINT-TEST] arango ready"
else
  echo "[ENTRYPOINT-TEST] Error! Unknown entrypoint option: ${1}"
  exit 1
fi

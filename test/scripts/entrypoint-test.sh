#!/bin/bash

echo '[ENTRYPOINT-TEST] starting'
echo "[ENTRYPOINT-TEST] using command '${1}'"

script_dir=$(dirname "$(readlink -f $0)")

export ROOT_DIR=$(realpath "$script_dir/../..")
export LIB_DIR="${ROOT_DIR}/lib"
export TEST_DIR="${ROOT_DIR}/test"
export PYTHONPATH="${TEST_DIR}:${LIB_DIR}:$PATH:$PYTHONPATH"

echo "[ENTRYPOINT-TEST] Python path: ${PYTHONPATH}"

if [ "${1}" = "bash" ] ; then
  echo "[ENTRYPOINT-TEST] shell mode"
  bash

elif [ "${1}" = "hello" ] ; then
  echo "[ENTRYPOINT-TEST] HELLO"

elif [ "${1}" = "begin" ] ; then
  echo "[ENTRYPOINT-TEST] begin tests"
  make test-begin

elif [ "${1}" = "end" ] ; then
  echo "[ENTRYPOINT-TEST] end tests"
  make test-end

elif [ "${1}" = "unit" ] ; then
  echo "[ENTRYPOINT-TEST] unit-test mode"
  make test-unit

elif [ "${1}" = "types" ] ; then
  echo "[ENTRYPOINT-TEST] mypy types mode"
  MYPYPATH="${LIB_DIR}" python -m mypy --namespace-packages "${LIB_DIR}/SampleService/core" "${TEST_DIR}"
  # make test-types

elif [ "${1}" = "integration" ] ; then
  echo "[ENTRYPOINT-TEST] integration test mode"
  SAMPLE_SERVICE_URL=http://sampleservice:5000 make wait-for-sample-service
  make test-integration

elif [ "${1}" = "system" ] ; then
  echo "[ENTRYPOINT-TEST] system test mode with Python path: ${PYTHONPATH}"
  # Note that this is the internal address, so always port 5000.
  SAMPLE_SERVICE_URL=http://sampleservice:5000 make wait-for-sample-service
  make test-system

else
  echo "[ENTRYPOINT-TEST] Error! Unknown entrypoint option: ${1}"
  exit 1
fi

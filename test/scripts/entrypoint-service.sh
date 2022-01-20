#!/bin/bash

echo '[ENTRYPOINT] starting'

dockerize ${EXTRA} -template deploy.cfg.tmpl:deploy.cfg

script_dir=$(dirname "$(readlink -f "$0")")

#
# Several aspects of the service rely on loading the deploy config file.
#
export KB_DEPLOYMENT_CONFIG=$script_dir/../../deploy.cfg

#
# Python path must include the test directory in order for the test validators
# to be loadable, the sitecustomize file to be invoked.
#
export PYTHONPATH="$script_dir/../../test:$script_dir/../../lib:$PYTHONPATH"

#
# Populates arangodb with collections, waits for it to be ready
#

# echo "[ENTRYPOINT] Preparing arango..." 
# python "${script_dir}/../../lib/cli/prepare-arango.py"
# echo "[ENTRYPOINT] arango ready"

#
# Parameters for gunicorn
#
workers=1
log_level=debug

# 
# Enable coverage if the "coverage" command is supplied
#
if [ "${1}" = "coverage" ] ; then
  export COVERAGE_PROCESS_START="test/coveragerc-system"
  echo "[ENTRYPOINT] Coverage option provided; COVERAGE_PROCESS_START is '${COVERAGE_PROCESS_START}'"
fi

echo "[ENTRYPOINT] Starting gunicorn with Python path: ${PYTHONPATH}"
exec gunicorn --worker-class gevent \
    --timeout 30 \
    --reload \
    --workers $workers \
    --bind :5000 \
    --log-level $log_level  \
    --capture-output \
    --env COVERAGE_PROCESS_START="${COVERAGE_PROCESS_START}" \
    --env PYTHONVERBOSE="TRUE" \
    SampleService.SampleServiceServer:application

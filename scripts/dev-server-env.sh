#
# The path to data for the mock services service
#
DEFAULT_MOCK_DATASET_PATH="${PWD}/dev/data/SampleService"
if [ -z "$MOCK_DATASET_PATH" ]; then
  echo "'MOCK_DATASET_PATH' environment variable set - default of '${DEFAULT_MOCK_DATASET_PATH}' will be used"
  export DC_MOCK_DATASET_PATH=$DEFAULT_MOCK_DATASET_PATH
else
  echo "'MOCK_DATASET_PATH' environment variable set to '$MOCK_DATASET_PATH'"
  export DC_MOCK_DATASET_PATH=$MOCK_DATASET_PATH
fi

#
# The 
#
DEFAULT_VALIDATION_SPEC_URL="https://raw.githubusercontent.com/kbase/sample_service_validator_config/master/metadata_validation.yml"
if [ -z "$VALIDATION_SPEC_URL" ]; then
  echo "'VALIDATION_SPEC_URL' environment variable set - default of '${DEFAULT_VALIDATION_SPEC_URL}' will be used"
  export DC_VALIDATION_SPEC_URL=${DEFAULT_VALIDATION_SPEC_URL}
else
  echo "'VALIDATION_SPEC_URL' environment variable set to '$VALIDATION_SPEC_URL'"
   export DC_VALIDATION_SPEC_URL=${VALIDATION_SPEC_URL}
fi

DEFAULT_PORT="5000"
if [ -z "$PORT" ]; then
  echo "'PORT' environment variable set - default of '${DEFAULT_PORT}' will be used"
  export DC_PORT=${DEFAULT_PORT}
else
  echo "'PORT' environment variable set to '$PORT'"
  export DC_PORT=$PORT
fi

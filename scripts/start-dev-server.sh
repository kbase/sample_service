root=$(git rev-parse --show-toplevel)

if [ -z "$MOCK_DATASET_PATH" ]; then
	echo "The 'MOCK_DATASET_PATH' environment variable is required"
	exit 1
fi
echo "MOCK_DATASET_PATH is set to ${MOCK_DATASET_PATH}"

if [ -z "$PORT" ]; then
  echo "'PORT' environment variable set - default of 5000 will be used"
else
   echo "'PORT' environment variable set to '$PORT'"
fi

# See if port is in use.
USING_PORT=$(lsof -i ":${PORT:-5000}")
if [ -n "$USING_PORT" ]; then
  echo "Another application is using port '${PORT:-5000}' (see below)"
  echo ""
  echo "${USING_PORT}"
  echo ""
  echo "Please set PORT to another value and try again."
  echo ""
  exit 1
fi

docker compose -f test/docker-compose.yml up

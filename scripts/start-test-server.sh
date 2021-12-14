root=$(git rev-parse --show-toplevel)

if [ -z "$MOCK_DATASET_PATH" ]; then
	echo "The 'MOCK_DATASET_PATH' environment variable is required"
	exit 1
fi
export mock_dataset_path=${MOCK_DATASET_PATH}
echo "mock_dataset_path is set to ${mock_dataset_path}"

docker compose up

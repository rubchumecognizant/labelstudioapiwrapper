#!/bin/bash
CREDENTIALS_FILE=$1
CONFIGURATION_FILE=$2

# shellcheck source=./*.env
source $CREDENTIALS_FILE
# shellcheck source=./*.env
source $CONFIGURATION_FILE


curl --location --request POST "http://$LABEL_STUDIO_HOST:$LABEL_STUDIO_PORT/api/storages/export/azure" \
--header "Authorization: Token $LABEL_STUDIO_API_TOKEN" \
--header 'Content-Type: application/json' \
--data-raw "{
  \"container\": \"$TARGET_AZURE_CONTAINER\",
  \"prefix\": \"$TARGET_AZURE_FOLDER_PREFIX\",
  \"use_blob_urls\": true,
  \"account_name\": \"$TARGET_AZURE_STORAGE_ACCOUNT_NAME\",
  \"account_key\": \"$TARGET_AZURE_STORAGE_ACCOUNT_KEY\",
  \"title\": \"$TARGET_CONNECTION_NAME\",
  \"description\": \"$TARGET_CONNECTION_DESCRIPTION\",
  \"last_sync\": \"2019-08-24T14:15:22Z\",
  \"last_sync_count\": 0,
  \"can_delete_objects\": true,
  \"project\": $LABEL_STUDIO_PROJECT_ID
}"

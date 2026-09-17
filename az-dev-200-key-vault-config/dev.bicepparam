using './main.bicep'

// Secrets fetched from CI at deploy-time; DO NOT commit real values.
// The @secure params ensure they never appear in ARM deployment history.
param dbConnectionString          = readEnvironmentVariable('DB_CONN_STR', 'Server=tcp:anchorline-dev.database.windows.net;Encrypt=true;Trusted_Connection=False;')
param serviceBusConnectionString  = readEnvironmentVariable('SB_CONN_STR', 'Endpoint=sb://anchorline-dev.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=placeholder')
param cognitiveServicesKey        = readEnvironmentVariable('COG_KEY', 'placeholder-key')

// Azure Blob wrapper — the parallel-module alternative to gcs.ts.
// Uses user-delegation SAS tokens (Entra-signed, not account-key signed) via
// DefaultAzureCredential. See:
//   https://learn.microsoft.com/azure/storage/blobs/storage-blob-create-user-delegation-sas-javascript
//
// Caller identity needs Storage Blob Data Contributor (write) or Reader (read)
// plus permission to call getUserDelegationKey.
import {
  BlobServiceClient,
  BlobSASPermissions,
  SASProtocol,
  generateBlobSASQueryParameters,
} from "@azure/storage-blob";
import { DefaultAzureCredential } from "@azure/identity";
import { appConfig } from "./config.js";

function serviceUrl(): string {
  if (!appConfig.azure.account) {
    throw new Error("AZURE_STORAGE_ACCOUNT not set — see .env.example");
  }
  return `https://${appConfig.azure.account}.blob.core.windows.net`;
}

function service(): BlobServiceClient {
  return new BlobServiceClient(serviceUrl(), new DefaultAzureCredential());
}

function container() {
  return service().getContainerClient(appConfig.azure.container);
}

async function sasFor(
  key: string,
  permissions: "r" | "w",
  expiresSec: number,
): Promise<string> {
  const svc = service();
  const startsOn = new Date(Date.now() - 60_000);
  const expiresOn = new Date(Date.now() + expiresSec * 1000);
  const udk = await svc.getUserDelegationKey(startsOn, expiresOn);

  const sas = generateBlobSASQueryParameters(
    {
      containerName: appConfig.azure.container,
      blobName: key,
      permissions: BlobSASPermissions.parse(permissions),
      startsOn,
      expiresOn,
      protocol: SASProtocol.Https,
    },
    udk,
    appConfig.azure.account,
  ).toString();

  const client = container().getBlockBlobClient(key);
  return `${client.url}?${sas}`;
}

export const blob = {
  async upload(buffer: Buffer, key: string, contentType: string): Promise<string> {
    const client = container().getBlockBlobClient(key);
    await client.uploadData(buffer, {
      blobHTTPHeaders: { blobContentType: contentType },
    });
    return client.url;
  },

  getSignedPutUrl(key: string, _contentType: string, expiresSec = 900): Promise<string> {
    return sasFor(key, "w", expiresSec);
  },

  getSignedGetUrl(key: string, expiresSec = 300): Promise<string> {
    return sasFor(key, "r", expiresSec);
  },

  async setPublicRead(_key: string): Promise<void> {
    // Azure public access is container-scoped, not per-blob — turn on anonymous
    // read via container access policy or disable allowBlobPublicAccess=false.
    // Left as a no-op here on purpose; L4 teaches "signed-only" as the right
    // default anyway.
  },

  publicUrl(key: string): string {
    return container().getBlockBlobClient(key).url;
  },
};

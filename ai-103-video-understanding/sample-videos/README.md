# sample-videos/

Short public-domain product-demo MP4s used by Exercise 2 (`src/upload_videos.py`).
The starter does NOT bake video binaries into the repo - every lab clone would
pay the download cost, and any modernization sweep would need to rewrite huge
blobs. Instead, `src/upload_videos.py` downloads them from public URLs into
this folder on demand.

## Where the videos come from

Two files are named in `SAMPLE_URLS` inside `src/upload_videos.py`:

- `hero_shot.mp4` - short indoor/studio product close-ups.
- `field_test.mp4` - outdoor field test with wind and terrain.

Both are small (~1-2 MB) synthetic samples pulled from the public
`Azure-Samples/cognitive-services-quickstart-code` GitHub repository (no
authentication required, no rate limits under normal lab usage). If those
public URLs stop resolving:

1. Any small MP4 works - the lab's exercises never assert specific frame
   content, only the SHAPE of the CU response (segments, fields, timestamps).
2. Substitute your own product-demo MP4s and keep the two filenames stable
   (`hero_shot.mp4`, `field_test.mp4`) - the exercise text + the agent's
   citation strings reference those names.

## Local storage

Anything you drop here is git-ignored (`.gitignore` excludes `*.mp4`, `*.mov`,
`*.mkv`). Only this `README.md` is tracked.

## Alternate paths

If your organization requires an internal sample source instead of GitHub raw
URLs, edit `SAMPLE_URLS` in `src/upload_videos.py` to point at your own signed
URLs. The rest of the pipeline (analyzer, index, agent) doesn't care where the
blob came from as long as it lands under the `videos/` container.

# sample_images/

This folder is intentionally near-empty in the starter. Each exercise
generates the images it needs from the FastAPI service itself:

- **Exercise 1** — `POST /generate` produces `storefront.png`, and
  `POST /edit` produces `storefront_edited.png`. A small `make_mask.py`
  snippet in the exercise creates `mask.png` with Pillow.
- **Exercise 2** — reuses `storefront.png` from Exercise 1 and generates
  a `pack.png` from a second `/generate` call.
- **Exercise 3** — reuses `/generate` to create `summitline_front.png`
  (a storefront with visible hours and phone).
- **Exercise 4** — a `make_test_images.py` Pillow snippet in the exercise
  creates `benign.png`, `injection.png`, and `subtle_injection.png`.

If you want to try your own photo (for example, a real product shot), drop
a PNG in this folder and reference its path in the `curl -F "image=@..."`
calls in place of the generated files. Keep images under 20 MB and in PNG
format — `images.edit` in particular rejects JPEG input.

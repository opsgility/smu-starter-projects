import os, sys
from dotenv import load_dotenv
import anthropic
def main():
    load_dotenv()
    if not os.environ.get("ANTHROPIC_API_KEY","").strip() or os.environ.get("ANTHROPIC_API_KEY","").startswith("<"):
        print("verify_env: FAIL"); return 1
    c = anthropic.Anthropic()
    r = c.messages.create(model=os.environ.get("ANTHROPIC_MODEL","claude-sonnet-5"), max_tokens=8,
                          messages=[{"role":"user","content":"Say ready."}])
    print("OK", next((b.text for b in r.content if b.type == "text"), "").strip()); return 0
if __name__ == "__main__": sys.exit(main())

# XPIA Test Harness

Local HTTP server for hosting Cross-Prompt Injection Attack (XPIA) test payloads.

## Quick Start

```powershell
cd xpia-test-harness
python server.py
```

Then browse to **http://localhost:8080** for the payload index.

## Usage

- **Add a payload**: Drop an `.html` file into `payloads/`
- **Edit a payload**: Edit any file in `payloads/` — changes appear instantly on page refresh
- **Remove a payload**: Delete the file from `payloads/`
- **Custom port**: `python server.py --port 9090`

### Payload descriptions

Add an HTML comment as the first line of your payload file to set a description:
```html
<!-- My description here -->
```

## Included Payloads

| # | File | Attack Category |
|---|------|-----------------|
| 01 | direct-instruction-override | Classic "ignore previous instructions" |
| 02 | role-hijacking | Attempts to reassign the model's persona |
| 03 | data-exfiltration | Tries to extract system prompt or user data |
| 04 | hidden-text-injection | Instructions concealed with CSS (invisible text) |
| 05 | goal-hijacking | Redirects the model to a different task |
| 06 | delimiter-escape | Tries to break out of content/context boundaries |
| 07 | subtle-persuasion | Injection blended naturally into plausible content |
| 08 | markdown-injection | Markdown/image tags that may render in chat UI |
| 09 | multi-language-injection | Base64 + non-English text to bypass filters |
| 10 | benign-baseline | Clean page — use as a control in your tests |

## Tips

- Always test with the **benign baseline** (payload 10) to establish expected behavior
- Compare model responses between benign and adversarial payloads
- The hidden-text payload (04) is especially important — many systems extract text and miss CSS
- Copy the URL from the index page and paste it into your URL slot for testing

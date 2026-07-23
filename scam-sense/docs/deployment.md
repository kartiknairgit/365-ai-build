# Deployment

ScamSense is ready for Streamlit Community Cloud or another service that can run a Python Streamlit process. No account, application secret, API key, database or paid service is required by the app.

## Streamlit Community Cloud

1. Merge the release branch into `main`.
2. In Streamlit Community Cloud, create an app from `kartiknairgit/365-ai-build`.
3. Choose branch `main`.
4. Set the entrypoint to `scam-sense/app.py`.
5. In advanced settings, select Python 3.12.
6. Leave the secrets field empty.
7. Deploy and replace the README's live-demo placeholder with the assigned URL.

`scam-sense/requirements.txt` is beside the entrypoint as recommended by Streamlit. It pins Streamlit to the version covered by CI. Community Cloud runs the entrypoint from the repository root, and the app resolves its isolated `scam-sense/src` package accordingly.

## Clean-environment verification

From the repository root:

```bash
python3.12 -m venv /tmp/scamsense-release
/tmp/scamsense-release/bin/python -m pip install -r scam-sense/requirements.txt
/tmp/scamsense-release/bin/python scam-sense/scripts/smoke_streamlit.py
```

The smoke check starts `scam-sense/app.py`, waits for Streamlit's local health endpoint, then stops the process.

## Privacy boundary

The application has no user accounts, analytics integration, database, logging of pasted text, or external analysis API. Text is analysed in the running Streamlit session's memory. A public deployment necessarily sends pasted text to the host running the app, so deployers should use a trusted host, HTTPS and accurate privacy copy. Users should remove personal information where practical.

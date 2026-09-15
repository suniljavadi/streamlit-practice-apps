# Streamlit Practice Applications

**Status: Learning project**

Small Streamlit applications exploring interactive Python UI patterns, including a basic app, a chatbot-style app, and an enhanced chatbot entry point.

## Entry Points

| File | Purpose |
| --- | --- |
| `app.py` | Basic Streamlit application |
| `streamlit_app.py` | Streamlit application variant |
| `chatbot.py` | Chatbot-oriented application code |
| `streamlit_enhanced_chatbot.py` | Enhanced chatbot-oriented entry point |

## Run Locally

Install the dependencies in a virtual environment, then run the entry point you want to inspect:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The basic entry points do not require external credentials. The advanced chatbot optionally uses the spaCy `en_core_web_sm` model and online translation; it falls back to token splitting, no entity results, or the original text when those resources are unavailable. The repository does not include automated tests, persistent storage, or a deployment configuration, so each entry point remains an exploratory example.

## Future Improvements

Add `requirements.txt`, screenshots, clear app-specific instructions, error handling, tests, and a documented deployment target once one application is selected for further development.

## Author

**Sunil Javadi**

- [GitHub](https://github.com/suniljavadi)
- [Portfolio](https://github.com/suniljavadi/sunil-portfolio)
- [LinkedIn](https://www.linkedin.com/in/sunil-javadi/)Practising Streamlit

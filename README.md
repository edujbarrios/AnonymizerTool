# PDF anonymizer tool

### https://anonymizertool.streamlit.app/

A tool that allows users to upload a PDF and get an anonimized PDF or embedding JSON files.

It can anonymize through regex:

- Spanish IDs (NIF / DNI)
- email
- phone
- adress

### Example:

```python
'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
```

**More keywords can be added by using specific regex by editing `src/utils.py` and the function `aonymize_text()`**

## Set up guide

**A full detailed set up will be added soon**, by now just take into account this tool uses **Streamlit** as a core for the UI, and other libraries for the in deep process. Check `pyproject.toml` for more details.

The way to execute this program is the following:

`streamlit run app.py`

## Contributing

Any contribution is welcomed, throw a pull request if you have any updates on this code.

## ToDo:

- Set Up README guide
- Create full anonymizations across a wide pdf dataset directory
- Allow Excel files

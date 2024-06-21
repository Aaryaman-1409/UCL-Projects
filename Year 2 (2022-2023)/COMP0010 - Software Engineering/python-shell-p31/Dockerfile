FROM python:3-slim

WORKDIR comp0010

COPY . .

RUN chmod u+x tools/test tools/coverage tools/analysis

RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "src/shell.py"]
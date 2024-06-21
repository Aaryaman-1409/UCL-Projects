FROM tsl0922/ttyd:latest

RUN apt update -y && apt install -y python3 python3-pip 

WORKDIR comp0010

COPY . .

RUN chmod u+x tools/test tools/coverage tools/analysis

RUN python3 -m pip install --no-cache-dir -r requirements.txt

EXPOSE 7681

CMD ["ttyd", "-W", "python3", "src/shell.py"]

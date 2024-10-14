FROM python:3.12.7-alpine
LABEL maintainer="craigb78@googlemail.com"

RUN adduser -D pgn_user
USER pgn_user
WORKDIR /home/pgn_user

COPY --chown=pgn_user:pgn_user pgn pgn
COPY --chown=pgn_user:pgn_user pgn_files pgn_files
COPY --chown=pgn_user:pgn_user requirements.txt requirements.txt
RUN pip3 install --user -r requirements.txt

CMD [ "python3", "-m", "pgn.main", "pgn_files/Karpov.pgn" ]

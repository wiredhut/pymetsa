FROM python:3.10
RUN pip install "poetry==1.3.2"

# Copy code
WORKDIR /code

# Install dependencies
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false \
  && poetry install $(test "sipe" == production && echo "--no-dev") --no-interaction --no-ansi

# Copy necessary code
COPY ./app /code/app
COPY ./data /code/data
COPY ./pymetsa /code/pymetsa
COPY ./start.sh /code/start.sh

RUN chmod +x /code/start.sh

# Socket configuration
CMD ["./start.sh"]
FROM python:3.11.5-slim-bookworm

WORKDIR /bot

RUN apt-get update && \
    apt-get install --no-install-recommends -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -U poetry


COPY ./poetry.lock* ./pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /bot
CMD ["poetry", "run", "task", "start"]
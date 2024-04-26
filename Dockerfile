FROM python:latest
COPY . /
RUN pip install -r requirements.txt
CMD ["python", "./perfect_strategst_vs_random_strategy_bots.py"]
FROM python:latest
COPY . /
RUN pip install -r requirements.txt
CMD ["python", "./perfect_strategist_vs_random_permutation_bots.py"]
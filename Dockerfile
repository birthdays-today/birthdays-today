FROM python as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY data/ data/
RUN mkdir birthdays
RUN python /app/data/ETL/get_birthday_day.py

FROM nginx:alpine
COPY site /usr/share/nginx/html
COPY --from=builder /app/birthdays /usr/share/nging/html/csv

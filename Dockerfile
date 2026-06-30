#pushing this from laptop's pycharm to github
#use official python image. start from an image that already has pythin installed

FROM python:3.12-slim

#create working directory. inside container create a app directory and get into it
WORKDIR /app

#copy requirements.txt first
COPY requirements.txt

#install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#copy the remaining application copy entire project from current to /app
COPY . .

#flask user port 5000. app runs on 55000
EXPOSE 55000

#Start the application
CMD ["python", "app.py"]
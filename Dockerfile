FROM python:3.12-slim-bookworm

# Set the working directory
WORKDIR /nulleinspeisung


# Copy the requirements file and install dependencies
COPY requirements.txt /nulleinspeisung/
COPY nulleinspeisung.py /nulleinspeisung/
RUN pip install --no-cache-dir -r requirements.txt

# precompile the python code
RUN python -m compileall /nulleinspeisung

# set env vars
ENV PYTHONUNBUFFERED=1

# Specify the command to run the application
CMD ["python", "nulleinspeisung.py"]
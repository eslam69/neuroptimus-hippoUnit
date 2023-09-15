# Use an official Python runtime as a parent image
FROM continuumio/miniconda3:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a new conda environment from the environment.yml file
RUN conda env create -f environment.yml

# Activate the conda environment
RUN echo "conda activate neuroptimus" >> ~/.bashrc

# Set the default command to run the project in GUI mode
CMD ["python", "neuroptimus/neuroptimus.py", "-g"]

# Allow the user to run the project in command-line mode with a configuration file
ENTRYPOINT ["python", "neuroptimus/neuroptimus.py", "-c"]
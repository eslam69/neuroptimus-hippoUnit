# Use a base image with Conda installed
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /app

# Copy the environment YAML file
COPY environment_integration.yml .

# Create the Conda environment
RUN conda env create -f environment_integration.yml

# Activate the environment
SHELL ["conda", "run", "-n", "neuroptimus", "/bin/bash", "-c"]

# Install PyQt5
RUN conda install -n neuroptimus pyqt=5.15.7

# Install xvfb
RUN apt-get update && apt-get install -y xvfb && apt-get clean


# RUN conda install git+https://github.com/eslam69/hippounit.git


# Copy the application code
COPY . .

ENV DISPLAY=:99

# Set the entry point
ENTRYPOINT ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & exec conda run --no-capture-output -n neuroptimus python neuroptimus/neuroptimus.py \"$@\"", "--"]
#e.g.
# ENTRYPOINT ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & exec conda run --no-capture-output -n neuroptimus python neuroptimus/neuroptimus.py -c neuroptimus/Data/CA1pyramidal_package/neuroptimus_settings.json "]

# to run command in my local machine
# sudo docker run -it -v /home/eslam/gsoc/neuroptimus-hippoUnit:/home/eslam/gsoc/neuroptimus-hippoUnit neuroptimus -c <path to the json file>
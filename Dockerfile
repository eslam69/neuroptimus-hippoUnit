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
# RUN apt-get update && apt-get install -y xvfb && apt-get clean

# Install xvfb and additional dependencies for Qt
RUN apt-get update && apt-get install -y \
    xvfb \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libxcb-xinput0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-sync1 \
    libxcb-xkb1 \
    libxrender1 \
    libxcomposite1 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libxss1 \
    libxext6 \
    libx11-xcb1 \
    && apt-get clean




# # Install necessary dependencies
# RUN apt-get update && apt-get install -y \
#     libxss1 \
#     libxext6 \
#     libx11-xcb1 \
#     libxcb1 \
#     libxcb-xinerama0 \
#     libxcb-xinput0 \
#     libxcb-xkb1 \
#     libxkbcommon-x11-0 \
#     libxrender1 \
#     libxi6 \
#     libgl1-mesa-glx \
#     libegl1-mesa \
#     libfontconfig1 \
#     && apt-get clean


# RUN conda install git+https://github.com/eslam69/hippounit.git


# Copy the application code
COPY . .

# Set environment variables
ENV DISPLAY=:99
ENV QT_QPA_PLATFORM=xcb

# Set the entry point
ENTRYPOINT ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & exec conda run --no-capture-output -n neuroptimus python neuroptimus/neuroptimus.py \"$@\"", "--"]
#e.g.
# ENTRYPOINT ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & exec conda run --no-capture-output -n neuroptimus python neuroptimus/neuroptimus.py -c neuroptimus/Data/CA1pyramidal_package/neuroptimus_settings.json "]


# to build the docker image
#xhost +local:docker
# sudo docker build -t neuroptimus .
# run command in my local machine
# sudo docker run -it -v /home/eslam/gsoc/neuroptimus-hippoUnit:/home/eslam/gsoc/neuroptimus-hippoUnit neuroptimus -c <path to the json file>
# sudo docker run -it -v /home/eslam/gsoc/neuroptimus-hippoUnit:/home/eslam/gsoc/neuroptimus-hippoUnit neuroptimus -c /home/eslam/gsoc/neuroptimus-hippoUnit/neuroptimus/Data/new_test_files/VClamp_surrogate/VClamp_surrogate_settings.json









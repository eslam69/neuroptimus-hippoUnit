# Use a base image with Conda installed
FROM continuumio/miniconda3

# Set a build argument for platform-specific logic
ARG PLATFORM=linux
ENV PLATFORM=$PLATFORM

# Set the working directory
WORKDIR /app

# Copy the environment YAML file
COPY environment_integration.yml .

# Create the Conda environment
RUN conda env create -f environment_integration.yml

# Use bash as the default shell
SHELL ["/bin/bash", "-c"]

# Activate the Conda environment and install PyQt5
RUN conda run -n neuroptimus conda install pyqt=5.15.7

# Install xvfb and additional dependencies for Qt (Linux only)
RUN if [ "$PLATFORM" = "linux" ]; then \
    apt-get update && apt-get install -y \
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
    && apt-get clean; \
fi

# Copy the application code
COPY . .

# Set environment variables
ENV DISPLAY=:99
ENV QT_QPA_PLATFORM=xcb



# Entry point based on the platform
ENTRYPOINT ["sh", "-c", "if [ \"$PLATFORM\" = \"linux\" ]; then \
    Xvfb :99 -screen 0 1024x768x16 & exec conda run --no-capture-output -n neuroptimus python neuroptimus/neuroptimus.py \"$@\"; \
else \
    exec conda run --no-capture-output -n neuroptimus python neuroptimus/neuroptimus.py \"$@\"; \
fi", "--"]
# for linux
#docker build --build-arg PLATFORM=linux -t neuroptimus .
# sudo docker run -it -v $(pwd):/home/eslam/gsoc/neuroptimus-hippoUnit -c <path to the json file>



# for windows
#docker build --build-arg PLATFORM=windows -t neuroptimus .
# docker run -it -v C:/path/to/your/project:/app neuroptimus -c <path to the json file>




#e.g.
# ENTRYPOINT ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & exec conda run --no-capture-output -n neuroptimus python neuroptimus/neuroptimus.py -c neuroptimus/Data/CA1pyramidal_package/neuroptimus_settings.json "]


# to build the docker image
#xhost +local:docker
# sudo docker build -t neuroptimus .
# run command in my local machine
# sudo docker run -it -v /home/eslam/gsoc/neuroptimus-hippoUnit:/home/eslam/gsoc/neuroptimus-hippoUnit neuroptimus -c <path to the json file>
# sudo docker run -it -v /home/eslam/gsoc/neuroptimus-hippoUnit:/home/eslam/gsoc/neuroptimus-hippoUnit neuroptimus -c /home/eslam/gsoc/neuroptimus-hippoUnit/neuroptimus/Data/new_test_files/VClamp_surrogate/VClamp_surrogate_settings.json
# sudo docker run -it -v $(pwd):/home/eslam/gsoc/neuroptimus-hippoUnit neuroptimus -c /home/eslam/gsoc/neuroptimus-hippoUnit/neuroptimus/Data/new_test_files/VClamp_surrogate/VClamp_surrogate_settings.json









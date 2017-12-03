# ContaminationAnalyzer #
The Contamination Spreading Analyzer (CSA) project is under development and it was started to obtain the master degree 
on Computer and Systems Engineering at Federal University of Rio de Janeiro (UFRJ). The objective is to apply concepts 
of complex networks and allow the user to simulate the evolution of a spreading disease on an environment, with a high 
level of abstraction. So the user can focus on analyze the contamination properties and its impact on the environment.

## Setup ##

The easy way to start using the CSA is by the container image on [paulormnas/csa](https://hub.docker.com/r/paulormnas/csa/) 
repository in Docker Hub. If you do not have the Docker installed yet, you can fallow the instructions on 
[Install Docker CE](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce) session.

After install the docker you can download the image from Docker Hub repo as following:

```commandline
$ docker pull paulormnas/csa
```

You can verify the image you just downloaded with:

```commandline
$ docker images
```

Now you need to clone the CSA repo from Github. First create a new directory and then download the code inside it:

```commandline
$ mkdir csa
$ cd csa
$ git clone https://github.com/paulormnas/ContaminationAnalyzer.git
```   

## Running ##

As the software is under development we did not created the container image with the CSA already, neither made a script 
which allow to download it from Github repository automatically. So you will need to copy the CSA code to a directory inside 
the container.

First you have to run the following code so the GUI can be show on host:

```commandline
 $ xhost +local:
 ```

Now start the container:

```commandline
$ docker run -ti --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix paulormnas/csa ipython3
```


On a new terminal, get the container ID and copy the code to a directory inside the container:

```commandline
$ docker container ls
CONTAINER ID        IMAGE                    COMMAND          CREATED                STATUS                   PORTS               NAMES
de513c9e2123       paulormnas/csa      "ipython3"         23 seconds ago      Up 22 seconds                                 nervous_rosalind
$ cp ..
$ docker cp ContaminationAnalyser/ de513c9e2123:/opt/
```

Return to the container terminal you can change to the directory where the CSA files were copied and reun the software:

```commandline
cd /opt/ContaminationAnalyser/
%run Main.py
```


# Production Repo for Face Profile
This repo contains the code to develop the facial model.  The endpoints will take in a portrait of a human face.  It will be deployed to UbiOps deployments which makes it available as a REST endpoint.

## Using this Template
There is a process that updates `./deployment_package` and deploys it as `./deployment_package.zip`.  Within `./deployment_package` there are several components as follows:
1. `deployment.py` imports `mod.core` which contains a class called `Deployment` which is called in the setup phase of deployment to the UbiOps service.  This file will be the same in all deployments
2. `libraries/` contains the project directories for library dependencies, namely `prcvd` and `mod`.
    1. `prcvd` is a library that contains code for implementing data science on conversational data streams audio and video.  This library is the same in all deployments.
    2. `mod` is a library that contains the deployment, model updating and versioning code, as well as the client (Maybe in future iterations, the client will be made its own library).  This library changes depending on the deployment.
3. The `deployment_package` is reproducible by running cells in the notebook called `./nbs/00_core.ipynb` so if you're interested in how `deployment_package` is created in more detail, look there.
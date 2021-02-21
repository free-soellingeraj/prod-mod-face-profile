# Production Repo for Face Profile
This repo contains the code to develop the facial model REST endpoint.  The endpoints will take in a portrait of a human face.  It will be deployed to UbiOps deployments which makes it available as a REST endpoint.

## Instructions
1. clone this repo
2. copy your model into `./deployment_package/`, call it `model1.pkl`
3. Run the cells in `00_core.ipynb`
4. Update any requirements not in the example `00_core.ipynb` in a cell with `#export` at the top of the cell, and in the cell that creates the `requirements.txt` file (near the top of the notebook)
5. Update the `Deployment` class to load your model up in the `Deployment.__init__` function and to execute a single request in `Deployment.request` (one invocation of `Deployment.model.predict`)
6. Define the `input_spec.json` and `output_spec.json` to include the metadata about your inputs and outputs from request. (For format, see the examples `ubiops_input_spec.json` and `ubiops_output_spec.json`) 
7. Get a UbiOps API key and save it somewhere.
8. One major benefit of using the notebook approach is that you can test whether the `Deployment` class works locally, which is very helpful as you begin to see bugs pushing to production.  So, test it!  You can see the example directly below the definition of `Deployment`.


## Layout of this Template
There is a process that updates `./deployment_package` and deploys it as `./deployment_package.zip`.  Within `./deployment_package` there are several components as follows:
1. `deployment.py` imports `mod.core` which contains a class called `Deployment` which is called in the setup phase of deployment to the UbiOps service.  This file will be the same in all deployments
2. `libraries/` contains the project directories for library dependencies, namely `prcvd` and `mod`.
    1. `prcvd` is a library that contains code for implementing data science on conversational data streams audio and video.  This library is the same in all deployments.
    2. `mod` is a library that contains the deployment, model updating and versioning code, as well as the client (Maybe in future iterations, the client will be made its own library).  This library changes depending on the deployment.
3. The `deployment_package` is reproducible by running cells in the notebook called `./nbs/00_core.ipynb` so if you're interested in how `deployment_package` is created in more detail, look there.
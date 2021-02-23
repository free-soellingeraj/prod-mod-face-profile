# Production Repo for Face Profile
> This repo contains the code to develop the facial model REST endpoint.  The endpoints will take in a portrait of a human face.  It will be deployed to UbiOps deployments which makes it available as a REST endpoint.


## Instructions
1. clone this repo
2. configure `00_core.ipynb` to fit your stack / use case
3. execute cells: the cells will handle the deployment

### Model Files (e.g. `depoyment_package/model1.pkl`)
Copy your model into `./deployment_package/`, call it `model1.pkl`
### Requirements (`deployment_package/requirements.txt`)
Update any requirements not in the example `00_core.ipynb` in a cell with `#export` at the top of the cell, and in the cell that creates the `requirements.txt` file (near the top of the notebook)
### Deployment loader (`Deployment.__init__`)
Update the `Deployment` class to load your model up in the `Deployment.__init__` function and to execute a single request in `Deployment.request` (one invocation of `Deployment.model.predict`)
### Input / Output Specification (`*_input_spec.json` and `*_output_spec.json`)
Define the `input_spec.json` and `output_spec.json` to include the metadata about your inputs and outputs from request. (For format, see the examples `ubiops_input_spec.json` and `ubiops_output_spec.json`) 
### UbiOps Auth
Get a UbiOps API key and save it somewhere.
### Local Notebook Test
One major benefit of using the notebook approach is that you can test whether the `Deployment` class works locally, which is very helpful as you begin to see bugs pushing to production.  So, test it!  You can see the example directly below the definition of `Deployment`.
### Regenerate the `deployment_package`
1. create/update `requirements.txt`
2. create/update `libraries/{mod}` (e.g. `prod-mod-face-profle`): this notebook is configured to copy the last saved state of every file in the `{mod}` python module, delete some unnecessary files (e.g. the `.git` directory, etc..) and save that under `deployment_package/libraries`
3. add in any other library dependencies.  The current version of this template is configured to `pip install` any library found in `deployment_package/libraries` __in no particular order__.  Warning: if your libraries need to be installed in a specific order, that is currently not supported.  It can be accomplished by altering the installation code found in `deployment.py`.  In the future, I will find a general way of supplying installation order, but I haven't thought of that yet.
4. create/update intput output `_spec` files.
5. zip it up into `deployment_package.zip`
### Define the Deployment Params
1. Provide an existing UbiOps project (e.g. facial-profile)
2. Define a name for your deployment (e.g. endtoend-N)
3. Define a version

This notebook is configured to attempt to push a deployment version, and if it fails, it will try to iterate the version.  The versioning naming convention used is just "v{i}" where i is an integer.  The maximum number of versions that can exist on a deployment is 5, so at 5 one may have to delete some past ones.  

It is also possible to use a UbiOps revision, which changes certain aspects of an existing version.
### Deploy and Build
The bottom cells in the notebook deploy
## Layout of this Template
There is a process that updates `./deployment_package` and deploys it as `./deployment_package.zip`.  Within `./deployment_package` there are several components as follows:
1. `deployment.py` imports `mod.core` which contains a class called `Deployment` which is called in the setup phase of deployment to the UbiOps service.  This file will be the same in all deployments
2. `libraries/` contains the project directories for library dependencies, namely `prcvd` and `mod`.
    1. `prcvd` is a library that contains code for implementing data science on conversational data streams audio and video.  This library is the same in all deployments.
    2. `mod` is a library that contains the deployment, model updating and versioning code, as well as the client (Maybe in future iterations, the client will be made its own library).  This library changes depending on the deployment.
3. The `deployment_package` is reproducible by running cells in the notebook called `./nbs/00_core.ipynb` so if you're interested in how `deployment_package` is created in more detail, look there.

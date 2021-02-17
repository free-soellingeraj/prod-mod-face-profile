# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb (unless otherwise specified).

__all__ = ['Deployment']

# Cell
import sys; import os
from pathlib import Path
import io
import skimage
from skimage import color
from prcvd.img.core import (
    TrainedSegmentationModel, MaskedImg
)
from prcvd.img.face import (
    FacialProfile
)

# Cell
class Deployment:
    def __init__(self, base_directory:str, context):
        """
        Initialisation method for the deployment. It can for example be used for loading modules that have to be kept in
        memory or setting up connections. Load your external model files (such as pickles or .h5 files) here.
        :param str base_directory: absolute path to the directory where the deployment.py file is located
        :param dict context: a dictionary containing details of the deployment that might be useful in your code.
            It contains the following keys:
                - deployment (str): name of the deployment
                - version (str): name of the version
                - input_type (str): deployment input type, either 'structured' or 'plain'
                - output_type (str): deployment output type, either 'structured' or 'plain'
                - language (str): programming language the deployment is running
                - environment_variables (str): the custom environment variables configured for the deployment.
                    You can also access those as normal environment variables via os.environ
        """
        global get_y_fn
        get_y_fn = lambda x: print('prod')
        print("Loading face segmentation model.")
        print('base_directory', base_directory)
        print('context', context)
        self.basedir = Path(base_directory)
        self.mod_fp = self.basedir/'checkpoint_20201007'
        self.output_classes = [
            'Background/undefined', 'Lips', 'Eyes', 'Nose', 'Hair',
            'Ears', 'Eyebrows', 'Teeth', 'General face', 'Facial hair',
            'Specs/sunglasses'
        ]
        self.size = 224
        self.mod_fp = self.basedir/"checkpoint_20201007"
        self.model = TrainedSegmentationModel(
            mod_fp=self.mod_fp,
            input_size=self.size,
            output_classes=self.output_classes
        )


    def request(self, data, attempt=1):
        """
        Method for deployment requests, called separately for each individual request.
        :param dict/str data: request input data. In case of deployments with structured data, a Python dictionary
            with as keys the input fields as defined upon deployment creation via the platform. In case of a deployment
            with plain input, it is a string.
                - img: list, data from image
                - sampling_strategy: str, 'use_all' | ...
                - align_face: bool, yes/no apply face alignment
                - num_attempts: int, max attempts before failure (sometimes face alignment fails)

        :return dict/str: request output. In case of deployments with structured output data, a Python dictionary
            with as keys the output fields as defined upon deployment creation via the platform. In case of a deployment
            with plain output, it is a string. In this example, a dictionary with the key: output.
        """
        img = MaskedImg()
        img.load_from_nparray(
            data['img']
        ) # possibly need to tx list -> np

        try:
            profile = FacialProfile(
                model=self.model,
                img=img,
                sampling_strategy=data['sampling_strategy'],
                align_face=data['align_face']
            )

        except:
            if not attempt > data['num_attempts']:
                return self.request(
                    data=data,
                    attempt=attempt+1,
                )
            else:
                return None, None

        plt.figure(figsize=(10,10))
        plt.imshow(profile.segmask.decoded_img.img)
        plt.imshow(
            skimage.color.label2rgb(np.array(profile.segmask.mask)),
            alpha=0.3
        )
        plt.title('Computed fWHR based on Segmentation Only (not FaceMesh).\nfWHR: {}'.format(profile.fwhr))
        plt.scatter(x=[profile.bizygomatic_right[0]],
                    y=[profile.bizygomatic_right[1]],
                    marker='+', c='orange')
        plt.scatter(x=[profile.bizygomatic_left[0]],
                    y=[profile.bizygomatic_left[1]],
                    marker='+', c='orange')
        plt.plot(
            [profile.bizygomatic_right[0], profile.bizygomatic_right[0]],
            [0, profile.segmask.mask.shape[1]-1],'ro-')
        plt.plot(
            [profile.bizygomatic_left[0], profile.bizygomatic_left[0]],
            [0, profile.segmask.mask.shape[1]-1],'ro-')

        plt.scatter(x=[profile.upperfacial_top[0]],
                    y=[profile.upperfacial_top[1]],
                    marker='+', c='red')
        plt.plot(
            [0, profile.segmask.mask.shape[0]-1],
            [profile.upperfacial_top[1], profile.upperfacial_top[1]],
            'go-'
        )

        plt.scatter(x=[profile.upperfacial_bottom[0]],
                    y=[profile.upperfacial_bottom[1]],
                    marker='+', c='red')
        plt.plot(
            [0, profile.segmask.mask.shape[0]-1],
            [profile.upperfacial_bottom[1], profile.upperfacial_bottom[1]], 'go-')

        outfp = self.basedir / 'tmp.jpeg'
        plt.savefig(outfp, format='jpeg')
        outimg = MaskedImg()
        outimg.load_from_file(fn=outfp)
        outfp.unlink()

        row = profile.get_profile()
        row['model_id'] = self.mod_fp

        return {'row': row, 'img':outimg.img}
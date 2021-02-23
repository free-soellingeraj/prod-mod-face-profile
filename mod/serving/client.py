# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/16_serving_client.ipynb (unless otherwise specified).

__all__ = ['RequestData', 'Client']

# Cell
import os
import requests
from ..exceptions import  (
    UnexpectedInputProvided, ExpectedInputMissing,
    DataTypeNotImplemented
)

# Cell
class RequestData:
    def __init__(self, spec):
        """Factory base class for request data."""
        self.spec = spec
        self.id_to_spec = {}
        self.name_to_spec = {}
        for obj in self.spec:
            self.id_to_spec[obj['id']] = obj
            self.name_to_spec[obj['name']] = obj

        self.type_transforms = {
            "int": self._tx_int,
            "double": self._tx_double,
            "blob": self._tx_blob,
            "bool": self._tx_bool,
            "string": self._tx_str,
            "array_int": self._tx_arrayint
        }


    def make_instance(self, data):
        """
        Takes in raw data in python representation,
        outputs required format for the request.

        In:
            data, dict: contains the data in the native format
        Out:
            data, dict: the format defined by the deployment client. e.g. http post
        """
        tx_data = {}
        for name in self.name_to_spec.keys():
            if name not in data:
                raise MissingInput(
                    ' '.join([
                        'Required input missing from spec: "{}"'])
                    .format(name)
                )

        for k, v in data.items():
            if k not in self.name_to_spec:
                raise UnexpectedInputProvided(
                    ' '.join([
                        'Unexpected input found in',
                        'request formation: "{}"'])
                    .format(k)
                )

            var_spec = self.name_to_spec[k]
            data_type = var_spec['data_type']['value']
            if data_type not in self.type_transforms:
                raise DataTypeNotImplemented(
                    'Request contains data type without defined behavior.',
                    'See client.RequestData missing {}'.format(data_type)
                )
            tx_data[k] = self.type_transforms[data_type](v)

        return tx_data


    def _tx_int(self, v):
        """Returns int value to be sent in request."""
        return v


    def _tx_bool(self, v):
        """Returns bool value to be sent in request."""
        return v


    def _tx_double(self, v):
        """Returns double value to be sent in request."""
        return v


    def _tx_str(self, v):
        """Returns str value to be sent in request."""
        return v


    def _tx_blob(self, v):
        """Returns blob value to be sent in request."""
        return v

    def _tx_arrayint(self, v):
        return v


class Client:
    def __init__(self, project_name, deployment_name,
                 deployment_version, input_spec,
                 output_spec, api_key, api_host):
        self.project_name = project_name
        self.deployment_name = deployment_name
        self.deployment_version = deployment_version
        self.input_spec = input_spec #dict
        self.output_spec = output_spec #dict
        self.api_key = api_key
        self.api_host = api_host


    def request(self, data):
        """Source the HTTP response."""
        tx_data = self.input_factory.make_instance(data=data)
        r = requests.post(
            self.req_url, json=tx_data, headers={
                "Authorization": self.api_key,  #TODO: generalize this
            }
        )
        return r


    def post_process(self, response):
        """Deal with the HTTP response."""
        if response.ok:
            output = json.loads(response.content)
        else:
            raise Exception("Failed HTTP request, no return.")

        return {
            self.id_to_spec[k]['name']: self.output_factory(v)
                for k, v in output['result'].items()
        }
import numpy as np
import pystache

from typing import Iterable


class MakefileTemplate(pystache.TemplateSpec):
    template_name = "Makefile"

    def __init__(
            self,
            source_files: Iterable[str],
            header_files: Iterable[str],
            bin_name: str,
            compiler_name: str,
    ):
        self.source_files = list(source_files)
        self.header_files = list(header_files)
        self.bin_name = bin_name
        self.compiler = compiler_name


# TODO Check if definition of the simple templates using a dataclass is possible
class DatasetHeaderTemplate(pystache.TemplateSpec):
    template_name = "test_dataset_h"

    def __init__(self, data_type: str, dataset_size: int, input_size: int, output_size: int):
        self.data_type = data_type
        self.dataset_size = dataset_size
        self.input_size = input_size
        self.output_size = output_size


class DatasetSourceTemplate(pystache.TemplateSpec):
    template_name = "test_dataset_c"

    def __init__(self, data_type: str, dataset: np.array):
        self.data_type = data_type
        self.dataset = []
        for d in dataset:
            self.dataset.append("{" + ", ".join(str(v) for v in d.flatten(order="C")) + "}")


class MainTemplate(pystache.TemplateSpec):
    template_name = "main_c"

    def __init__(self, data_type: str):
        self.data_type = data_type


class ActivationFunctionHeaderTemplate(pystache.TemplateSpec):
    template_name = "activation_function_h"

    def __init__(self, activation_declarations: Iterable[str]):
        self.declarations = activation_declarations


class ActivationFunctionSourceTemplate(pystache.TemplateSpec):
    template_name = "activation_function_c"

    def __init__(self, activation_definitions: Iterable[str]):
        self.definitions = activation_definitions


class InferenceSourceTemplate(pystache.TemplateSpec):
    template_name = "inference_c"

    def __init__(self, data_type: str):
        self.data_type = data_type


# TODO
class InferenceHeaderTemplate(pystache.TemplateSpec):
    template_name = "inference_h"

    def __init__(self, layers):
        self.layers = layers


class LayersHeaderTemplate(pystache.TemplateSpec):
    template_name = "layers_hpp"

    def __init__(
            self,
            has_input: bool = False,
            has_convolution2D: bool = False,
            has_max_pooling2D: bool = False,
            has_average_pooling2D: bool = False,
            has_dense: bool = False,
            has_softmax: bool = False,
    ):
        self.has_input = has_input
        self.has_convolution2D = has_convolution2D
        self.has_max_pooling2D = has_max_pooling2D
        self.has_average_pooling2D = has_average_pooling2D
        self.has_dense = has_dense
        self.has_softmax = has_softmax

# TODO
class GlobalsTemplate(pystache.TemplateSpec):
    template_name = "global_vars_c"

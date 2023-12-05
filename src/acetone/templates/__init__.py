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


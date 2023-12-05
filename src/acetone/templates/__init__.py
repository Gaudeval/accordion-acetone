import pystache


class MakefileTemplate(pystache.TemplateSpec):
    template_name = "Makefile"

    def __init__(
            self,
            source_files: list[str],
            header_files: list[str],
            bin_name: str,
            compiler_name: str,
    ):
        self.source_files = source_files
        self.header_files = header_files
        self.bin_name = bin_name
        self.compiler = compiler_name

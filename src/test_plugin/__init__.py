from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class MyParserOneEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description="Custom configuration parameter")

    def load(self):
        from nomad_aa_plugin.parsers.parser import MyParserOne

        return MyParserOne(**self.dict())


parser_one_entry_point = MyParserOneEntryPoint(
    name="MyParserOne",
    description="My parser entry point configuration.",
    mainfile_name_re=r".+\.nxs",
)

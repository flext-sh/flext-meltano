from enum import StrEnum, unique

@unique
class PluginType(StrEnum):
    EXTRACTORS = "extractors"
    LOADERS = "loaders"
    TRANSFORMS = "transforms"
    ORCHESTRATORS = "orchestrators"
    TRANSFORMERS = "transformers"
    MAPPINGS = "mappings"
    UTILITY = "utility"
    COMMAND = "command"

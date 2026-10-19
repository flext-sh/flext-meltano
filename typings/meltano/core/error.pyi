# Copyright (c) 2026 FLEXT Team. All rights reserved.

class Error(Exception): ...
class MeltanoError(Error): ...

# External class objects consumed as exception handlers, not owned declarations.
EmptyMeltanoFileException: type[MeltanoError]
ProjectNotFound: type[Error]

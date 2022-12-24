from typing import Optional, Any, Type


class Finger:
    __CHARACTERISTICS_IDENTIFIER_TYPE = None
    __CHARACTERISTICS_IDENTIFIER_TYPE_DEFAULT = str

    @classmethod
    def set_characteristics_identifier_type(cls, target_type: Type = __CHARACTERISTICS_IDENTIFIER_TYPE_DEFAULT):
        if cls.__CHARACTERISTICS_IDENTIFIER_TYPE is not None:
            raise RuntimeError(
                "RuntimeError: You can't change the type of 'CHARACTERISTICS_IDENTIFIER' in same runtime.\n"
                f"Note: default is set to '{cls.__CHARACTERISTICS_IDENTIFIER_TYPE_DEFAULT}'"
            )

        cls.__CHARACTERISTICS_IDENTIFIER_TYPE = target_type

    def __init__(self, template_id: int, characteristics_identifier: Optional[__CHARACTERISTICS_IDENTIFIER_TYPE] = None,
                 confidence: Optional[int] = None):
        if Finger.__CHARACTERISTICS_IDENTIFIER_TYPE is None:
            Finger.set_characteristics_identifier_type()

        self.__template_id: int = template_id
        self.__characteristics_identifier: \
            Optional[Finger.__CHARACTERISTICS_IDENTIFIER_TYPE] = characteristics_identifier
        self.__confidence: Optional[int] = confidence

    @property
    def template_id(self) -> int:
        return self.__template_id

    @property
    def characteristics_identifier(self) -> Optional[__CHARACTERISTICS_IDENTIFIER_TYPE]:
        return self.__characteristics_identifier

    @property
    def confidence(self) -> int:
        return self.__confidence

    def __str__(self) -> str:
        return f"<{self.characteristics_identifier}> #{self.template_id} ({self.confidence})"

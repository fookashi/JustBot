from pydantic import BaseModel as PydanticBaseModel


class DatabaseModel(PydanticBaseModel):
    class Config:
        from_attributes = True

    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})

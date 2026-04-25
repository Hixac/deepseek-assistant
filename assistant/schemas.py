import json

from pydantic import BaseModel


# {
#     "new_chat": [bool? = true],
#     "expert_mode": [bool? = false],
# 
#     "msg": [string],
#     "rules": [string?],
#     "context": [string?],
# }

class Protocol(BaseModel):
    new_chat: bool = True
    expert_mode: bool = False

    msg: str
    rules: str | None = None
    context: str | None = None

    def get_query(self) -> str:
        data = {
            "msg": self.msg
        }
        if self.rules is not None:
            data["rules"] = self.rules
        if self.context is not None:
            data["context"] = self.context

        return json.dumps(data)

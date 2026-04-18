from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from mcdreforged.api.types import PluginServerInterface
from pydantic import BaseModel

from .config import Config

app = FastAPI()
bearer_scheme = HTTPBearer()

__server: PluginServerInterface
__config: Config


class ExecuteRequest(BaseModel):
    command: str


def verify_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    if credentials.credentials != __config.token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials


@app.post("/execute")
async def execute_command(
        request: ExecuteRequest,
        _token: str = Security(verify_token),
):
    __server.execute_command(request.command)
    return {"status": "ok", "command": request.command}


def on_load(server: PluginServerInterface, prev_module):
    # mount if fastapi_mcdr is ready
    global __server, __config
    __server = server
    __config = server.load_config_simple(target_class=Config)

    fastapi_mcdr = server.get_plugin_instance('fastapi_mcdr')
    if fastapi_mcdr is not None and fastapi_mcdr.is_ready():
        mount_app(server)

    server.register_event_listener(
        fastapi_mcdr.COLLECT_EVENT,
        mount_app
    )


def on_unload(server: PluginServerInterface):
    # save plugin id and fastapi_mcdr instance
    id_ = server.get_self_metadata().id
    fastapi_mcdr = server.get_plugin_instance('fastapi_mcdr')

    # unmount app
    fastapi_mcdr.unmount(id_)


def mount_app(server: PluginServerInterface):
    # save plugin id and fastapi_mcdr instance
    id_ = server.get_self_metadata().id
    fastapi_mcdr = server.get_plugin_instance('fastapi_mcdr')

    # mount app
    fastapi_mcdr.mount(id_, app)

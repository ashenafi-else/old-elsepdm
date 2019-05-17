from celery.utils.log import get_task_logger

from app.celery_app import app
from elsecommon.transports.router import Router
from elsepublic.elsedam.dto.remove_assets_from_buffer_operation import RemoveAssetsFromBufferParameters
from elsepublic.elsedam.interfaces.remove_assets_from_buffer_operation import RemoveAssetsFromBufferOpInterface

logger = get_task_logger(__name__)


@app.task
def remove_buffered_assets():
    remove_assets = Router[RemoveAssetsFromBufferOpInterface.uri]
    remove_assets(RemoveAssetsFromBufferParameters())
    # todo figure out with transport and implement background buffered and dam assets removing
    print('remove_buffered_assets START')

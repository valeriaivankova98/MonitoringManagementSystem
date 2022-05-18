import grpc
import yandexcloud


from yandex.cloud.resourcemanager.v1.cloud_service_pb2 import ListCloudsRequest
from yandex.cloud.resourcemanager.v1.cloud_service_pb2_grpc import CloudServiceStub
from yandex.cloud.resourcemanager.v1.folder_service_pb2 import ListFoldersRequest
from yandex.cloud.resourcemanager.v1.folder_service_pb2_grpc import FolderServiceStub

from yandex.cloud.compute.v1.zone_service_pb2 import ListZonesRequest  # for creating uses
from yandex.cloud.compute.v1.zone_service_pb2_grpc import ZoneServiceStub

# from yandex.cloud.compute.v1.instance_pb2 import Instance
from yandex.cloud.compute.v1.instance_service_pb2 import (
    ListInstancesRequest,
    StartInstanceRequest,
    StopInstanceRequest,
    RestartInstanceRequest,
    StartInstanceMetadata,
    StopInstanceMetadata,
    RestartInstanceMetadata
)
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub


from database import get_user_data


def _prep_client(user_id, folder=True):
    user_data = get_user_data(user_id)
    if user_data is None or not user_data['token']:
        raise('Token not set! Please set folder first using /settoken {token}')
    if folder and not user_data['folder']:
        raise('Folder not set! Please set folder first using /setfolder {folder_name}')
    interceptor = yandexcloud.RetryInterceptor(max_retry_count=5, retriable_codes=[grpc.StatusCode.UNAVAILABLE])
    sdk = yandexcloud.SDK(interceptor=interceptor, token=user_data['token'])
    if folder:
        return (sdk, user_data['folder'])
    return sdk


def list_clouds(user_id):
    sdk = _prep_client(user_id, folder=False)
    cloud_service = sdk.client(CloudServiceStub)
    try:
        operation = cloud_service.List(ListCloudsRequest())
        ret = ''
        for cloud in operation.clouds:
            ret += f'{cloud.name}(id "{cloud.id}")\n'
        if ret == '':
            return 'No clouds found! Create a cloud first to use this bot'
        return ret
    except grpc.RpcError as e:
        print(e.details())
        status_code = e.code()
        print(status_code.name)
        print(status_code.value)


def list_folders(user_id, cloud_id):
    sdk = _prep_client(user_id, folder=False)
    cloud_service = sdk.client(FolderServiceStub)
    try:
        operation = cloud_service.List(ListFoldersRequest(cloud_id=cloud_id))
        ret = ''
        for folder in operation.folders:
            ret += f'{folder.name}(id "{folder.id}")\n'
        if ret == '':
            return f'No folders found in cloud {cloud_id}'
        return ret
    except grpc.RpcError as e:
        print(e.details())
        status_code = e.code()
        print(status_code.name)
        print(status_code.value)


def list_zones(user_id):
    sdk = _prep_client(user_id, folder=False)
    zone_service = sdk.client(ZoneServiceStub)
    try:
        operation = zone_service.List(ListZonesRequest())
        ret = ''
        for zone in operation.zones:
            ret += f'{zone.name}(id "{zone.id}")\n'
        if ret == '':
            return 'No zones are currently available'
        return ret
    except grpc.RpcError as e:
        print(e.details())
        status_code = e.code()
        print(status_code.name)
        print(status_code.value)


def list_vm(user_id):
    (sdk, folder_id) = _prep_client(user_id)
    # res = ''
    instance_service = sdk.client(InstanceServiceStub)
    try:
        operation = instance_service.List(ListInstancesRequest(
            folder_id=folder_id
        ))
        ret = ''
        for instance in operation.instances:
            ret += f'{instance.name}(id "{instance.id}")\n'
        if ret == '':
            return f'No vms found in folder {folder_id}'
        return ret
    except grpc.RpcError as e:
        print(e.details())
        status_code = e.code()
        print(status_code.name)
        print(status_code.value)


def start_vm(user_id, instance_id):
    (sdk, folder_id) = _prep_client(user_id)
    # res = ''
    instance_service = sdk.client(InstanceServiceStub)
    operation = instance_service.Start(StartInstanceRequest(
        instance_id=instance_id
    ))
    operation_result = sdk.wait_operation_and_get_result(
        operation,
        meta_type=StartInstanceMetadata,
    )
    return operation_result


def stop_vm(user_id, instance_id):
    (sdk, folder_id) = _prep_client(user_id)
    # res = ''
    instance_service = sdk.client(InstanceServiceStub)
    operation = instance_service.Stop(StopInstanceRequest(
        instance_id=instance_id
    ))
    operation_result = sdk.wait_operation_and_get_result(
        operation,
        meta_type=StopInstanceMetadata,
    )
    return operation_result


def restart_vm(user_id, instance_id):
    (sdk, folder_id) = _prep_client(user_id)
    # res = ''
    instance_service = sdk.client(InstanceServiceStub)
    operation = instance_service.Restart(RestartInstanceRequest(
        instance_id=instance_id
    ))
    operation_result = sdk.wait_operation_and_get_result(
        operation,
        meta_type=RestartInstanceMetadata,
    )
    return operation_result

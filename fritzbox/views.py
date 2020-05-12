from django.http import HttpResponse, JsonResponse
from django.template import loader

from fritzbox.fritzconnection.fritzconnection import FritzConnection
from fritzbox.fritzconnection.fritzhosts import FritzHosts
from fritzbox.fritzconnection.fritzstatus import FritzStatus
from fritzbox.fritzconnection.fritzwlan import FritzWLAN
from fritzbox.models import BoxConfig



# https://github.com/stbkde/fritzconnection/blob/master/fritzconnection/fritzwlan.py
from timeline.utils import first


def index(request):
    """
    main page

    :param request: request
    :return: response
    """

    fritz_box_configurations = []

    for config in BoxConfig.objects.all():
        fritz_box_configurations.append(config.id)

    template = loader.get_template('fritzbox/dashboard.html')
    context = {
        'title': 'Dashboard',
        'configurations': fritz_box_configurations
    }
    return HttpResponse(template.render(context, request))


def check(request, box_config_id):
    """
    check for boxes

    :param box_config_id:
    :param request: request
    :return: response
    """
    try:
        box_config = BoxConfig.objects.get(pk=box_config_id)
    except BoxConfig.DoesNotExist:
        box_config = None

    connection = FritzConnection(address=box_config.address, user=box_config.user, password=box_config.password)

    response_data = {
        'address': box_config.address,
        'user': box_config.user,
        'password': box_config.password,
        'modelname': connection.modelname
    }

    return JsonResponse(response_data)


def wifi(request, box_config_id):
    """
    wifi information

    :param box_config_id:
    :param request: request
    :return: response
    """
    try:
        box_config = BoxConfig.objects.get(pk=box_config_id)
    except BoxConfig.DoesNotExist:
        box_config = None

    fritz_wlan = FritzWLAN(address=box_config.address, user=box_config.user, password=box_config.password) # umzug4436
    wlan_ext_info = fritz_wlan.get_wlan_ext_info()
    #print("wlan_ext_info: %s" % wlan_ext_info)
    host_numbers = fritz_wlan.host_numbers
    hosts_info = fritz_wlan.get_hosts_info()
    device_list_path = fritz_wlan.device_list_path

    fritz_hosts = FritzHosts(address=box_config.address, user=box_config.user,
                             password=box_config.password)
    get_hosts_info = fritz_hosts.get_hosts_info()

    wifi_devices = []

    for device in device_list_path['items']:
        try:
            host = first( get_hosts_info, condition=lambda x: x['ip'] == device['ip'])['name']
            # host = get_hosts_info[0]['ip']
        except StopIteration as e:
            host = '-'

        item = {
            'name': host,
            'mac': device['mac'],
            'ip': device['ip'],
            'speed': device['speed']
        }
        wifi_devices.append(item)

    response_data = {
        'ssid': fritz_wlan.ssid,
        'bssid': fritz_wlan.bssid,
        'wlan_ext_info': wlan_ext_info,
        'host_numbers': host_numbers,
        'hosts_info': hosts_info,
        'total_associations': device_list_path['total_associations'],
        'clients': wifi_devices
    }

    return JsonResponse(response_data)


def hosts(request, box_config_id):
    """
    hosts information

    :param box_config_id:
    :param request: request
    :return: response
    """
    try:
        box_config = BoxConfig.objects.get(pk=box_config_id)
    except BoxConfig.DoesNotExist:
        box_config = None

    fritz_hosts = FritzHosts(address=box_config.address, user=box_config.user, password=box_config.password) # umzug4436
    #get_hosts_info = fritz_hosts.get_hosts_info()
    get_hosts_info = fritz_hosts.get_hosts_info_ext()

    response_data = {
        'get_hosts_info': get_hosts_info,
    }

    return JsonResponse(response_data)


def status(request, box_config_id):
    """
    monitor dsl information

    :param box_config_id:
    :param request: request
    :return: response
    """
    try:
        box_config = BoxConfig.objects.get(pk=box_config_id)
    except BoxConfig.DoesNotExist:
        box_config = None

    fritz_status = FritzStatus(address=box_config.address)
    upstream_str, downstream_str = fritz_status.str_max_bit_rate

    response_data = {
        'is_connected': fritz_status.is_connected,
        'wan_access_type': fritz_status.wan_access_type,
        'upstream_str': upstream_str,
        'downstream_str': downstream_str,
        'uptime': fritz_status.uptime,
        'uptime_str': fritz_status.str_uptime,
    }

    return JsonResponse(response_data)
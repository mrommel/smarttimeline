# -*- coding: utf-8 -*-

"""
fritzwlan.py
Utility modul for FritzConnection to list the known WLAN connections.
Based on fritzhosts from Klaus Bremer https://bitbucket.org/kbr/fritzconnection
License: MIT https://opensource.org/licenses/MIT
Author: Bernd Strebel
"""

import os, argparse

# tiny hack to run this as a package but also from the command line. In
# the latter case ValueError is raised from python 2.7 and SystemError
# from Python 3.5, and ImportError by Python 3.6
from xml.etree import ElementTree

import requests

from fritzbox.fritzconnection import fritzconnection

__version__ = '0.6.5'

SERVICE = 'WLANConfiguration'

# version-access:
def get_version():
    return __version__


class FritzWLAN(object):

    def __init__(self,
                 fc=None,
                 address=fritzconnection.FRITZ_IP_ADDRESS,
                 port=fritzconnection.FRITZ_TCP_PORT,
                 user=fritzconnection.FRITZ_USERNAME,
                 password='',
                 service=1):
        super(FritzWLAN, self).__init__()
        if fc is None:
            fc = fritzconnection.FritzConnection(address, port, user, password)
        self.fc = fc
        self.service = service

    def action(self, actionname, **kwargs):
        service = '{}:{}'.format(SERVICE, self.service)
        return self.fc.call_action(service, actionname, **kwargs)

    @property
    def modelname(self):
        return self.fc.modelname

    @property
    def info(self):
        result = self.action('GetInfo')
        return result

    @property
    def ssid(self):
        return self.info['NewSSID']

    @property
    def bssid(self):
        return self.info['NewBSSID']

    @property
    def device_list_path(self):
        result = self.action('X_AVM-DE_GetWLANDeviceListPath')
        link = result['NewX_AVM-DE_WLANDeviceListPath']

        url = 'http://%s:%s%s' % (self.fc.address, self.fc.port, link)

        # sending get request and saving the response as response object
        response = requests.get(url=url)

        # extracting data in xml format
        root = ElementTree.fromstring(response.content)

        total_associations = root.findtext('TotalAssociations')
        items = []

        for item in root.findall('Item'):
            # AssociatedDeviceIndex
            mac = item.findtext('AssociatedDeviceMACAddress')
            ip = item.findtext('AssociatedDeviceIPAddress')
            # AssociatedDeviceAuthState
            speed = item.findtext('X_AVM-DE_Speed')
            signal_strength = item.findtext('X_AVM - DE_SignalStrength')
            # AssociatedDeviceChannel
            # AssociatedDeviceGuest

            items.append({ 'mac': mac, 'ip': ip, 'speed': speed, 'signal_strength': signal_strength })

        result = {
            'total_associations': total_associations,
            'items': items
        }

        return result

    @property
    def host_numbers(self):
        result = self.action('GetTotalAssociations')
        return result['NewTotalAssociations']

    def get_generic_host_entry(self, index):
        result = self.action('GetGenericAssociatedDeviceInfo', NewAssociatedDeviceIndex=index)
        return result

    def get_specific_host_entry(self, mac_address):
        result = self.action('GetSpecificAssociatedDeviceInfo', NewAssociatedDeviceMACAddress=mac_address)
        return result

    def get_wlan_ext_info(self):
        result = self.action('X_AVM-DE_GetWLANExtInfo')
        return result

    def get_hosts_info(self):
        """
        Returns a list of dicts with information about the known hosts.
        The dict-keys are: 'auth', 'mac', 'ip', 'signal', 'speed'
        """
        result = []
        index = 0
        while index < self.host_numbers:
            host = self.get_generic_host_entry(index)
            if host:
                result.append({
                    'service': self.service,
                    'index': index,
                    'status': host['NewAssociatedDeviceAuthState'],
                    'mac': host['NewAssociatedDeviceMACAddress'],
                    'ip': host['NewAssociatedDeviceIPAddress'],
                    'signal': host['NewX_AVM-DE_SignalStrength'],
                    'speed': host['NewX_AVM-DE_Speed']
                })
            index += 1
        return result


# ---------------------------------------------------------
# terminal-output:
# ---------------------------------------------------------


def _print_header(fh):
    print('\nFritzHosts:')
    print('{:<30}{}'.format('version:', get_version()))
    print('{:<30}{}'.format('model:', fh.modelname))
    print('{:<30}{}'.format('ip:', fh.fc.address))


def print_hosts(fh):
    print('\n{}:{}\n'.format(SERVICE, fh.service))
    print('{:>5} {:<7} {:<15} {:<17} {:<7} {:>7} {:>7}\n'.format(
        'index', 'status', 'ip', 'mac', 'service', 'signal', 'speed'))
    hosts = fh.get_hosts_info()
    for index, host in enumerate(hosts):
        status = 'active' if host['status'] == '1' else  '-'
        ip = '-' if host['ip'] == None else host['ip']
        mac = '-' if host['mac'] == None else host['mac']
        print('{:>4}: {:<7} {:<15} {:<17} {:<7} {:>7} {:>7}'.format(
            host['index'],
            status,
            ip,
            mac,
            host['service'],
            host['signal'],
            host['speed'],
            )
        )


def _print_detail(fh, detail, quiet):
    mac_address = detail[0].lower()
    info = fh.get_specific_host_entry(mac_address)
    if info:
        if not quiet:
            print('\n{:<30}{}'.format('Details for host:', mac_address))
            print('{:<30}{}:{} ({})\n'.format('', SERVICE, fh.service, fh.host_numbers))
            for key, value in info.items():
                print('{:<30}: {}'.format(key, value))
        else: print(info['NewAssociatedDeviceAuthState'])
    else:
        if quiet: print('0')


def _print_nums(fh):
    print('{}:{} {}'.format(SERVICE, fh.service, fh.host_numbers))

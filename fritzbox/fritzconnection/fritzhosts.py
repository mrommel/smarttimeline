# -*- coding: utf-8 -*-

"""
fritzhosts.py

Utility modul for FritzConnection to list the known hosts.

Older versions of FritzOS lists only up to 16 entries.
For newer versions this limitation is gone.

License: MIT https://opensource.org/licenses/MIT
Source: https://bitbucket.org/kbr/fritzconnection
Author: Klaus Bremer
"""

import os, argparse

# tiny hack to run this as a package but also from the command line. In
# the latter case ValueError is raised from python 2.7,
# SystemError from Python 3.5
# ImportError from Python 3.6
from xml.etree import ElementTree

import requests

from fritzbox.fritzconnection import fritzconnection


__version__ = '0.6.2'

SERVICE = 'Hosts'


# version-access:
def get_version():
    return __version__


class FritzHosts(object):

    def __init__(self,
                 fc=None,
                 address=fritzconnection.FRITZ_IP_ADDRESS,
                 port=fritzconnection.FRITZ_TCP_PORT,
                 user=fritzconnection.FRITZ_USERNAME,
                 password=''):
        super(FritzHosts, self).__init__()
        if fc is None:
            fc = fritzconnection.FritzConnection(address, port, user, password)
        self.fc = fc

        self.user = user
        self.password = password

    def action(self, actionname, **kwargs):
        return self.fc.call_action(SERVICE, actionname, **kwargs)

    @property
    def modelname(self):
        return self.fc.modelname

    @property
    def host_numbers(self):
        """
        The number of known hosts.
        """
        result = self.action('GetHostNumberOfEntries')
        return result['NewHostNumberOfEntries']

    def get_generic_host_entry(self, index):
        """
        Returns a dictionary with informations about a device internally
        registered by the position *index*. Index-positions are
        zero-based.
        """
        result = self.action('GetGenericHostEntry', NewIndex=index)
        return result

    def get_specific_host_entry(self, mac_address):
        """
        Returns a dictionary with information about a device addressed
        by the MAC-address.
        """
        result = self.action('GetSpecificHostEntry', NewMACAddress=mac_address)
        return result

    def get_specific_host_entry_by_ip(self, ip_address):
        """
        Returns a dictionary with information about a device addressed
        by the ip-address. Provides additional information about
        connection speed and system-updates for AVM devices.
        """
        result = self.action('X_AVM-DE_GetSpecificHostEntryByIP', NewIPAddress=ip_address)
        return result

    def get_host_status(self, mac_address):
        """
        Provides status information about the device with the given
        `mac_address`. Returns `True` if the device is active or `False`
        otherwise. Returns `None` if the device is not known or the
        `mac_address` is invalid.
        """
        result = self.get_specific_host_entry(mac_address)
        return result['NewActive']

    def get_hosts_info(self):
        """
        Returns a list of dicts with information about the known hosts.
        The dict-keys are: 'ip', 'name', 'mac', 'status'
        """
        result = []
        index = 0
        while index < self.host_numbers:
            host = self.get_generic_host_entry(index)
            result.append({
                'ip': host['NewIPAddress'],
                'name': host['NewHostName'],
                'mac': host['NewMACAddress'],
                'status': host['NewActive'],
                'interface': host['NewInterfaceType']})
            index += 1
        return result

    def get_hosts_info_ext(self):
        result = self.action('X_AVM-DE_GetHostListPath')
        link = result['NewX_AVM-DE_HostListPath']

        url = 'http://%s:%s%s' % (self.fc.address, self.fc.port, link)

        # sending get request and saving the response as response object
        response = requests.get(url=url)

        # extracting data in xml format
        root = ElementTree.fromstring(response.content)

        result = []

        for item in root.findall('Item'):
            # Index
            name = item.findtext('HostName')
            mac = item.findtext('MACAddress')
            ip = item.findtext('IPAddress')
            speed = item.findtext('X_AVM-DE_Speed')
            update_available = item.findtext('X_AVM-DE_UpdateAvailable')
            interface = item.findtext('NewInterfaceType')

            result.append({
                'name': name,
                'interface': interface,
                'mac': mac,
                'ip': ip,
                'speed': speed,
                'update_available': update_available
            })

        return result

    def get_hosts_info_ext2(self):
        """
        Returns a list of dicts with information about the known hosts.
        The dict-keys are: 'ip', 'name', 'mac', 'status', 'speed'
        """
        #fi = fritzconnection.FritzInspection(self.fc.address, self.fc.port, self.fc.user, self.fc.password)
        #fi.view_actionnames(SERVICE)

        """
        result = []
        index = 0
        while index < self.host_numbers:
            host = self.get_generic_host_entry(index)
            host_ext = self.get_specific_host_entry_by_ip(host['NewMACAddress'])
            print("host_ext mac: %s" % host['NewMACAddress'])
            print("host_ext: %s" % host_ext)

            try:
                speed = host_ext['NewX_AVM-DE_Speed']
            except KeyError:
                speed = None

            try:
                update_available = host_ext['NewX_AVM-DE_UpdateAvailable']
            except KeyError:
                update_available = None

            result.append({
                'ip': host['NewIPAddress'],
                'name': host['NewHostName'],
                'mac': host['NewMACAddress'],
                'status': host['NewActive'],
                'interface': host['NewInterfaceType'],
                'speed': speed,
                'update_available': update_available})
            index += 1
        return result
        """
        pass

    def get_mesh_topology(self, raw=False):
        """
        Returns information about the mesh network topology. If `raw` is
        `False` the topology gets returned as a dictionary with a list
        of nodes. If `raw` is `True` the data are returned as text in
        json format. Default is `False`.
        """
        result = self._action('X_AVM-DE_GetMeshListPath')
        path = result['NewX_AVM-DE_MeshListPath']
        url = f'{self.fc.address}:{self.fc.port}{path}'
        with self.fc.session.get(url) as response:
            return response.text if raw else response.json()

    def get_wakeonlan_status(self, mac_address):
        """
        Returns a boolean whether wake on LAN signal gets send to the
        device with the given `mac_address` in case of a remote access.
        """
        info = self._action(
            'X_AVM-DE_GetAutoWakeOnLANByMACAddress', NewMACAddress=mac_address
        )
        return info['NewAutoWOLEnabled']

    def set_wakeonlan_status(self, mac_address, status=False):
        """
        Sets whether a wake on LAN signal should get send send to the
        device with the given `mac_address` in case of a remote access.
        `status` is a boolean, default value is `False`. This method has
        no return value.
        """
        args = {
            'NewMACAddress': mac_address,
            'NewAutoWOLEnabled': status,
        }
        self._action('X_AVM-DE_SetAutoWakeOnLANByMACAddress', arguments=args)

    def set_host_name(self, mac_address, name):
        """
        Sets the hostname of the device with the given `mac_address` to
        the new `name`.
        """
        args = {
            'NewMACAddress': mac_address,
            'NewHostName': name,
        }
        self._action('X_AVM-DE_SetHostNameByMACAddress', arguments=args)

    def run_host_update(self, mac_address):
        """
        Triggers the host with the given `mac_address` to run a system
        update. The method returns immediately, but for the device it
        take some time to do the OS update. All vendor warnings about running a
        system update apply, like not turning power off during a system
        update. So run this command with caution.
        """
        self._action('X_AVM-DE_HostDoUpdate', NewMACAddress=mac_address)

# ---------------------------------------------------------
# terminal-output:
# ---------------------------------------------------------

def _print_header(fh):
    print('\nFritzHosts:')
    print('{:<20}{}'.format('version:', get_version()))
    print('{:<20}{}'.format('model:', fh.modelname))
    print('{:<20}{}'.format('ip:', fh.fc.address))


def print_hosts(fh):
    print('\nList of registered hosts:\n')
    print('{:>3}: {:<15} {:<26} {:<17}   {}\n'.format(
        'n', 'ip', 'name', 'mac', 'status'))
    hosts = fh.get_hosts_info()
    for index, host in enumerate(hosts):
        status = 'active' if host['status'] == '1' else  '-'
        ip = '-' if host['ip'] == None else host['ip']
        mac = '-' if host['mac'] == None else host['mac']
        print('{:>3}: {:<15} {:<26} {:<17}   {}'.format(
            index,
            ip,
            host['name'],
            mac,
            status,
            )
        )
    print('\n')


def _print_detail(fh, detail, quiet):
    mac_address = detail[0].upper()
    info = fh.get_specific_host_entry(mac_address)
    if info:
        if not quiet:
            print('\n{:<23}{}\n'.format('Details for host:', mac_address))
            for key, value in info.items():
                print('{:<23}: {}'.format(key, value))
            print('\n')
        else:
            print(info['NewActive'])
    else:
        print('0')

def _print_nums(fh):
    print('{:<20}{}\n'.format('Number of hosts:', fh.host_numbers))


# ---------------------------------------------------------
# cli-section:
# ---------------------------------------------------------

def _get_cli_arguments():
    parser = argparse.ArgumentParser(description='FritzBox Hosts')
    parser.add_argument('-i', '--ip-address',
                        nargs='?', default=os.getenv('FRITZ_IP_ADDRESS', fritzconnection.FRITZ_IP_ADDRESS),
                        dest='address',
                        help='ip-address of the FritzBox to connect to. '
                             'Default: %s' % fritzconnection.FRITZ_IP_ADDRESS)
    parser.add_argument('--port',
                        nargs='?', default=os.getenv('FRITZ_TCP_PORT', fritzconnection.FRITZ_TCP_PORT),
                        dest='port',
                        help='port of the FritzBox to connect to. '
                             'Default: %s' % fritzconnection.FRITZ_TCP_PORT)
    parser.add_argument('-u', '--username',
                        nargs=1, default=os.getenv('FRITZ_USERNAME', fritzconnection.FRITZ_USERNAME),
                        help='Fritzbox authentication username')
    parser.add_argument('-p', '--password',
                        nargs=1, default=os.getenv('FRITZ_PASSWORD',''),
                        help='Fritzbox authentication password')
    parser.add_argument('-a', '--all',
                        action='store_true',
                        help='Show all hosts '
                             '(default if no other options given)')
    parser.add_argument('-n', '--nums',
                        action='store_true',
                        help='Show number of known hosts')
    parser.add_argument('-d', '--detail',
                        nargs=1, default='',
                        help='Show information about a specific host '
                             '(DETAIL: MAC Address)')
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='Quiet mode '
                             '(just return state as 0|1 for requested mac address)')
    args = parser.parse_args()
    return args


def _print_status(arguments):
    fh = FritzHosts(address=arguments.address,
                    port=arguments.port,
                    user=arguments.username,
                    password=arguments.password)
    if not arguments.quiet:
        _print_header(fh)
    if arguments.detail:
        _print_detail(fh, arguments.detail, arguments.quiet)
    elif arguments.nums:
        _print_nums(fh)
    else:
        print_hosts(fh)

def main():
    _print_status(_get_cli_arguments())

if __name__ == '__main__':
    main()

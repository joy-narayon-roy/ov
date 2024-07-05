import psutil
import platform


def is_connected_to_vpn():
    system = platform.system()

    # Common VPN interface names for Unix-like systems
    vpn_interfaces_unix = ["tun", "tap", "ppp"]
    # Common VPN interface names for Windows
    vpn_interfaces_windows = ["VPN", "Virtual", "ppp"]

    interfaces = psutil.net_if_addrs()

    if system == "Windows":
        # Check network interfaces for common VPN names in Windows
        for interface in interfaces:
            for vpn_interface in vpn_interfaces_windows:
                if vpn_interface.lower() in interface.lower():
                    return True
    else:
        # Check network interfaces for common VPN names in Unix-like systems
        for interface in interfaces:
            for vpn_interface in vpn_interfaces_unix:
                if vpn_interface in interface:
                    return True

    return False

from pywebostv.connection import WebOSClient
from pywebostv.controls import MediaControl
from pathlib import Path
import json
import ipaddress

class LGTVVolumeControl:
    def __init__(self):
        self._CONFIG_PATH = Path(__file__).parent / "config.json"
        self._DATA = {
            "ip": "",
            "client_key": None
        }
        self._is_connected = False
        self._updateConfig()
        self._connectWebOS()

    def _updateConfig(self, ip: str = None, client_key: str = None):
        if self._CONFIG_PATH.exists():
            try:
                config = json.loads(self._CONFIG_PATH.read_text(encoding="utf-8"))
                if "ip" in config and "client_key" in config:
                    self._DATA = config
            except:
                pass
        if ip is not None:
            try:
                _ = ipaddress.IPv4Address(ip)
                self._DATA["ip"] = ip
            except:
                pass
        if client_key is not None:
            self._DATA["client_key"] = client_key
        self._CONFIG_PATH.write_text(json.dumps(self._DATA, indent=2), encoding="utf-8")

    def _connectWebOS(self):
        self._is_connected = False
        try:
            _ = ipaddress.IPv4Address(self._DATA["ip"])
            self._client = WebOSClient(self._DATA["ip"], secure=True)
            self._client.connect()
            store = {"client_key": self._DATA["client_key"]}
            for status in self._client.register(store):
                if status == WebOSClient.PROMPTED:
                    pass
                elif status == WebOSClient.REGISTERED:
                    self._updateConfig(client_key=store["client_key"])
                    self._media = MediaControl(self._client)
                    self._is_connected = True
        except Exception as e:
            pass

    def updateIP(self, ip: str):
        self._updateConfig(ip=ip)
        self._connectWebOS()

    def getIP(self):
        return self._DATA["ip"]

    def getVolumeStats(self) -> dict:
        if self._is_connected:
            data = self._media.get_volume()
            return {
                "volume": data["volume"],
                "muted": data["muted"]
            }
        return {
            "volume": None,
            "muted":None
        }

    def volumeUp(self):
        if self._is_connected:
            self._media.volume_up()

    def volumeDown(self):
        if self._is_connected:
            self._media.volume_down()

    def setVolume(self, n: int):
        if self._is_connected:
            if 0 <= n <= 100:
                self._media.set_volume(n)

    def mute(self, status: bool) -> bool:
        if self._is_connected:
            self._media.mute(status)
            return status
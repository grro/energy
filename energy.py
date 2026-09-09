from provider import Provider
from pv import Pv
from battery import Battery
from heater import Heater



class Energy:

    def __init__(self, provider: Provider, pv: Pv, battery: Battery, heater: Heater):
        self.__is_running = True
        self.__listeners = set()
        self.provider = provider
        self.pv = pv
        self.battery = battery
        self.heater = heater
        self.provider.add_listener(self.__on_update)
        self.pv.add_listener(self.__on_update)
        self.battery.add_listener(self.__on_update)
        self.heater.add_listener(self.__on_update)
        self.__provider_core_power_smoothen_recorder = WattRecorder()

    def add_listener(self, listener):
        self.__listeners.add(listener)

    def __on_update(self):
        self.__provider_core_power_smoothen_recorder.put(self.power_core_consumption)
        [listener() for listener in self.__listeners]

    @property
    def power_core_consumption_5s(self) -> int:
        return self.__provider_core_power_smoothen_recorder.watt_per_hour(second_range=5)

    @property
    def power_core_consumption(self) -> int:
        downstream = self.provider.provider_power_downstream + self.pv.power_downstream + self.battery.power_downstream
        upstream = self.provider.provider_power_upstream + self.battery.power_upstream + self.heater.power
        return downstream - upstream

    @property
    def power_consumption(self) -> int:
        return self.provider.provider_power + self.battery.power_downstream + self.pv.power_downstream

    @property
    def power_consumption_5s(self) -> int:
        return self.provider.provider_power_5s + self.battery.power_downstream_5s + self.pv.power_downstream_5s

    @property
    def power_consumption_15s(self) -> int:
        return self.provider.provider_power_15s + self.battery.power_downstream_15s + self.pv.power_downstream_15s

    @property
    def power_consumption_1m(self) -> int:
        return self.provider.provider_power_1m + self.battery.power_downstream_1m + self.pv.power_downstream_1m

    @property
    def power_consumption_5m(self) -> int:
        return self.provider.provider_power_5m + self.battery.power_downstream_5m + self.pv.power_downstream_5m

    @property
    def power_green_1m(self) -> int:
        return self.pv.power_downstream_1m + self.battery.power_downstream_1m

    @property
    def power_surplus(self) -> int:
        return self.provider.provider_power_upstream + self.battery.power_upstream

    @property
    def power_surplus_5s(self) -> int:
        return self.provider.provider_power_upstream_5s + self.battery.power_upstream_5s

    @property
    def power_surplus_15s(self) -> int:
        return self.provider.provider_power_upstream_15s + self.battery.power_upstream_15s

    @property
    def power_surplus_1m(self) -> int:
        return self.provider.provider_power_upstream_1m + self.battery.power_upstream_1m

    @property
    def power_surplus_5m(self) -> int:
        return self.provider.provider_power_upstream_5m + self.battery.power_upstream_5m

    @property
    def power_surplus_60m(self) -> int:
        return self.provider.provider_power_upstream_60m + self.battery.power_upstream_60m

    def start(self):
        pass

    def stop(self):
        self.__is_running = False



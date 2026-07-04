from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def update_5m(self, candle):
        pass

    @abstractmethod
    def update_1m(self, candle):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def reset_state(self):
        pass

    @abstractmethod
    def get_signals(self):
        pass

    @abstractmethod
    def pop_signal(self):
        pass
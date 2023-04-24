from abc import ABC, abstractmethod

from sklearn.preprocessing import StandardScaler

class MLServer(ABC):
    # PRIVATE

    @abstractmethod
    def _failure_indicator(self, test_data) -> float:
        return 42.0



    # PUBLIC

    @abstractmethod
    def train(self, training_data) -> None:
        self.scaler = StandardScaler().fit(training_data)
        self.training_data = self.scaler.transform(training_data)

    def failure_indicator(self, test_data) -> None:
        test_data = self.scaler.transform(test_data)
        return self._failure_indicator(test_data)
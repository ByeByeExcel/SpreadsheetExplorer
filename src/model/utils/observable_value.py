from typing import Generic, TypeVar, Callable

T = TypeVar("T")


class ObservableValue(Generic[T]):
    def __init__(self, value: T):
        self._value: T = value
        self._observers: list[Callable[[T, T], None]] = []

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: T):
        if new_value != self._value:
            old_value = self._value
            self._value = new_value
            for callback in self._observers:
                callback(new_value, old_value)

    def set_value(self, value: T):
        self.value = value

    def add_observer(self, callback: Callable[[T, T], None]):
        self._observers.append(callback)

    def remove_observer(self, callback: Callable[[T, T], None]):
        self._observers.remove(callback)

    def remove_all_observers(self):
        self._observers.clear()

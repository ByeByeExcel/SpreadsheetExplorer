from model.utils.observable_value import ObservableValue


def test_initial_value():
    ov = ObservableValue(10)
    assert ov.value == 10


def test_set_value_triggers_observer():
    ov = ObservableValue(0)
    calls = []

    def observer(new, old):
        calls.append((new, old))

    ov.add_observer(observer)
    ov.set_value(42)
    ov.set_value(43)

    assert ov.value == 43
    assert calls[0] == (0, 0)
    assert calls[1] == (42, 0)
    assert calls[2] == (43, 42)


def test_no_trigger_on_same_value():
    ov = ObservableValue(5)
    calls = []

    def observer(new, old):
        calls.append((new, old))

    ov.add_observer(observer)
    ov.set_value(5)  # same value

    # Only the initial call when added
    assert calls == [(5, 5)]


def test_remove_observer():
    ov = ObservableValue(1)
    calls = []

    def observer(new, old):
        calls.append((new, old))

    ov.add_observer(observer)
    ov.remove_observer(observer)
    ov.set_value(2)

    assert calls == [(1, 1)]  # only the initial add call, no updates after removal


def test_remove_all_observers():
    ov = ObservableValue(1)
    calls = []

    def observer1(new, old):
        calls.append(('obs1', new, old))

    def observer2(new, old):
        calls.append(('obs2', new, old))

    ov.add_observer(observer1)
    ov.add_observer(observer2)
    ov.remove_all_observers()
    ov.set_value(2)

    assert calls == [('obs1', 1, 1), ('obs2', 1, 1)]  # only initial calls, no updates after clearing

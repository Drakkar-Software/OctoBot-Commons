class Singleton(object):
    """
    From https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    def __cnew__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

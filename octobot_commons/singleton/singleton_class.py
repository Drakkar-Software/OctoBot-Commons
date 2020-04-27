class Singleton:
    """
    From https://stackoverflow.com/questions/51245056/singleton-is-not-working-in-cython
    """

    _instances = {}

    @classmethod
    def instance(cls, *args, **kwargs):
        """
        Create the instance if not already created
        Return the class instance
        :param args: the constructor arguments
        :param kwargs: the constructor optional arguments
        :return: the class only instance
        """
        if cls not in cls._instances:
            cls._instances[cls] = cls(*args, **kwargs)
        return cls._instances[cls]

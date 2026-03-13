class FolderColor:
    color1: tuple[int, int, int]
    is_gradient: bool
    color2: tuple[int, int, int]
    start_gradient: [int, int]
    end_gradient: [int, int]

    def __init__(self, **kwargs):
        """
            :param is_gradient: bool
            :param color1: [int, int, int]

             if is_gradient:
                :param color2: [int, int, int]
                :param start_gradient: [int, int]
                :param end_gradient: [int, int]
        """
        if "is_gradient" in kwargs.keys() or "color2" in kwargs.keys():
            self.is_gradient: bool = True
            self.color2: tuple[int, int, int] = tuple(kwargs["color2"])
            self.start_gradient: [int, int] = kwargs["start_gradient"]
            self.end_gradient: [int, int] = kwargs["end_gradient"]
        else:
            self.is_gradient: bool = False
        self.color1: [int, int, int] = tuple(kwargs["color1"])

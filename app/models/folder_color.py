class FolderColor:
    def __init__(self, **kwargs):
        """
            is_gradient: bool
            color1: [int, int, int]

            if is_gradient:
                color2: [int, int, int]
                start_gradient: [int, int]
                end_gradient: [int, int]
        """
        if "is_gradient" in kwargs.values():
            self.is_gradient: bool = kwargs["is_gradient"]
            self.color2: [int, int, int] = kwargs["color2"]
            self.start_gradient: [int, int] = kwargs["start_gradient"]
            self.end_gradient: [int, int] = kwargs["end_gradient"]
        else:
            self.is_gradient: bool = False
        self.color1: [int, int, int] = kwargs["color1"]

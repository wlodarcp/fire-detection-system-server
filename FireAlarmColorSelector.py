class FireAlarmColorSelector:

    def __init__(self):
        self.color = "background-color:red;"

    def get_color(self):
        if self.color == "background-color:red;":
            self.color = "background-color:orange;"
        elif self.color == "background-color:orange;":
            self.color = "background-color:red;"
        return self.color
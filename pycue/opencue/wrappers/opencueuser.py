from opencue.compiled_proto import opencueUser_pb2
from opencue.cuebot import Cuebot

class OpencueUser(object):
    def __init__(self, opencueuser=None):
        self.data = opencueuser
        self.stub = Cuebot.getStub('opencueUser')

    def name(self):
        return self.data.name

    def admin(self):
        return self.data.admin

    def job_priority(self):
        return self.data.job_priority

    def job_max_cores(self):
        return self.data.job_max_cores

    def show(self):
        return self.data.show

    def show_min_cores(self):
        return self.data.show_min_cores

    def show_max_cores(self):
        return self.data.show_max_cores

    def activate(self):
        return self.data.activate

    def priority_weight(self):
        return self.data.priority_weight

    def error_weight(self):
        return self.data.error_weight

    def submit_time_weight(self):
        return self.data.submit_time_weight

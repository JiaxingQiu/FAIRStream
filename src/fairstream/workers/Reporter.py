from workers.Goblin import Goblin


class Reporter(Goblin):
    def __init__(self, work_dir):
        Goblin.__init__(self, work_dir)

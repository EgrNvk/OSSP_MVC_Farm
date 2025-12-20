class MissionModel:
    def __init__(self):
        self.unlock_all_fields_done = False
        self.unlocked_fields = 0
        self.total_fields = 0

        self.wheat_stock_done = False
        self.wheat_count = 0

        self.save_1000_done = False
        self.money = 0

        self.organic_done = False
        self.organic_plantings = 0

        self.longest_session_done = False
        self.longest_session_time = 0
        self.current_session_time = 0

    def check_all(self):
        if not self.unlock_all_fields_done:
            if self.total_fields > 0 and self.unlocked_fields >= self.total_fields:
                self.unlock_all_fields_done = True

        self.wheat_stock_done = (self.wheat_count >= 10)

        self.save_1000_done = (self.money >= 1000)

        if not self.organic_done:
            if self.organic_plantings >= 10:
                self.organic_done = True

        if self.current_session_time > self.longest_session_time:
            self.longest_session_time = self.current_session_time
            self.longest_session_done = True

    def save_state(self, data: dict) -> None:
        data["missions"] = {
            "unlock_all_fields_done": self.unlock_all_fields_done,
            "unlocked_fields": self.unlocked_fields,
            "total_fields": self.total_fields,

            "wheat_stock_done": self.wheat_stock_done,
            "wheat_count": self.wheat_count,

            "save_1000_done": self.save_1000_done,
            "money": self.money,

            "organic_done": self.organic_done,
            "organic_plantings": self.organic_plantings,

            "longest_session_done": self.longest_session_done,
            "longest_session_time": self.longest_session_time,
            "current_session_time": self.current_session_time,
        }

    def load_state(self, data: dict) -> None:
        missions = data.get("missions")
        if not isinstance(missions, dict):
            return

        self.unlock_all_fields_done = bool(missions.get("unlock_all_fields_done", self.unlock_all_fields_done))
        self.unlocked_fields = int(missions.get("unlocked_fields", self.unlocked_fields))
        self.total_fields = int(missions.get("total_fields", self.total_fields))

        self.wheat_stock_done = bool(missions.get("wheat_stock_done", self.wheat_stock_done))
        self.wheat_count = int(missions.get("wheat_count", self.wheat_count))

        self.save_1000_done = bool(missions.get("save_1000_done", self.save_1000_done))
        self.money = int(missions.get("money", self.money))

        self.organic_done = bool(missions.get("organic_done", self.organic_done))
        self.organic_plantings = int(missions.get("organic_plantings", self.organic_plantings))

        self.longest_session_done = bool(missions.get("longest_session_done", self.longest_session_done))
        self.longest_session_time = int(missions.get("longest_session_time", self.longest_session_time))
        self.current_session_time = int(missions.get("current_session_time", self.current_session_time))

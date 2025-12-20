class MissionController:
    def __init__(self, model):
        self.model = model

    def sync_all(self):
        m=self.model.missions
        m.money=int(self.model.balance)
        m.unlocked_fields=sum(1 for f in self.model.fields if getattr(f, "unlocked", False))
        m.total_fields=len(self.model.fields)
        m.wheat_count=int(self.model.ambar.get("Пшениця", 0))
        if m.current_session_time > m.longest_session_time:
            m.longest_session_time = m.current_session_time
            m.longest_session_done = True
        m.total_harvest = sum(self.model.ambar.values())
        m.check_all()

    def after_field_unlocked(self):
        m = self.model.missions
        m.unlocked_fields = sum(
            1 for f in self.model.fields if getattr(f, "unlocked", False)
        )
        m.check_all()

    def after_plant(self, fertilizer_used: bool):
        if not fertilizer_used:
            m = self.model.missions
            m.organic_plantings += 1
            m.check_all()

    def after_harvest(self):
        m = self.model.missions
        m.wheat_count = int(self.model.ambar.get("Пшениця", 0))
        m.check_all()

    def after_balance_change(self):
        m = self.model.missions
        m.money = int(self.model.balance)
        m.check_all()

    def after_tick(self):
        self.model.missions.current_session_time += 1
        self.sync_all()
class Event:
    
    year: int = 0
    month: int = 0
    day: int = 0
    time_hours: int = 0
    time_minutes: int or str = "00"
    category: str = None
    title: str = None
    #details: str = None
    id: int = None

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def create(kw_dict: dict):
        event = Event()
        for key in kw_dict:
            setattr(event, key, kw_dict[key])
        return event

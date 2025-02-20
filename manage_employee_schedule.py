from typing import List, Dict, Set
from enum import Enum

class Shift(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"

class Day(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class ManageSchedule:
    def __init__(self, schedule):
        self.employeeInfos = {} # Dict[str, Set[tuple]]
        self.employeePerShiftDay = {} # Dict[str, List[List]]
        self.preferences = {} # Dict[str, Set[tuple]]
        self.shifts = Shift()
        self.days = Day()
        
    def getPreference(self, filename: str) -> bool:
        '''
        set a preference of employees' schedule
        return true if successful
        '''
        pass

    def getEmployeeInfos(self, filename: str) -> bool:
        '''
        initialize employeeInfos with names
        return true if successful
        '''
        pass

    def initializeEmployeePerShiftDay(self) -> None:
        '''
        initialize employeePerShiftDay with empty list
        '''
        pass

    def assignShift(self, name: str) -> None:
        '''
        assign shift to employees
        '''
        pass

    def isOneShiftPerDay(self, name: str) -> bool:
        '''
        return true if one shift per day of the employee
        '''
        pass

    def isWorkMaximum(self, name: str) -> bool:
        '''
        return true if the employee works maximum
        '''
        pass

    def employeeNumPerShiftDay(self, day: str) -> tuple:
        '''
        return the number of employees per shift of the day (morning, afternoon, evening)
        '''
        return morning, afternoon, evening
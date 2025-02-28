from typing import List, Dict, Set
from enum import Enum
import logging
import yaml
logging.basicConfig(level=logging.INFO)

class Shift(Enum):
    MORNING = 0
    AFTERNOON = 1
    EVENING = 2

class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

class ManageSchedule:
    def __init__(self, schedule):
        self.employeeSchedule = {} # {name: [(day1,shift1), (day2,shift2), ...]}
        self.employeeNumberPerShiftDay = {} # {day: [[morning,x],[afternoon,y],[evening,z]]}
        self.preferences = {} # {name: [(day1,shift1), (day2,shift2), ...]}
        self.employeeWorkMaxDays = [] # [name1, name2, name3, ...]

        self.initializeEmployeePerShiftDay()
        
    def getPreference(self, filename: str) -> bool:
        '''
        set a preference of employees' schedule
        return true if successful
        '''
        with open(filename, 'r') as file:
            preferences = yaml.safe_load(file)
        logging.debug(f'finish loading preferences: {preferences}')

        for i, employee in enumerate(preferences['employees']):
            slots = []
            for j, slot in enumerate(employee['preferences']):
                day = slot['day']
                shift = slot['time']
                slots.append((day, shift))
            self.preferences[employee['name']] = slots
        #print(self.preferences['Bob'])
        #print(self.preferences['Sarah'])

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
        for day in (Day):
            morning = 0
            afternoon = 0
            evening = 0
            self.employeeNumberPerShiftDay[day.value] = [morning, afternoon, evening]
        logging.info('finish initializing employeeNumberPerShiftDay')
        

    def assignShift(self, name: str, shiftLimit: int = 4, maxWorkDay: int = 5) -> None:
        '''
        assign shift to employees

        This method will assign shift to employees based on their preferences.
        Use this following methods

        manages:
        main loop1: go each employee in preferences (O(n))
            if isOneShiftPerday() is false
                error: employee "name" has more than one shift per day
                break
            if getNumofWorkDay() > maxWorkDay
                error: employee "name" works more than 5 days
                break
            if getNumofWorkDay() == maxWorkDay    
                add in a list of employees who work maximum - employeeWorkMaxDays: [name1, name2, name3, ...]

        if those conditions are met, then assign shift to the employee as follows
        main loop2: go through each employee in preferences (O(n))
            for each day in (day,shift)
                numMorning, numAfternoon, numEvening = employeeNumPerShiftDay(day)
                if shift == 1 (morning)
                    if numMorning < shiftLimit
                        assign shift to the employee
                    else
                        assign shift to the next shift on the same day or next day
                if shift == 2 (afternoon)
                    if numAfternoon < shiftLimit
                        assign shift to the employee
                    else
                        assign shift to the next shift on the same day or next day
                if shift == 3 (evening)
                    if numEvening < shiftLimit
                        assign shift to the employee
                    else
                        assign shift to the next shift on the same day or next day
        
        main loop3: go through each day in employeeNumberPerShiftDay
            numMorning, numAfternoon, numEvening = employeeNumPerShiftDay(day)
            if any of them < 2:
                randomly assign shift to the employee who has not on employeeWorkMaxDays
                
        '''
        pass

    def isOneShiftPerDay(self, name: str) -> bool:
        '''
        return true if one shift per day of the employee

        isOneShiftPerDay: this condition will go through preferences and check if the employee has only one shift per day
        e.g. compare tuple (day1,shift1) and (day2, shift2) if day1 == day2 then isOneShiftPerday is false

        datastructure: preferences
        is used in assignShift method
        '''
        pass

    def getNumofWorkDay(self, name: str) -> int:
        '''
        return the number of days the employee works

        e.g. for employee A, count the number of tuples (day,shift) in preferences.
        
        datastructure: preferences
        is used in assignShift method
        '''
        pass

    def getEmployeeNumPerShiftDay(self, day: str) -> tuple:
        '''
        return the number of employees per shift of the day (morning, afternoon, evening)
        in the following format (shift, number of employees)
        
        e.g. 5, 3, 4 # morning, afternoon, evening

        datastructure: employeeNumberPerShiftDay
        is used in assignShift method

        '''
        match day.upper():
            case 'MON':
                numMorning = self.employeeNumberPerShiftDay[1][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[1][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[1][Shift.EVENING.value]
            case 'TUE':
                numMorning = self.employeeNumberPerShiftDay[2][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[2][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[2][Shift.EVENING.value]
            case 'WED':
                numMorning = self.employeeNumberPerShiftDay[3][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[3][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[3][Shift.EVENING.value]
            case 'THU':
                numMorning = self.employeeNumberPerShiftDay[4][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[4][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[4][Shift.EVENING.value]
            case 'FRI':
                numMorning = self.employeeNumberPerShiftDay[5][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[5][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[5][Shift.EVENING.value]
            case 'SAT':
                numMorning = self.employeeNumberPerShiftDay[6][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[6][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[6][Shift.EVENING.value]
            case 'SUN':
                numMorning = self.employeeNumberPerShiftDay[7][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[7][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[7][Shift.EVENING.value]
            case _:
                numMorning = self.employeeNumberPerShiftDay[Day[day.upper()].value][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[Day[day.upper()].value][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[Day[day.upper()].value][Shift.EVENING.value]
        
        return numMorning, numAfternoon, numEvening
    
    def updateEmployeeNumPerShiftDay(self, day: str, shift: str) -> None:
        '''
        update the number of employees per shift of the day (morning, afternoon, evening)
        '''
        match day.upper():
            case 'MON':
                self.employeeNumberPerShiftDay[1][Shift[shift.upper()].value] += 1
            case 'TUE':
                self.employeeNumberPerShiftDay[2][Shift[shift.upper()].value] += 1
            case 'WED':
                self.employeeNumberPerShiftDay[3][Shift[shift.upper()].value] += 1
            case 'THU':
                self.employeeNumberPerShiftDay[4][Shift[shift.upper()].value] += 1
            case 'FRI':
                self.employeeNumberPerShiftDay[5][Shift[shift.upper()].value] += 1
            case 'SAT':
                self.employeeNumberPerShiftDay[6][Shift[shift.upper()].value] += 1
            case 'SUN':
                self.employeeNumberPerShiftDay[7][Shift[shift.upper()].value] += 1
            case _:
                self.employeeNumberPerShiftDay[Day[day.upper()].value][Shift[shift.upper()].value] += 1
        return None
    

if __name__ == '__main__':
    schedule = ManageSchedule('schedule')

    schedule.getPreference('input/preference_schedule.yaml')
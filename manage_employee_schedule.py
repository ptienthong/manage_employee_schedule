from typing import List, Dict, Set
from enum import Enum
import logging
import yaml
import random
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
    def __init__(self):
        self.employeeSchedule = {} # {name: [(day1,shift1), (day2,shift2), ...]}
        self.employeeNumberPerShiftDay = {} # {day: [[morning,x],[afternoon,y],[evening,z]]}
        self.preferences = {} # {name: [(day1,shift1), (day2,shift2), ...]}

        self.initializeEmployeePerShiftDay()
        
    def getPreference(self, filename: str) -> None:
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
            self.preferences[employee['name'].upper()] = slots

    def writeOutput(self, filename: str) -> None:
        '''
        write the output to the file
        return true if successful
        '''
        with open(filename, 'w') as file:
            yaml.dump(self.employeeSchedule, file)
        logging.debug(f'successfully wrote the schedule to {filename}')
    
    def initializeEmployeePerShiftDay(self) -> None:
        '''
        initialize employeePerShiftDay with empty list
        '''
        for day in (Day):
            self.employeeNumberPerShiftDay[day.name] = [0, 0, 0]
        logging.info('finish initializing employeeNumberPerShiftDay')
        
    def assignShift(self, maxWorkDay: int = 5) -> None:
        '''
        assign shift to employees

        This method will assign shift to employees based on their preferences.
        Use this following methods
        '''
        for name, _ in self.preferences.items():
            if not self.isOneShiftPerDay(name):
                logging.error(f'employee {name} has more than one preference shift per day!')
                break
            if self.getNumofWorkPreference(name) > maxWorkDay:
                logging.error(f'employee {name} has preference work more than 5 days!')
                break

        for name, preference in self.preferences.items():
            for day, shift in preference:
                if shift == 'morning':
                    numMorning, _, _ = self.getEmployeeNumPerShiftDay(day)
                    if self.getNumberofWorkAssigned(name) < maxWorkDay and numMorning < 2:
                        self.updateEmployeeNumPerShiftDay(day, shift)
                        self.setEmployeeSchedule(name, day, shift)
                    else:
                        # assign alternate shift
                        shift = self.findAvailableShiftDay(name, day, maxWorkDay)
                        if shift is not None:
                            self.setEmployeeSchedule(name, day, shift)
                            self.updateEmployeeNumPerShiftDay(day, shift)
                        else:
                            # assign shift to the employee next available day
                            for next_day in self.findNextDays(day):
                                shift = self.findAvailableShiftDay(name, next_day, maxWorkDay)
                                if shift is None:
                                    continue
                                else:    
                                    self.setEmployeeSchedule(name, next_day, shift)
                                    self.updateEmployeeNumPerShiftDay(next_day, shift)
                                    break
                elif shift == 'afternoon':
                    _, numAfternoon, _ = self.getEmployeeNumPerShiftDay(day)
                    if self.getNumberofWorkAssigned(name) < maxWorkDay and numAfternoon < 2:
                        self.updateEmployeeNumPerShiftDay(day, shift)
                        self.setEmployeeSchedule(name, day, shift)
                    else:
                        # assign alternate shift
                        shift = self.findAvailableShiftDay(name, day, maxWorkDay)
                        if shift is not None:
                            self.setEmployeeSchedule(name, day, shift)
                            self.updateEmployeeNumPerShiftDay(day, shift)
                        else:
                            # assign shift to the employee next available day
                            for next_day in self.findNextDays(day):
                                shift = self.findAvailableShiftDay(name, next_day, maxWorkDay)
                                if shift is None:
                                    continue
                                else:    
                                    self.setEmployeeSchedule(name, next_day, shift)
                                    self.updateEmployeeNumPerShiftDay(next_day, shift)
                                    break
                elif shift == 'evening':
                    _, _, numEvening = self.getEmployeeNumPerShiftDay(day)
                    if self.getNumberofWorkAssigned(name) < maxWorkDay and numEvening < 2:
                        self.updateEmployeeNumPerShiftDay(day, shift)
                        self.setEmployeeSchedule(name, day, shift)
                    else:
                        # assign alternate shift
                        shift = self.findAvailableShiftDay(name, day, maxWorkDay)
                        if shift is not None:
                            self.setEmployeeSchedule(name, day, shift)
                            self.updateEmployeeNumPerShiftDay(day, shift)
                        else:
                            # assign shift to the employee next available day
                            for next_day in self.findNextDays(day):
                                shift = self.findAvailableShiftDay(name, next_day, maxWorkDay)
                                if shift is None:
                                    continue
                                else:    
                                    self.setEmployeeSchedule(name, next_day, shift)
                                    self.updateEmployeeNumPerShiftDay(next_day, shift)
                                    break
                else:
                    logging.error(f'invalid shift: {shift}')
                    ValueError(f'invalid shift: {shift}')
                    break

        # fill under staffed shifts
        self.fillUnderStaffedÍhifts()       
                        
    def isOneShiftPerDay(self, name: str) -> bool:
        '''
        return true if one shift per day of the employee

        isOneShiftPerDay: this condition will go through preferences and check if the employee has only one shift per day
        e.g. compare tuple (day1,shift1) and (day2, shift2) if day1 == day2 then isOneShiftPerday is false

        datastructure: preferences
        is used in assignShift method
        '''
        perference_list = self.preferences[name.upper()]
        for i in range(len(perference_list)):
            for j in range(i+1, len(perference_list)):
                if perference_list[i][0].upper() == perference_list[j][0].upper():
                    return False
        return True
    
    def getNumofWorkPreference(self, name: str) -> int:
        '''
        return the number of days the employee works

        e.g. for employee A, count the number of tuples (day,shift) in preferences.
        
        datastructure: preferences
        is used in assignShift method
        '''
        return len(self.preferences[name.upper()])
    
    def getNumberofWorkAssigned(self, name: str) -> int:
        '''
        return the number of days the employee works

        e.g. for employee A, count the number of tuples (day,shift) in employeeSchedule.
        
        datastructure: employeeSchedule
        is used in assignShift method
        '''
        return len(self.employeeSchedule.get(name.upper(), []))

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
                numMorning = self.employeeNumberPerShiftDay[Day.MONDAY.name][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[Day.MONDAY.name][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[Day.MONDAY.name][Shift.EVENING.value]
            case 'TUE':
                numMorning = self.employeeNumberPerShiftDay[Day.TUESDAY.name][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[Day.TUESDAY.name][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[Day.TUESDAY.name][Shift.EVENING.value]
            case 'WED':
                numMorning = self.employeeNumberPerShiftDay[Day.WEDNESDAY.name][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[Day.WEDNESDAY.name][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[Day.WEDNESDAY.name][Shift.EVENING.value]
            case 'THU':
                numMorning = self.employeeNumberPerShiftDay[Day.THURSDAY.name][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[Day.THURSDAY.name][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[Day.THURSDAY.name][Shift.EVENING.value]
            case 'FRI':
                numMorning = self.employeeNumberPerShiftDay[Day.FRIDAY.name][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[Day.FRIDAY.name][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[Day.FRIDAY.name][Shift.EVENING.value]
            case 'SAT':
                numMorning = self.employeeNumberPerShiftDay[Day.SATURDAY.name][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[Day.SATURDAY.name][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[Day.SATURDAY.name][Shift.EVENING.value]
            case 'SUN':
                numMorning = self.employeeNumberPerShiftDay[Day.SUNDAY.name][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[Day.SUNDAY.name][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[Day.SUNDAY.name][Shift.EVENING.value]
            case _:
                numMorning = self.employeeNumberPerShiftDay[Day[day.upper()].name][Shift.MORNING.value]
                numAfternoon = self.employeeNumberPerShiftDay[Day[day.upper()].name][Shift.AFTERNOON.value]
                numEvening = self.employeeNumberPerShiftDay[Day[day.upper()].name][Shift.EVENING.value]
        
        return (numMorning, numAfternoon, numEvening)
    
    def updateEmployeeNumPerShiftDay(self, day: str, shift: str) -> None:
        '''
        update the number of employees per shift of the day (morning, afternoon, evening)
        '''
        match day.upper():
            case 'MON':
                self.employeeNumberPerShiftDay[Day.MONDAY.name][Shift[shift.upper()].value] += 1
            case 'TUE':
                self.employeeNumberPerShiftDay[Day.TUESDAY.name][Shift[shift.upper()].value] += 1
            case 'WED':
                self.employeeNumberPerShiftDay[Day.WEDNESDAY.name][Shift[shift.upper()].value] += 1
            case 'THU':
                self.employeeNumberPerShiftDay[Day.THURSDAY.name][Shift[shift.upper()].value] += 1
            case 'FRI':
                self.employeeNumberPerShiftDay[Day.FRIDAY.name][Shift[shift.upper()].value] += 1
            case 'SAT':
                self.employeeNumberPerShiftDay[Day.SATURDAY.name][Shift[shift.upper()].value] += 1
            case 'SUN':
                self.employeeNumberPerShiftDay[Day.SUNDAY.name][Shift[shift.upper()].value] += 1
            case _:
                self.employeeNumberPerShiftDay[Day[day.upper()].name][Shift[shift.upper()].value] += 1
        return None
    
    def setEmployeeSchedule(self, name: str, day: str, shift: str) -> None:
        '''
        set the employee schedule
        '''
        match day.upper():
                case 'MON':
                    schedule = (Day.MONDAY.name, Shift[shift.upper()].name)
                case 'TUE':
                    schedule = (Day.TUESDAY.name, Shift[shift.upper()].name)
                case 'WED':
                    schedule = (Day.WEDNESDAY.name, Shift[shift.upper()].name)
                case 'THU':
                    schedule = (Day.THURSDAY.name, Shift[shift.upper()].name)
                case 'FRI':
                    schedule = (Day.FRIDAY.name, Shift[shift.upper()].name)
                case 'SAT':
                    schedule = (Day.SATURDAY.name, Shift[shift.upper()].name)
                case 'SUN':
                    schedule = (Day.SUNDAY.name, Shift[shift.upper()].name)
                case _:
                    schedule = (Day[day.upper()].name, Shift[shift.upper()].name)
        
        if name.upper() not in self.employeeSchedule.keys():
            self.employeeSchedule[name.upper()] = []
            self.employeeSchedule[name.upper()].append(schedule)
        else:
            self.employeeSchedule[name.upper()].append(schedule)

        return None
    
    def findAvailableShiftDay(self, name: str, day: str, maxWorkDay: int) -> str:
        '''
        find available shift
        '''
        numMorning, numAfternoon, numEvening = self.getEmployeeNumPerShiftDay(day)
        for shift in ['morning', 'afternoon', 'evening']:
            if shift == 'morning' and numMorning < 2:
                if self.getNumberofWorkAssigned(name) < maxWorkDay:
                    return 'morning'
            elif shift == 'afternoon' and numAfternoon < 2:
                if self.getNumberofWorkAssigned(name) < maxWorkDay:
                    return 'afternoon'
            elif shift == 'evening' and numEvening < 2:
                if self.getNumberofWorkAssigned(name) < maxWorkDay:
                    return 'evening'
            else:
                return None
        
    def findNextDays(self, day: str) -> tuple:
        '''
        return the next days
        '''
        match day.upper():
            case 'MON':
                return ('TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')
            case 'TUE':
                return ('WED', 'THU', 'FRI', 'SAT', 'SUN', 'MON')
            case 'WED':
                return ('THU', 'FRI', 'SAT', 'SUN', 'MON', 'TUE')
            case 'THU':
                return ('FRI', 'SAT', 'SUN', 'MON', 'TUE', 'WED')
            case 'FRI':
                return ('SAT', 'SUN', 'MON', 'TUE', 'WED', 'THU')
            case 'SAT':
                return ('SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI')
            case 'SUN':
                return ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT')
            case _:
                return ()
    
    def fillUnderStaffedÍhifts(self):
        '''
        fill the under staffed shifts
        '''
        availableEmployees = [name for name in self.preferences.keys() if self.getNumberofWorkAssigned(name) < 5]
        for day, shifts in self.employeeNumberPerShiftDay.items():
            morning, afternoon, evening = self.getEmployeeNumPerShiftDay(day)
            while morning < 2 and availableEmployees:
                selectedName = random.choice(availableEmployees)
                self.setEmployeeSchedule(selectedName, day, 'morning')
                self.updateEmployeeNumPerShiftDay(day, 'morning')
                morning, _, _ = self.getEmployeeNumPerShiftDay(day)
                if self.getNumberofWorkAssigned(selectedName) == 5:
                    availableEmployees.remove(selectedName)
            while afternoon < 2 and availableEmployees:
                selectedName = random.choice(availableEmployees)
                self.setEmployeeSchedule(selectedName, day, 'afternoon')
                self.updateEmployeeNumPerShiftDay(day, 'afternoon')
                _, afternoon, _ = self.getEmployeeNumPerShiftDay(day)
                if self.getNumberofWorkAssigned(selectedName) == 5:
                    availableEmployees.remove(selectedName)
            while evening < 2 and availableEmployees:
                selectedName = random.choice(availableEmployees)
                self.setEmployeeSchedule(selectedName, day, 'evening')
                self.updateEmployeeNumPerShiftDay(day, 'evening')
                _, _, evening = self.getEmployeeNumPerShiftDay(day)
                if self.getNumberofWorkAssigned(selectedName) == 5:
                    availableEmployees.remove(selectedName)
    
        
if __name__ == '__main__':
    schedule = ManageSchedule()

    schedule.getPreference('input/preference_schedule.yaml')
    schedule.assignShift(maxWorkDay=5)
    logging.info(f'successfully assigned shift to employees')
    schedule.writeOutput('output/schedule.yaml')
    logging.info(f'successfully wrote the schedule to output/schedule.yaml')
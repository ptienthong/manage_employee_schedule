import pytest
import os
from manage_employee_schedule import ManageSchedule

def test_initializeEmployeePerShiftDay():
    schedule = ManageSchedule('schedule')
    schedule.initializeEmployeePerShiftDay()

    # monday
    assert schedule.employeeNumberPerShiftDay['MONDAY'] == [0, 0, 0]
    # tuesday
    assert schedule.employeeNumberPerShiftDay['TUESDAY'] == [0, 0, 0]
    # wednesday
    assert schedule.employeeNumberPerShiftDay['WEDNESDAY'] == [0, 0, 0]
    # thursday
    assert schedule.employeeNumberPerShiftDay['THURSDAY'] == [0, 0, 0]
    # friday
    assert schedule.employeeNumberPerShiftDay['FRIDAY'] == [0, 0, 0]
    # saturday
    assert schedule.employeeNumberPerShiftDay['SATURDAY'] == [0, 0, 0]
    # sunday
    assert schedule.employeeNumberPerShiftDay['SUNDAY'] == [0, 0, 0]

def test_employee_number_per_day():
    schedule = ManageSchedule('schedule')
    schedule.initializeEmployeePerShiftDay()

    assert schedule.getEmployeeNumPerShiftDay("monday") == (0, 0, 0)
    assert schedule.getEmployeeNumPerShiftDay("Tuesday") == (0, 0, 0)
    assert schedule.getEmployeeNumPerShiftDay("WEDNESDAY") == (0, 0, 0)
    assert schedule.getEmployeeNumPerShiftDay("Thu") == (0, 0, 0)
    assert schedule.getEmployeeNumPerShiftDay("FRI") == (0, 0, 0)
    assert schedule.getEmployeeNumPerShiftDay("sat") == (0, 0, 0)
    assert schedule.getEmployeeNumPerShiftDay("suN") == (0, 0, 0)
    

def test_update_employee_number_per_day():
    schedule = ManageSchedule('schedule')
    schedule.initializeEmployeePerShiftDay()

    schedule.updateEmployeeNumPerShiftDay("monday", "morning")
    assert schedule.getEmployeeNumPerShiftDay("monday") == (1, 0, 0)

    schedule.updateEmployeeNumPerShiftDay("Monday", "afternoon")
    assert schedule.getEmployeeNumPerShiftDay("monday") == (1, 1, 0)

    schedule.updateEmployeeNumPerShiftDay("monday", "Evening")
    assert schedule.getEmployeeNumPerShiftDay("monday") == (1, 1, 1)

    schedule.updateEmployeeNumPerShiftDay("Tue", "evening")
    assert schedule.getEmployeeNumPerShiftDay("TUE") == (0, 0, 1)

    schedule.updateEmployeeNumPerShiftDay("WED", "Morning")
    assert schedule.getEmployeeNumPerShiftDay("wed") == (1, 0, 0)

    schedule.updateEmployeeNumPerShiftDay("wed", "Morning")
    assert schedule.getEmployeeNumPerShiftDay("weD") == (2, 0, 0)

def test_get_numof_workday():
    schedule = ManageSchedule('schedule')
    filepath = os.path.expanduser('~/manage_employee_schedule/input/preference_schedule.yaml')
    schedule.getPreference(filepath)

    assert schedule.getNumofWorkPreference('bob') == 5
    assert schedule.getNumofWorkPreference('sarah') == 5
    assert schedule.getNumofWorkPreference('Alice') == 5

def test_is_one_shift_per_day():
    schedule = ManageSchedule('schedule')
    filepath = os.path.expanduser('~/manage_employee_schedule/input/preference_schedule.yaml')
    schedule.getPreference(filepath)

    assert schedule.isOneShiftPerDay('bob') == True
    assert schedule.isOneShiftPerDay('sarah') == True
    assert schedule.isOneShiftPerDay('Alice') == True


    
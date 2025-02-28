import pytest
from manage_employee_schedule import ManageSchedule

def test_initializeEmployeePerShiftDay():
    schedule = ManageSchedule('schedule')
    schedule.initializeEmployeePerShiftDay()

    # monday
    assert schedule.employeeNumberPerShiftDay[1] == [0, 0, 0]
    # tuesday
    assert schedule.employeeNumberPerShiftDay[2] == [0, 0, 0]
    # wednesday
    assert schedule.employeeNumberPerShiftDay[3] == [0, 0, 0]
    # thursday
    assert schedule.employeeNumberPerShiftDay[4] == [0, 0, 0]
    # friday
    assert schedule.employeeNumberPerShiftDay[5] == [0, 0, 0]
    # saturday
    assert schedule.employeeNumberPerShiftDay[6] == [0, 0, 0]
    # sunday
    assert schedule.employeeNumberPerShiftDay[7] == [0, 0, 0]

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

    
#include <fstream>
#include <iostream>
#include <map>
#include <optional>
#include <random>
#include <set>
#include <string>
#include <vector>
#include <yaml-cpp/yaml.h>


enum class Shift {
    MORNING,
    AFTERNOON,
    EVENING,
    NONE
};

enum class Day {
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY
};

class ManageSchedule {
public:
    ManageSchedule() : debug(true) {
        initializeEmployeePerShiftDay();
    }

    void getPreference(const std::string& filename) {
        YAML::Node preferences = YAML::LoadFile(filename);
        for (const auto& employee : preferences["employees"]) {
            if (debug)
            {
                std::cout << "Employee: " << employee["name"].as<std::string>() << std::endl;
            }
            std::vector<std::pair<Day, Shift>> slots;
            for (const auto& slot : employee["preferences"]) {
                Day day = stringToDay(slot["day"].as<std::string>());
                Shift shift = stringToShift(slot["time"].as<std::string>());
                slots.emplace_back(day, shift);
                // debug print day, shift
                if (debug)
                {
                    // to ensure that stringToDay and stringToShift are working correctly
                    std::cout << "Day: " << static_cast<int>(day) << " Shift: " << static_cast<int>(shift) << std::endl;
                }
                
            }
            preferences_[employee["name"].as<std::string>()] = slots;
        }
    }

    void writeOutput(const std::string& filename) {
        YAML::Emitter out;
        out << YAML::BeginMap;
        for (const auto& [name, schedule] : employeeSchedule_) {
            out << YAML::Key << name << YAML::Value << YAML::BeginSeq;
            for (const auto& [day, shift] : schedule) {
                out << YAML::BeginMap;
                out << YAML::Key << "day" << YAML::Value << dayToString(day);
                out << YAML::Key << "shift" << YAML::Value << shiftToString(shift);
                out << YAML::EndMap;
            }
            out << YAML::EndSeq;
        }
        out << YAML::EndMap;

        std::ofstream fout(filename);
        fout << out.c_str();
    }

    void assignShift(int maxWorkDay = 5) {
        for (const auto& [name, _] : preferences_) {
            if (!isOneShiftPerDay(name)) {
                std::cerr << "Employee " << name << " has more than one preference shift per day!" << std::endl;
                break;
            }
            if (getNumofWorkPreference(name) > maxWorkDay) {
                std::cerr << "Employee " << name << " has preference work more than 5 days!" << std::endl;
                break;
            }
        }

        for (const auto& [name, preference] : preferences_) {
            for (const auto& [day, shift] : preference) {
                if (shift == Shift::MORNING) {
                    auto [numMorning, unused1, unused2] = getEmployeeNumPerShiftDay(day);
                    if (getNumberofWorkAssigned(name) < maxWorkDay && numMorning < 2) {
                        updateEmployeeNumPerShiftDay(day, shift);
                        setEmployeeSchedule(name, day, shift);
                    } else {
                        auto alternateShift = findAvailableShiftDay(name, day, maxWorkDay);
                        if (alternateShift != Shift::NONE) {
                            setEmployeeSchedule(name, day, alternateShift);
                            updateEmployeeNumPerShiftDay(day, alternateShift);
                        } else {
                            auto next_days = findNextDays(day);
                            for (const auto& next_day : next_days) {
                                auto nextShift = findAvailableShiftDay(name, next_day, maxWorkDay);
                                if (nextShift == Shift::NONE) {
                                    continue;
                                } else {
                                    setEmployeeSchedule(name, next_day, nextShift);
                                    updateEmployeeNumPerShiftDay(next_day, nextShift);
                                    break;
                                }
                            }
                        }
                    }
                } else if (shift == Shift::AFTERNOON) {
                    auto [unused1, numAfternoon, unused2] = getEmployeeNumPerShiftDay(day);
                    if (getNumberofWorkAssigned(name) < maxWorkDay && numAfternoon < 2) {
                        updateEmployeeNumPerShiftDay(day, shift);
                        setEmployeeSchedule(name, day, shift);
                    } else {
                        auto alternateShift = findAvailableShiftDay(name, day, maxWorkDay);
                        if (alternateShift != Shift::NONE) {
                            setEmployeeSchedule(name, day, alternateShift);
                            updateEmployeeNumPerShiftDay(day, alternateShift);
                        } else {
                            auto next_days = findNextDays(day);
                            for (const auto& next_day : next_days) {
                                auto nextShift = findAvailableShiftDay(name, next_day, maxWorkDay);
                                if (nextShift == Shift::NONE) {
                                    continue;
                                } else {
                                    setEmployeeSchedule(name, next_day, nextShift);
                                    updateEmployeeNumPerShiftDay(next_day, nextShift);
                                    break;
                                }
                            }
                        }
                    }
                } else if (shift == Shift::EVENING) {
                    auto [unused1, unused2, numEvening] = getEmployeeNumPerShiftDay(day);
                    if (getNumberofWorkAssigned(name) < maxWorkDay && numEvening < 2) {
                        updateEmployeeNumPerShiftDay(day, shift);
                        setEmployeeSchedule(name, day, shift);
                    } else {
                        auto alternateShift = findAvailableShiftDay(name, day, maxWorkDay);
                        if (alternateShift != Shift::NONE) {
                            setEmployeeSchedule(name, day, alternateShift);
                            updateEmployeeNumPerShiftDay(day, alternateShift);
                        } else {
                            auto next_days = findNextDays(day);
                            for (const auto& next_day : next_days) {
                                auto nextShift = findAvailableShiftDay(name, next_day, maxWorkDay);
                                if (nextShift == Shift::NONE) {
                                    continue;
                                } else {
                                    setEmployeeSchedule(name, next_day, nextShift);
                                    updateEmployeeNumPerShiftDay(next_day, nextShift);
                                    break;
                                }
                            }
                        }
                    }
                } else {
                    std::cerr << "Invalid shift: " << static_cast<int>(shift) << std::endl;
                    throw std::invalid_argument("Invalid shift");
                }
            }
        }

        fillUnderStaffedShifts();
        printEmployeeSchedule();
    }

private:
    bool debug;
    std::map<std::string, std::vector<std::pair<Day, Shift>>> employeeSchedule_;
    std::map<std::string, std::vector<std::pair<Day, Shift>>> preferences_;
    std::map<Day, std::array<int, 3>> employeeNumberPerShiftDay_;

    void printEmployeeSchedule() {
        for (const auto& [name, schedule] : employeeSchedule_) {
            std::cout << name << ": ";
            for (const auto& [day, shift] : schedule) {
                std::cout << dayToString(day) << " " << shiftToString(shift) << ", ";
            }
            std::cout << std::endl;
        }
    }

    void initializeEmployeePerShiftDay() {
        for (int i = static_cast<int>(Day::MONDAY); i <= static_cast<int>(Day::SUNDAY); ++i) {
            employeeNumberPerShiftDay_[static_cast<Day>(i)] = {0, 0, 0};
        }
    }

    bool isOneShiftPerDay(const std::string& name) {
        const auto& preference_list = preferences_[name];
        for (size_t i = 0; i < preference_list.size(); ++i) {
            for (size_t j = i + 1; j < preference_list.size(); ++j) {
                if (preference_list[i].first == preference_list[j].first) {
                    return false;
                }
            }
        }
        return true;
    }

    int getNumofWorkPreference(const std::string& name) {
        return preferences_[name].size();
    }

    int getNumberofWorkAssigned(const std::string& name) {
        if (employeeSchedule_.find(name) != employeeSchedule_.end()) {
            return employeeSchedule_[name].size();
        }
        return 0;
    }

    std::tuple<int, int, int> getEmployeeNumPerShiftDay(Day day) {
        const auto& shifts = employeeNumberPerShiftDay_[day];
        return std::make_tuple(shifts[0], shifts[1], shifts[2]);
    }

    void updateEmployeeNumPerShiftDay(Day day, Shift shift) {
        if (shift == Shift::MORNING || shift == Shift::AFTERNOON || shift == Shift::EVENING) {
            employeeNumberPerShiftDay_[day][static_cast<int>(shift)]++;
        } else {
            throw std::invalid_argument("Invalid shift");
        }
    }

    void setEmployeeSchedule(const std::string& name, Day day, Shift shift) {
        employeeSchedule_[name].emplace_back(day, shift);
    }

    Shift findAvailableShiftDay(const std::string& name, Day day, int maxWorkDay) {
        if (getNumberofWorkAssigned(name) == maxWorkDay) {
            return Shift::NONE; // No available shift
        }
        auto [numMorning, numAfternoon, numEvening] = getEmployeeNumPerShiftDay(day);
        if (numMorning < 2) {
            return Shift::MORNING;
        } 
        else if (numAfternoon < 2) {
            return Shift::AFTERNOON;
        }
        else if (numEvening < 2) {
            return Shift::EVENING;
        } else {
            return Shift::NONE; // No available shift
        }
        
    }

    std::vector<Day> findNextDays(Day day) {
        switch (day) {
            case Day::MONDAY: return {Day::TUESDAY, Day::WEDNESDAY, Day::THURSDAY, Day::FRIDAY, Day::SATURDAY, Day::SUNDAY};
            case Day::TUESDAY: return {Day::WEDNESDAY, Day::THURSDAY, Day::FRIDAY, Day::SATURDAY, Day::SUNDAY, Day::MONDAY};
            case Day::WEDNESDAY: return {Day::THURSDAY, Day::FRIDAY, Day::SATURDAY, Day::SUNDAY, Day::MONDAY, Day::TUESDAY};
            case Day::THURSDAY: return {Day::FRIDAY, Day::SATURDAY, Day::SUNDAY, Day::MONDAY, Day::TUESDAY, Day::WEDNESDAY};
            case Day::FRIDAY: return {Day::SATURDAY, Day::SUNDAY, Day::MONDAY, Day::TUESDAY, Day::WEDNESDAY, Day::THURSDAY};
            case Day::SATURDAY: return {Day::SUNDAY, Day::MONDAY, Day::TUESDAY, Day::WEDNESDAY, Day::THURSDAY, Day::FRIDAY};
            case Day::SUNDAY: return {Day::MONDAY, Day::TUESDAY, Day::WEDNESDAY, Day::THURSDAY, Day::FRIDAY, Day::SATURDAY};
            default: return {};
        }
    }

    void fillUnderStaffedShifts() {
        std::vector<std::string> availableEmployees;
        for (const auto& [name, _] : preferences_) {
            if (getNumberofWorkAssigned(name) < 5) {
                availableEmployees.push_back(name);
            }
        }

        for (const auto& [day, shifts] : employeeNumberPerShiftDay_) {
            auto [morning, afternoon, evening] = getEmployeeNumPerShiftDay(day);
            while (morning < 2 && !availableEmployees.empty()) {
                std::string selectedName = availableEmployees[rand() % availableEmployees.size()];
                setEmployeeSchedule(selectedName, day, Shift::MORNING);
                updateEmployeeNumPerShiftDay(day, Shift::MORNING);
                morning = std::get<0>(getEmployeeNumPerShiftDay(day));
                if (getNumberofWorkAssigned(selectedName) == 5) {
                    availableEmployees.erase(std::remove(availableEmployees.begin(), availableEmployees.end(), selectedName), availableEmployees.end());
                }
            }
            while (afternoon < 2 && !availableEmployees.empty()) {
                std::string selectedName = availableEmployees[rand() % availableEmployees.size()];
                setEmployeeSchedule(selectedName, day, Shift::AFTERNOON);
                updateEmployeeNumPerShiftDay(day, Shift::AFTERNOON);
                afternoon = std::get<1>(getEmployeeNumPerShiftDay(day));
                if (getNumberofWorkAssigned(selectedName) == 5) {
                    availableEmployees.erase(std::remove(availableEmployees.begin(), availableEmployees.end(), selectedName), availableEmployees.end());
                }
            }
            while (evening < 2 && !availableEmployees.empty()) {
                std::string selectedName = availableEmployees[rand() % availableEmployees.size()];
                setEmployeeSchedule(selectedName, day, Shift::EVENING);
                updateEmployeeNumPerShiftDay(day, Shift::EVENING);
                evening = std::get<2>(getEmployeeNumPerShiftDay(day));
                if (getNumberofWorkAssigned(selectedName) == 5) {
                    availableEmployees.erase(std::remove(availableEmployees.begin(), availableEmployees.end(), selectedName), availableEmployees.end());
                }
            }
        }
    }

    Day stringToDay(const std::string& day) {
        if (day == "Mon") return Day::MONDAY;
        if (day == "Tue") return Day::TUESDAY;
        if (day == "Wed") return Day::WEDNESDAY;
        if (day == "Thu") return Day::THURSDAY;
        if (day == "Fri") return Day::FRIDAY;
        if (day == "Sat") return Day::SATURDAY;
        if (day == "Sun") return Day::SUNDAY;

        if (day == "Monday") return Day::MONDAY;
        if (day == "Tuesday") return Day::TUESDAY;
        if (day == "Wednesday") return Day::WEDNESDAY;
        if (day == "Thursday") return Day::THURSDAY;
        if (day == "Friday") return Day::FRIDAY;
        if (day == "Saturday") return Day::SATURDAY;
        if (day == "Sunday") return Day::SUNDAY;
        
        throw std::invalid_argument("Invalid day");
    }

    std::string dayToString(Day day) {
        switch (day) {
            case Day::MONDAY: return "MON";
            case Day::TUESDAY: return "TUE";
            case Day::WEDNESDAY: return "WED";
            case Day::THURSDAY: return "THU";
            case Day::FRIDAY: return "FRI";
            case Day::SATURDAY: return "SAT";
            case Day::SUNDAY: return "SUN";
            default: throw std::invalid_argument("Invalid day");
        }
    }

    Shift stringToShift(const std::string& shift) {
        if (shift == "morning") return Shift::MORNING;
        if (shift == "afternoon") return Shift::AFTERNOON;
        if (shift == "evening") return Shift::EVENING;
        throw std::invalid_argument("Invalid shift");
    }

    std::string shiftToString(Shift shift) {
        switch (shift) {
            case Shift::MORNING: return "morning";
            case Shift::AFTERNOON: return "afternoon";
            case Shift::EVENING: return "evening";
            default: throw std::invalid_argument("Invalid shift");
        }
    }
};

int main() {
    try {
        ManageSchedule schedule;

        schedule.getPreference("/Users/peeratienthong/manage_employee_schedule/input/preference_schedule.yaml");
        schedule.assignShift(5);
        std::cout << "Successfully assigned shift to employees" << std::endl;
        schedule.writeOutput("/Users/peeratienthong/manage_employee_schedule/output/schedule_cpp.yaml");
        std::cout << "Successfully wrote the schedule to output/schedule.yaml" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return 1;
    }
    return 0;
}

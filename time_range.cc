#include<vector>
#include<utility>
#include<iostream>
#include<string>



using namespace std;

class DayScheduler {
    int duration_task = 90;
    int duration_break = 20;
    const int task_cnt = 9;
    vector<vector<pair<int, int> > > day_schedule = vector<vector<pair<int, int> > >(task_cnt, vector<pair<int, int> >(2, make_pair(05, 30)));
public:
    DayScheduler(const pair<int, int>& start) {
        for (int i = 0; i < task_cnt; i++) {
            calculateTaskTimeRange(start, i);
        }
        rescheduleByMealBreak(0);
    }
    void printSchedule() {
        for (int i = 0; i < task_cnt; i++) {
            if  (firstTaskAfterMeal(i)) cout << "=== Meal Break === " << endl;
            cout << i << ". "
                 << beautifyHourMinute(day_schedule[i][0].first) << ":" << beautifyHourMinute(day_schedule[i][0].second) << " - "
                 << beautifyHourMinute(day_schedule[i][1].first) << ":" << beautifyHourMinute(day_schedule[i][1].second) << endl;
        }
        string time_block = "{";
        for (int i = 0; i < task_cnt; i++) {
            time_block +=  ("\"" + beautifyHourMinute(day_schedule[i][0].first) + ":" + beautifyHourMinute(day_schedule[i][0].second) + "\","
                 + "\"" + beautifyHourMinute(day_schedule[i][1].first) + ":" + beautifyHourMinute(day_schedule[i][1].second) + "\",");
        }
        time_block.pop_back();
        cout << time_block + "}" << endl;
    }
    void changeTargetTaskTimeRange(int task_idx, const pair<int, int>& start, int duration = 90) {
        day_schedule[task_idx][0] = timeAfterInterval(start, 0);
        day_schedule[task_idx][1] = timeAfterInterval(start, duration);
        changeTasksRangeAfterFixedTask(task_idx, start, duration);
    }
private:
    pair<int, int> timeAfterInterval(const pair<int, int>& start, int interval) {
        int interval_minute = start.second + interval;
        return make_pair(start.first + interval_minute / 60, interval_minute % 60); 
    }

    void calculateTaskTimeRange(const pair<int, int>& start, int i) {
        int duration = duration_task + duration_break;
        day_schedule[i][0] = timeAfterInterval(start, i *  duration);
        day_schedule[i][1] = timeAfterInterval(start, i *  duration + duration_task);
    }

    void changeTasksRangeAfterFixedTask(int task_idx, const pair<int, int>& start, int duration) {
        int delta = duration - duration_task, origin_interval = duration_task + duration_break;
        for (int i = task_idx + 1; i < task_cnt; i++) {
            day_schedule[i][0] = timeAfterInterval(start, (i - task_idx) * origin_interval + delta);
            day_schedule[i][1] = timeAfterInterval(start, (i - task_idx) * origin_interval + delta + duration_task);
        }
        rescheduleByMealBreak(task_idx + 1);
    }
    
    string beautifyHourMinute(int clock) {
        return clock < 10 ? "0" + to_string(clock) : to_string(clock);
    }
    void rescheduleByMealBreak(int begin_idx) {
        for (int i = begin_idx; i < task_cnt; i++) {
            if (firstTaskAfterMeal(i)) changeTargetTaskTimeRange(i, timeAfterInterval(day_schedule[i][0], 10));
        }
    }
    bool firstTaskAfterMeal(int i) {
        return i == 1 || i == 4 || i == 7;
    }
};

int main() {
	DayScheduler d(make_pair(5, 30));
    d.changeTargetTaskTimeRange(4, make_pair(13,00));
    d.printSchedule();
    return 0;
}


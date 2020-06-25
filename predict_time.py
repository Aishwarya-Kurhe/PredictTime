import pandas as pd
import random
import numpy as np
import time

#Function which will be used to create the scenario
def create_scenario(type):
    issue_id = random.randint(1000, 2000)
    f = open("agent_data.csv", "a")
    #When the agent is busy with other issue then the previous issue is not abandoned and resolved
    #So we need to make entry in agent_data.csv file where abandoned/resolved field is empty
    if type == "busy":
        f.write(str(issue_id) + ", " + "7:02" + ", " + "" + ", " + "7:02" + ", " + "" + ", " + "" + "\n")

    #When agent is free to solve new issue then the previous issue should be resolved or abandoned
    #So we need to make entry in agent_data.csv with abandoned/resolved and with respect to their time
    elif type == "free":
        status = random.choice(["abandoned", "resolved"])
        if status == "abandoned":
            f.write(str(issue_id) + ", " + "7:02" + ", " + status + ", " + "7:02" + ", " + "7:39" + ", " + "" + "\n")
        elif status == "resolved":
            f.write(str(issue_id) + ", " + "7:02" + ", " + status + ", " + "7:02" + ", " + "" + ", " + "7:39" + "\n")
    f.close()

def predict_time():
    #time_difference is used to collect the time (minutes) required to solve the issue with respect to issue_id
    time_difference = []

    #Using pandas library we will fetch the last row of agent_data.csv file and check whether the issue is remain to solve or abandoned/resolved
    df = pd.read_csv("agent_data.csv")
    last_row = df.tail(1).to_numpy().tolist()[0]
    status = last_row[2]

    #If the issue status is abandoned or resolved that means the agent is free to solve new issue the predicted time will be current system time
    if "abandoned" in status or "resolved" in status:
        predicted_time = time.asctime( time.localtime(time.time()))[11:16]
        return predicted_time

    #If the issue status is not abandoned or resolved that means the agent is busy in solving the previous issue
    #So wee need to get the previous issue id and find all the data related to that issue
    else:
        issue_id = int(last_row[0])
        data_with_issue_id = df.loc[df["issue_id"]==issue_id].to_numpy().tolist()

        #After getting the issue data we need to find the time (minutes) required to solve the issue
        for ind in range(len(data_with_issue_id)):
            if ind == (len(data_with_issue_id) - 1):
                break
            if "abandoned" in data_with_issue_id[ind][2]:
                end_time = data_with_issue_id[ind][4]
            elif "resolved" in data_with_issue_id[ind][2]:
                end_time = data_with_issue_id[ind][5]
            answer_time = data_with_issue_id[ind][3]
            end_time = end_time.split(":")
            end_hr = int(end_time[0])
            end_min = int(end_time[1])
            answer_time = answer_time.split(":")
            answer_hr = int(answer_time[0])
            answer_min = int(answer_time[1])
            if end_hr > (answer_hr + 1):
                hrs = end_hr - answer_hr + 1
            else:
                hrs = 0
            mins = (60 - answer_min) + hrs * 60 + end_min
            time_difference.append(mins)

        #After getting the time required to solve the issue, we will find the average of that time (minutes)
        time_difference = np.average(np.asarray(time_difference))

        #Then the average time is added into the current system time and then it will return the predicted time
        current_time = time.asctime( time.localtime(time.time()))[11:16]
        current_time = str(current_time).split(":")
        current_hr = int(current_time[0])
        current_min = int(current_time[1]) + int(time_difference)
        if current_min > 60:
            current_hr += int(current_min/60)
            current_min = current_min % 60
        if current_hr > 23:
            current_hr = current_hr - 24
            if len(current_min) == 1:
                current_min = "0" + str(current_min)
        predicted_time = str(current_hr) + ":" + str(current_min)
        return predicted_time

def main():
    #Get the issue from user
    issue = input("Enter your issue: ")

    #The agent_data.csv file contains about 3000 data logs
    #There will be two scenario from which we can predict time i.e.
    # 1. When the agent is busy in solving other issue
    # 2. When agent is free to solve the issue

    #First we will predict the time when agent is busy in solving other issue
    #To get that we need to create the scenario
    create_scenario("busy")
    #Now predict the time while agent is busy
    time_when_agent_is_busy = predict_time()
    print("\nTest Case 1: When the agent is not available")
    print("Agent will be available till: ", time_when_agent_is_busy)

    #Second we will predict the time when agent is free to solve issue
    #TO get that we will create the scenario
    create_scenario("free")
    #Now predict the time while agent is free
    time_when_agent_is_free = predict_time()
    print("\nTest Case 2: When the agent is available")
    print("Agent will be available till: ", time_when_agent_is_free)


if __name__ == '__main__':
    main()

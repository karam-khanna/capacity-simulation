import os

import pandas as pd
from matplotlib import pyplot as plt

def update_master_csv():
    # create master pandas
    master_csv = pd.DataFrame()


    # loop through files in raw_csvs
    for file in os.listdir("assets/raw_csvs"):
        # skip non-csv files
        if not file.endswith(".csv"):
            continue



        # load data from csv
        data = pd.read_csv(f"assets/raw_csvs/{file}")

        # append data to master csv via concat
        master_csv = pd.concat([master_csv, data], ignore_index=True)

        # sort by room then n
        master_csv = master_csv.sort_values(["room", "n"])




    # write master csv to file overwriting old file
    master_csv.to_csv("assets/master_csv/master.csv", index=False)







def built_n_time_linechart():

    update_master_csv()


    # load data from master csv
    data1 = pd.read_csv("assets/master_csv/master.csv")

    # create plot
    fig, ax = plt.subplots()

    # get list of rooms
    rooms = data1["room"].unique()

    # plot each room
    for room in rooms:
        # filter data
        data = data1[data1["room"] == room]

        # get averages for each n
        data = data.groupby("n").mean().reset_index()

        # sort data
        data = data.sort_values("n")

        # plot data with color
        ax.plot(data["n"], data["time"], label=room)

        # calculate standard deviation
        data["std"] = data1[data1["room"] == room].groupby("n").std().reset_index()["time"]

        # show mean standard deviation as text box
        ax.text(data["n"].iloc[-1], data["time"].iloc[-1], f"std: {data['std'].iloc[-1]:.2f}", bbox=dict(facecolor='white', alpha=0.5))

        # show on average how many data points per n
        # ax.text(data["n"].iloc[-1], data["time"].iloc[-1] - 6, f"n: {data1[data1['room'] == room]['n'].value_counts().mean():.2f}", bbox=dict(facecolor='white', alpha=0.5))






        # # show standard deviation bars every 20th point
        # ax.errorbar(data["n"], data["time"], yerr=data["std"], fmt="none", ecolor="black", elinewidth=1, capsize=2, capthick=1, alpha=0.5)



    # set legend
    ax.legend()


    # set title
    ax.set_title("n vs time")

    # label axes
    ax.set_xlabel("n")
    ax.set_ylabel("time")



    # show plot
    plt.show()

    # write plot to file
    fig.savefig("assets/visuals/n_vs_time.png")

def build_table_for_each_room():

    update_master_csv()


    data = pd.read_csv("assets/master_csv/master.csv")

    # select data where room = jones
    jones = data[data["room"] == "jonesRoom"]

    # get averages for each n
    jonesMeans = jones.groupby("n").mean().reset_index()

    # select data where room = jones
    basic = data[data["room"] == "basic"]

    # get averages for each n
    basicMeans = jones.groupby("n").mean().reset_index()

    # select data where room = jones
    classroom = data[data["room"] == "classroom"]

    # get averages for each n
    classroomMeans = classroom.groupby("n").mean().reset_index()
    #
    # print("jones")
    # print(jonesMeans)
    #
    # print("basic")
    # print(basicMeans)
    #
    # print("classroom")
    # print(classroomMeans)

    # create table



if __name__ == '__main__':
    built_n_time_linechart()


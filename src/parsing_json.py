import json
from re import search
import matplotlib.pyplot as plt

def parsing():
    parsed_string = json.load(open('export.json', 'r'))
    first = list(parsed_string["buckets"])
    substring = "aw-watcher-window"

    for j in first:
        if search(substring, j):
            index = first.index(j)

    system_name = (list(parsed_string["buckets"])[index])

    unique_app = {}

    for i in range(len(parsed_string["buckets"][system_name]["events"])):

        app = (parsed_string["buckets"][system_name]["events"][i]["data"]["app"])
        duration = (parsed_string["buckets"][system_name]["events"][i]["duration"]/60)

        if (app not in unique_app.keys()):
            unique_app[app] = duration
        else:
            old_value = unique_app[app]
            new_value = old_value + duration
            unique_app[app] = new_value


    return unique_app


def plotting(dictionary):
    # Pie Chart
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.pie([float(dictionary[v]) for v in dictionary], labels=[str(k) for k in dictionary], autopct='%1.1f%%', normalize=True)

    # Bar Graph
    names = list(dictionary.keys())
    values = list(dictionary.values())

    ax2.barh(range(len(dictionary)), values, tick_label=names)
    plt.savefig('plot.png')

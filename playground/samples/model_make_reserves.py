import json

reservelist = []

path_ = {
    "table_path": f"",
    "checklist_path": f""
}

def make_reserves():
    gettable()
    ftt = json.load(open(path_["table_path"], "r"))
    f = json.load(open(path_["checklist_path"], "r"))
    cl = f["programs"]

    print(cl)

    for i in range(len(cl)):
        day = int(cl[i]["day"])
        for j in range(len(ftt[day])):
            if cl[i]['title'] in ftt[day][j]['title']:
                appends = ftt[day][j]
                appends['flag'] = False
                reservelist.append(appends)
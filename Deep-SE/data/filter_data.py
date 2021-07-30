import sys
import csv
import re

repo = sys.argv[1]
data = []

with open(repo + '_origin.csv', 'r', encoding="utf-8") as f:
    csv_reader = csv.reader(f, delimiter=',')
    indexes = [0, 0, 0, 0]

    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            for i, col in enumerate(row):
                if col == "Summary":
                    indexes[1] = i
                elif col == "Issue key":
                    indexes[0] = i
                elif col == "Description":
                    indexes[2] = i
                elif col == "Custom field (Story Points)":
                    indexes[3] = i

            line_count += 1
        else:
            record = []
            is_valid = True
            for i, idx in enumerate(indexes):
                if row[idx] == "":
                    is_valid = False
                    break
                if i == 3:
                    if re.match("[^0-9]*[0-9.]+[^0-9]*", row[idx]):
                        sp = re.match("[0-9]+[.]", row[idx])
                        record.append(row[idx][sp.start():sp.end()-1])
                    else:
                        is_valid = False
                    continue

                record.append(row[idx].replace('\n', ''))

            if is_valid:
                data.append(record)

# print(data)

with open(repo + '.csv', 'w', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['issuekey', 'title', 'description', 'storypoint'], delimiter=',')
    writer.writeheader()
f.close()

with open(repo + '.csv', 'a', encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(data)
f.close()

for i in range(len(data)):
    data[i][3] = "NULL"

with open('tpssoft_pretrain.csv', 'w', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['issuekey', 'title', 'description', 'storypoint'], delimiter=',')
    writer.writeheader()
f.close()

with open('tpssoft_pretrain.csv', 'a', encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(data)
f.close()

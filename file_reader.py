import csv


def csv_read(filename, max_line=None):
    with open(filename, mode='r') as f:
        csv_reader, content, counter = csv.reader(f), [], 0
        for line in csv_reader:
            content.append(line)
            counter += 1
            if max_line is not None and counter == max_line:
                break

        return content[1:]

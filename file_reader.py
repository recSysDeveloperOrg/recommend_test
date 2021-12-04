import csv


def csv_read(filename, max_line=None, encoding='utf8'):
    with open(filename, mode='r', encoding=encoding) as f:
        csv_reader, content, counter = csv.reader(f), [], 0
        for line in csv_reader:
            content.append(line)
            counter += 1
            if max_line is not None and counter == max_line:
                break

        return content[1:]

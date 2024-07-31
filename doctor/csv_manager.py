import csv


rows = [['Nikhil', 'COE', '2', '9.0'],
        ['Sanchit', 'COE', '2', '9.1'],
        ['Aditya', 'IT', '2', '9.3'],
        ['Sagar', 'SE', '1', '9.5'],
        ['Prateek', 'MCE', '3', '7.8'],
        ['Sahil', 'EP', '2', '9.1']]


mydict = [{'branch': 'COE', 'cgpa': '9.0',
           'name': 'Nikhil', 'year': '2'},
          {'branch': 'COE', 'cgpa': '9.1',
           'name': 'Sanchit', 'year': '2'},
          {'branch': 'IT', 'cgpa': '9.3',
           'name': 'Aditya', 'year': '2'},
          {'branch': 'SE', 'cgpa': '9.5',
           'name': 'Sagar', 'year': '1'},
          {'branch': 'MCE', 'cgpa': '7.8',
           'name': 'Prateek', 'year': '3'},
          {'branch': 'EP', 'cgpa': '9.1',
           'name': 'Sahil', 'year': '2'}]


fields = ['name', 'branch', 'year', 'cgpa']


def csv_append(file_name, fields, rows):
    with open(file_name, '+a', encoding='utf-8') as csv_app:
        csv_file = csv.writer(csv_app)
        csv_file.writerow(fields)
        csv_file.writerows(rows)


def csv_single_append(file_name, list_item):
    with open(file_name, '+a', encoding='utf-8') as csv_app:
        csv_file = csv.writer(csv_app)
        csv_file.writerow(list_item)


def csv_dict_append(file_name, fields, _dict):
    with open(file_name, '+a', encoding='utf-8') as csv_app:
        writer = csv.DictWriter(csv_app, fieldnames=fields)
        writer.writeheader()
        writer.writerows(_dict)


def csv_get_all_rows(file_name):
    rows = list()
    with open(file_name, 'r', encoding='utf-8') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
    
        # extracting field names through first row
        fields = next(csvreader)
    
        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
    return rows


def main():
    # csv_append('test.csv')
    csv_dict_append('test.csv',fields,mydict)


if __name__ == "__main__":
    main()

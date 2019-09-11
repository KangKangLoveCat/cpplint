# -*- coding: utf-8 -*-
import sys
import xlwt

class Issue:

    def __init__(self, issuename, lineno):
        self.issue_name = issuename
        self.line_no = str(lineno)
        self.count = 1

    def append(self, lineno):
        self.line_no = self.line_no + "," + str(lineno)
        self.count = self.count + 1

    def get_issue_name(self):
        return self.issue_name

    def get_line_no(self):
        return self.line_no

    def get_count(self):
        return self.count

def issue_cmp(issue1, issue2):
    return issue2.get_count() - issue1.get_count()

class FileIssuePack:
    
    def __init__(self, file_name):
        self.issue_list = []
        self.filename = file_name
        self.issue_count = 0

    def add_issue(self, issue, line_no):
        self.issue_count = self.issue_count + 1
        for i in range(len(self.issue_list)):
            if self.issue_list[i].get_issue_name() == issue:
                self.issue_list[i].append(line_no)
                return 
        issue = Issue(issue, line_no)
        self.issue_list.append(issue)

    def sort(self):
        self.issue_list.sort(issue_cmp)

    def get_issue_list(self):
        return self.issue_list

    def get_file_name(self):
        return self.filename

    def get_issue_count(self):
        return self.issue_count

def main():
    lines = []
    with open(sys.argv[1]) as fp:
        lines.extend([line.strip() for line in fp])

    file_issue_pack_list = []
    for each_line in lines:
        line_split = each_line.split(":")
        file_path = line_split[0].strip()
        issue_line_no = line_split[1].strip()
        issue = each_line.split("[")[-2].strip().split("]")[0].strip()

        if len(file_issue_pack_list) == 0 or file_path != file_issue_pack_list[-1].get_file_name():
            pack = FileIssuePack(file_path)
            pack.add_issue(issue, issue_line_no)
            file_issue_pack_list.append(pack)
        else:
            file_issue_pack_list[-1].add_issue(issue, issue_line_no)
    
    for each_issue_pack in file_issue_pack_list:
        each_issue_pack.sort()

    # write xls
    book = xlwt.Workbook()
    sheet = book.add_sheet("summary")
    sheet.col(0).width = 10000 
    sheet.col(1).width = 4000
    sheet.col(2).width = 8000
    sheet.col(3).width = 40000
    sheet.write(0, 0, r"file name")
    sheet.write(0, 1, r"error count")
    sheet.write(0, 2, r"error type")
    sheet.write(0, 3, r"line number")
    line_no = 1
    for i in range(len(file_issue_pack_list)):
        issue_pack = file_issue_pack_list[i]
        sheet.write(line_no, 0, issue_pack.get_file_name())
        sheet.write(line_no, 1, issue_pack.get_issue_count())
        line_no = line_no + 1
        issue_list = issue_pack.get_issue_list()
        for issue in issue_list:
            sheet.write(line_no, 1, issue.get_count())
            sheet.write(line_no, 2, issue.get_issue_name())
            sheet.write(line_no, 3, issue.get_line_no())
            line_no = line_no + 1

    sheet2 = book.add_sheet("detail")
    sheet2.col(0).width = 10000
    sheet2.col(1).width = 50000
    file_name = None
    line_no = 0
    for each_line in lines:
        file_path = each_line.split(":")[0].strip()
        if file_name == None or file_path != file_name:
            file_name = file_path
            sheet2.write(line_no, 0, file_name)
            sheet2.write(line_no, 1, "line " + each_line.lstrip(file_name).strip(":"))
            line_no = line_no + 1
        else:
            sheet2.write(line_no, 1, "line " + each_line.lstrip(file_name).strip(":"))
            line_no = line_no + 1

    book.save(sys.argv[2])

if __name__ == "__main__":
    main()

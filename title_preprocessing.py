import os
import re
import csv

class Title():
    def __init__(self):
        self.project_pwd = os.getcwd();
        self.TITLE = os.path.join(self.project_pwd,'dataset','title','titles1.csv')
        self.FILTER = os.path.join(self.project_pwd,'dataset','filters')
        self.RETULT = os.path.join(self.project_pwd,'dataset','title','titles1.csv')
        self.titles=[]
        self.brands=[]
        self.filters=[]

    def GetTitle(self):
        tmp_title = []
        with open(self.TITLE, 'rb') as title_file:
            for title_brand in title_file.readlines():
                title_brand = title_brand.strip()
                fileds = str(title_brand).replace(",,,","")
                fileds = fileds.lower()
                fileds = fileds.replace("\\'","'")
                fileds = fileds.replace("b\'\"","")
                fileds = fileds.replace("b\'","")
                fileds = fileds.replace("b\"","")
                fileds = fileds.replace("(","")
                fileds = fileds.replace(")","")
                fileds = fileds.split(',')
                # preprocess and add tmp title info
                tmp_title.append(fileds[:len(fileds)-1])
                # preprocess and add brand info
                if fileds[len(fileds)-1][-1] == '\'' or fileds[len(fileds)-1][-1] == '\"':
                    brand = fileds[len(fileds)-1][:len(fileds[len(fileds)-1])-1]
                    self.brands.append(brand)
                else:
                    self.brands.append(fileds[len(fileds)-1])

        title_file.close()

        # add title info
        for title in tmp_title:
            tmp = ''
            for i in range(len(title)):
                tmp += title[i]

            if tmp[-1] == '\'' or tmp[-1] == '\"':
                self.titles.append(tmp[:len(tmp)-1])
            else:
                self.titles.append(tmp)

        """
        # remove brand in title
        for i in range(len(self.titles)):
            a = self.titles[i]
            b = str(a).replace(self.brands[i],"")
            print(b)
        
        for i in range(len(self.titles)):
            print(self.brands[i], "|||" ,  self.titles[i])
        """

    def GetFilter(self):
        filter_files = os.listdir(self.FILTER)
        for files in filter_files:
            file_path = os.path.join(self.FILTER, files)
            count = 0
            with open(file_path, 'rb') as filter_file:
                for filter in filter_file.readlines():
                    count+=1
                    filter = filter.strip()
                    fileds = str(filter).replace("b\'","")
                    fileds = fileds.replace("b\"","")
                    fileds = fileds.lower()
                    if fileds[-1] == '\'' or fileds[-1] == '\"':
                        fileds = fileds[:len(fileds)-1]
                    if count != 1:
                        self.filters.append(fileds)


def title_preprocessing():
    AWS_title = Title()
    AWS_title.GetTitle()
    AWS_title.GetFilter()
    AWS_title.filters = sorted(AWS_title.filters, key=len)
    AWS_title.filters = AWS_title.filters[::-1]

    preprocessed_titles=[]
    for title in AWS_title.titles:
        for filter in AWS_title.filters:
            title = re.sub('\\b'+filter+'\\b',"",title)

        preprocessed_titles.append(title)
    """
    for i in range(len(preprocessed_titles)):
        if len(preprocessed_titles[i]) != len(AWS_title.titles[i]):
            print(len(AWS_title.titles[i]), AWS_title.titles[i])
            print(len(preprocessed_titles[i]), preprocessed_titles[i])
            print("####################3")
    """

    with open(AWS_title.RETULT,'w',encoding='utf-8',newline='') as result_file:
        wr = csv.writer(result_file)
        for i in range(len(preprocessed_titles)):
            wr.writerow([preprocessed_titles[i],AWS_title.brands[i]])

    result_file.close()

if __name__ == '__main__':
    title_preprocessing()
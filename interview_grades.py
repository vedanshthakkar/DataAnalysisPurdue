import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import heapq
import seaborn as sns

class DataVisualization:
    def __init__(self):
        self.data_dir = "data\interview_grades.csv"
        self.students = pd.DataFrame(pd.read_csv(self.data_dir))
        self.fillNullValues()
        self.outlierAnalysis()

    def fillNullValues(self):
        self.updated_students = self.students
        self.cols_to_be_updated = []
        for col_name in self.students.columns:
            if self.students[col_name].isnull().values.any():
                self.cols_to_be_updated.append(col_name)

        for col_name in self.cols_to_be_updated:
            self.updated_students[col_name] = self.updated_students[col_name].fillna(int(self.updated_students[col_name].mean()))

        if os.path.exists(self.data_dir.replace(".csv", "_updated_grades.csv")):
            os.remove(self.data_dir.replace(".csv", "_updated_grades.csv"))
        self.updated_students.to_csv(self.data_dir.replace(".csv", "_updated_updated.csv"))

    def outlierAnalysis(self):
        if not os.path.exists("figures"):
            os.mkdir("figures")
        for col_name in self.cols_to_be_updated:
            fig, ax = plt.subplots()
            sns.boxplot(self.updated_students[col_name], ax=ax)
            plt.savefig(os.path.join("figures", col_name+".png"))

    def trackStudentProgress(self, student_pk):
        # track GPA of a student over all the semesters
        df = self.updated_students[['academic_period_desc', 'student_pk', 'course_grade', 'course_pk', 'subject_pk']]
        student_to_academic_period = df.loc[df['student_pk'] == student_pk, "academic_period_desc"]
        student_to_grade = list(df.loc[df['student_pk'] == student_pk, "course_grade"])
        student_to_course = list(df.loc[df['student_pk'] == student_pk, "course_pk"])
        student_to_subject = list(df.loc[df['student_pk'] == student_pk, "subject_pk"])
        student_pk_indices = df[df['student_pk'] == student_pk].index

        heap = []
        curr_idx = 0
        for sem in student_to_academic_period:
            heapq.heappush(heap, (sem, student_to_course[curr_idx], student_to_subject[curr_idx], student_to_grade[curr_idx], student_pk_indices[curr_idx]))
            curr_idx += 1

        hashmap = {}
        for element in heap:
            if element[0] not in hashmap:
                hashmap[element[0]] = [element[3]]
            else:
                hashmap[element[0]].append(element[3])

        for element in hashmap:
            hashmap[element] = sum(hashmap[element])/len(hashmap[element])

        names = list(hashmap.keys())
        values = list(hashmap.values())

        plt.bar(range(len(hashmap)), values, tick_label=names)
        plt.xlabel("Semesters")
        plt.ylabel("GPA")
        plt.title("Track of a Student's GPA over time")
        plt.xticks(rotation=90)
        plt.show()

obj = DataVisualization()
obj.trackStudentProgress(student_pk=1477)

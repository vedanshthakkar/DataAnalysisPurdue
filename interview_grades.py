import pandas as pd
import matplotlib.pyplot as plt
import heapq
import numpy as np
from matplotlib import colors
import seaborn as sns
from interview_student_profile import DataVisualization

class AnalyzeData:
    def __init__(self, data_dir):
        students = pd.DataFrame(pd.read_csv(data_dir))
        self.updated_students, self.cols_to_be_updated = DataVisualization.fillNullValues(self, students, data_dir)
        DataVisualization.outlierAnalysis(self, self.updated_students, self.cols_to_be_updated)

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

    def coursePerformance(self, semester):
        # for a given semester which course performs the best? compute avg gpa of all the students enrolled in a given semester. Compute avg GPA of all the courses
        # offered in that semester and plot the histogram
        df = self.updated_students[['academic_period_desc', 'course_pk', 'course_grade']]
        semester_to_grade = list(df.loc[df['academic_period_desc'] == semester, "course_grade"])
        semester_to_course = list(df.loc[df['academic_period_desc'] == semester, "course_pk"])

        hashmap = {}
        for i in range(len(semester_to_course)):
            if semester_to_course[i] not in hashmap:
                hashmap[semester_to_course[i]] = [semester_to_grade[i]]
            else:
                hashmap[semester_to_course[i]].append(semester_to_grade[i])

        for element in hashmap:
            hashmap[element] = sum(hashmap[element])/len(hashmap[element])

        n_bins = 10
        # Creating distribution
        x = hashmap.values()
        fig, axs = plt.subplots(1, 1,
                                figsize=(10, 7),
                                tight_layout=True)

        for s in ['top', 'bottom', 'left', 'right']:
            axs.spines[s].set_visible(False)

        axs.xaxis.set_ticks_position('none')
        axs.yaxis.set_ticks_position('none')

        axs.xaxis.set_tick_params(pad=5)
        axs.yaxis.set_tick_params(pad=10)

        # Add x, y gridlines
        axs.grid(b=True, color='grey',
                 linestyle='-.', linewidth=0.5,
                 alpha=0.6)

        # Add Text watermark
        fig.text(0.9, 0.15, '',
                 fontsize=12,
                 color='red',
                 ha='right',
                 va='bottom',
                 alpha=0.7)

        N, bins, patches = axs.hist(x, bins=n_bins)

        fracs = ((N ** (1 / 5)) / N.max())
        norm = colors.Normalize(fracs.min(), fracs.max())
        for thisfrac, thispatch in zip(fracs, patches):
            color = plt.cm.viridis(norm(thisfrac))
            thispatch.set_facecolor(color)

        plt.xlabel("GPA Intervals")
        plt.ylabel("Number of Courses")
        plt.title("Distribution of GPA in "+semester)
        plt.show()

obj = AnalyzeData(data_dir = "data\interview_grades.csv")
obj.trackStudentProgress(student_pk=1477)
obj.coursePerformance(semester='Fall 2017')
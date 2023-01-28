import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualization:
    def __init__(self, data_dir):
        students = pd.DataFrame(pd.read_csv(data_dir))
        self.updated_students, self.cols_to_be_updated = self.fillNullValues(students, data_dir)
        self.outlierAnalysis(self.updated_students, self.cols_to_be_updated)

    def fillNullValues(self, students, data_dir):
        updated_students = students
        cols_to_be_updated = []
        for col_name in students.columns:
            if students[col_name].isnull().values.any():
                cols_to_be_updated.append(col_name)

        for col_name in cols_to_be_updated:
            updated_students[col_name] = updated_students[col_name].fillna(int(updated_students[col_name].mean()))

        if os.path.exists(data_dir.replace(".csv", "_updated.csv")):
            os.remove(data_dir.replace(".csv", "_updated.csv"))
        updated_students.to_csv(data_dir.replace(".csv", "_updated.csv"))
        return updated_students, cols_to_be_updated

    def outlierAnalysis(self, updated_students, cols_to_be_updated):
        if not os.path.exists("figures"):
            os.mkdir("figures")
        for col_name in cols_to_be_updated:
            fig, ax = plt.subplots()
            sns.boxplot(updated_students[col_name], ax=ax)
            plt.savefig(os.path.join("figures", col_name+".png"))

    def removeOutliers(self):
        # There are not many outliers so skipping this step
        pass

    def computeTypeBasedAvgScores(self, basis, unique_list):
        hashmap_avg = {}
        hashmap_act = {}
        hashmap_sat = {}
        hashmap_hs = {}

        df = self.updated_students
        for i in range(len(unique_list)):
            sat_sections = 0
            act_sections = 0
            final_avg_score = 0
            final_act_avg_score = 0
            final_sat_avg_score = 0
            final_hs_avg_percentile = 0
            for j in range(len(self.cols_to_be_updated)):
                temp = df.loc[df[basis] == unique_list[i], self.cols_to_be_updated[j]]
                avg_score = sum(temp)/len(temp)
                final_avg_score += avg_score
                if "act" in self.cols_to_be_updated[j]:
                    final_act_avg_score += avg_score
                    act_sections += 1
                if "sat" in self.cols_to_be_updated[j]:
                    final_sat_avg_score += avg_score
                    sat_sections += 1
                if "high_school" in self.cols_to_be_updated[j]:
                    final_hs_avg_percentile += avg_score
            hashmap_hs[unique_list[i]] = final_hs_avg_percentile
            hashmap_act[unique_list[i]] = final_act_avg_score/sat_sections
            hashmap_sat[unique_list[i]] = final_sat_avg_score / act_sections
            hashmap_avg[unique_list[i]] = final_avg_score/len(self.cols_to_be_updated)

        avg_overall_scores = list(hashmap_avg.values())
        avg_hs_scores = list(hashmap_hs.values())
        avg_act_scores = list(hashmap_act.values())
        avg_sat_scores = list(hashmap_sat.values())

        X_axis = np.arange(len(unique_list))
        plt.bar(X_axis, avg_overall_scores, 0.2, label='avg_overall')
        plt.bar(X_axis-0.2, avg_hs_scores, 0.2, label='avg_high_school')
        plt.bar(X_axis+0.2, avg_act_scores, 0.2, label='avg_act')
        plt.bar(X_axis+0.4, avg_sat_scores, 0.2, label='avg_sat')

        plt.xticks(X_axis, unique_list)
        plt.xlabel("profile_college")
        plt.ylabel("Scores")
        plt.title("Avgerage test scores")
        plt.legend()
        plt.show()

    def computeCollegeBasedAvgScores(self):
        # computes the avg scores of  SAT, ACT, HS, and overall(SAT+ACT+HS) exams that were admitted to a particular college
        unique_list = self.updated_students.profile_college.unique().tolist()
        self.computeTypeBasedAvgScores("profile_college", unique_list)

    def computeResidenceBasedAvgScores(self):
        # compute avg scores of ACT, SAT, HS and overall(SAT+ACT+HS) for each group of students - F,R,NR
        unique_list = self.updated_students.profile_residence.unique().tolist()
        self.computeTypeBasedAvgScores("profile_residence", unique_list)

    def compareResidenceBasedScore(self, subject):
        df = self.updated_students[['profile_residence', subject]]
        g = sns.catplot(data=df, kind="bar", x="profile_residence", y=subject, palette="dark", alpha=.6, height=6)
        g.set_axis_labels("profile_residence", "Score of "+subject)
        g.fig.suptitle("Residence based Scores of "+subject)
        for ax in g.axes.flat:
            ax.bar_label(ax.containers[0])
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=0)
        plt.show()

    def compareResidenceBasedMath(self):
        # compares ACT math scores of diff types of residences
        self.compareResidenceBasedScore("profile_highest_act_math")

    def compareResidenceBasedEnglish(self):
        # compares ACT english scores of diff types of residences
        self.compareResidenceBasedScore("profile_highest_act_english")

    def getNumStudentTypesInEachCollege(self):
        # For every college, computes how many F,NR,R are there
        hashmap = {}
        unique_colleges = self.updated_students.profile_college.unique().tolist()
        unique_residences = self.updated_students.profile_residence.unique().tolist()
        df = self.updated_students[['profile_college', 'profile_residence']]
        for i in range(len(unique_colleges)):
            N_count = 0
            R_count = 0
            F_count = 0
            temp = df.loc[df['profile_college'] == unique_colleges[i], "profile_residence"]
            for element in temp:
                if element == "N":
                    N_count += 1
                elif element == "R":
                    R_count += 1
                else:
                    F_count += 1
            hashmap[unique_colleges[i]] = [N_count, R_count, F_count]

        keys = [key for key in hashmap.keys()]
        values = [value for value in hashmap.values()]

        fig, ax = plt.subplots()
        ax.bar(np.arange(len(keys)),[value[0] for value in values],width=0.2, align='center')
        ax.bar(np.arange(len(keys)) + 0.2, [value[1] for value in values], width=0.2, align='center')
        ax.bar(np.arange(len(keys)) - 0.2, [value[2] for value in values], width=0.2, align='center')
        ax.set_xticklabels(keys)
        ax.set_xticks(np.arange(len(keys)))
        plt.xlabel("profile_colleges")
        plt.ylabel("Count")
        plt.title("Number of Resident types in each college")
        plt.legend(unique_residences)
        plt.show()

    def computeNumOfStudentsInEachCollege(self):
        sns.set(font_scale=1)
        g = sns.catplot(x='profile_college', kind='count', data=self.updated_students, orient='h').set(title="Number of Students in Each College")
        for ax in g.axes.flat:
            ax.bar_label(ax.containers[0])
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=0)
        plt.show()

if __name__ == "__main__":
    obj = DataVisualization(data_dir = "data\interview_student_profile.csv")
    obj.computeCollegeBasedAvgScores()
    obj.computeResidenceBasedAvgScores()
    obj.compareResidenceBasedMath()
    obj.compareResidenceBasedEnglish()
    obj.getNumStudentTypesInEachCollege()
    obj.computeNumOfStudentsInEachCollege()
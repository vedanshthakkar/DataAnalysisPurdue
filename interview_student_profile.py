import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualization:
    def __init__(self):
        self.data_dir = "data\interview_student_profile.csv"
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

        if os.path.exists(self.data_dir.replace(".csv", "_updated.csv")):
            os.remove(self.data_dir.replace(".csv", "_updated.csv"))
        self.updated_students.to_csv(self.data_dir.replace(".csv", "_updated.csv"))

    def outlierAnalysis(self):
        if not os.path.exists("figures"):
            os.mkdir("figures")
        for col_name in self.cols_to_be_updated:
            fig, ax = plt.subplots()
            sns.boxplot(self.updated_students[col_name], ax=ax)
            plt.savefig(os.path.join("figures", col_name+".png"))

    def removeOutliers(self):
        pass

    def catPlot(self, key, title):
        sns.set(font_scale=1)
        g = sns.catplot(x=key, kind='count', data=self.updated_students, orient='h').set(title=title)
        for ax in g.axes.flat:
            ax.bar_label(ax.containers[0])
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=0)
        plt.show()

    def computeNumOfStudentsInEachCollege(self):
        self.catPlot(key='profile_college', title="Number of Students in Each College")

    def computeCollegeBasedAvgScores(self):
        # computes the avg scores of overall, SAT, ACT, and HS exams that were admitted to a particular college
        unique_colleges = self.updated_students.profile_college.unique().tolist()
        hashmap_avg = {}
        hashmap_act = {}
        hashmap_sat = {}
        hashmap_hs = {}

        df = self.updated_students
        for i in range(len(unique_colleges)):
            final_avg_score = 0
            final_act_avg_score = 0
            final_sat_avg_score = 0
            final_hs_avg_percentile = 0
            for j in range(len(self.cols_to_be_updated)):
                temp = df.loc[df['profile_college'] == unique_colleges[i], self.cols_to_be_updated[j]]
                avg_score = sum(temp)/len(temp)
                final_avg_score += avg_score
                if "act" in self.cols_to_be_updated[j]:
                    final_act_avg_score += avg_score
                if "sat" in self.cols_to_be_updated[j]:
                    final_sat_avg_score += avg_score
                if "high_school" in self.cols_to_be_updated[j]:
                    final_hs_avg_percentile += avg_score
            hashmap_hs[unique_colleges[i]] = final_hs_avg_percentile
            hashmap_act[unique_colleges[i]] = final_act_avg_score/3 #total 3 sections in SAT
            hashmap_sat[unique_colleges[i]] = final_sat_avg_score / 6 #total 6 sections in ACT
            hashmap_avg[unique_colleges[i]] = final_avg_score/len(self.cols_to_be_updated)

        avg_overall_scores = list(hashmap_avg.values())
        avg_hs_scores = list(hashmap_hs.values())
        avg_act_scores = list(hashmap_act.values())
        avg_sat_scores = list(hashmap_sat.values())

        X = unique_colleges

        X_axis = np.arange(len(X))

        plt.bar(X_axis, avg_overall_scores, 0.2, label='avg_overall')
        plt.bar(X_axis-0.2, avg_hs_scores, 0.2, label='avg_high_school')
        plt.bar(X_axis+0.2, avg_act_scores, 0.2, label='avg_act')
        plt.bar(X_axis+0.4, avg_sat_scores, 0.2, label='avg_sat')

        plt.xticks(X_axis, X)
        plt.xlabel("profile_college")
        plt.ylabel("Scores")
        plt.title("Avgerage test scores")
        plt.legend()
        plt.show()

    def computeResidenceBasedAvgScores(self):
        # compute avg scores of ACT, SAT and HS for each group of students - F,R,NR
        unique_residences = self.updated_students.profile_residence.unique().tolist()
        hashmap_act = {}
        hashmap_sat = {}
        hashmap_hs = {}

        df = self.updated_students
        for i in range(len(unique_residences)):
            final_act_avg_score = 0
            final_sat_avg_score = 0
            final_hs_avg_percentile = 0
            for j in range(len(self.cols_to_be_updated)):
                temp = df.loc[df['profile_residence'] == unique_residences[i], self.cols_to_be_updated[j]]
                avg_score = sum(temp) / len(temp)
                if "act" in self.cols_to_be_updated[j]:
                    final_act_avg_score += avg_score
                if "sat" in self.cols_to_be_updated[j]:
                    final_sat_avg_score += avg_score
                if "high_school" in self.cols_to_be_updated[j]:
                    final_hs_avg_percentile += avg_score
            hashmap_hs[unique_residences[i]] = final_hs_avg_percentile
            hashmap_act[unique_residences[i]] = final_act_avg_score / 3  # total 3 sections in SAT
            hashmap_sat[unique_residences[i]] = final_sat_avg_score / 6  # total 6 sections in ACT

        avg_hs_scores = list(hashmap_hs.values())
        avg_act_scores = list(hashmap_act.values())
        avg_sat_scores = list(hashmap_sat.values())

        def addlabels(x, y):
            for i in range(len(x)):
                plt.text(i, y[i], int(y[i]))

        X_axis = np.arange(len(unique_residences))

        plt.bar(X_axis, avg_hs_scores, 0.2, label='avg_high_school')
        addlabels(unique_residences, avg_hs_scores)
        plt.bar(X_axis + 0.2, avg_act_scores, 0.2, label='avg_act')
        addlabels(unique_residences, avg_act_scores)
        plt.bar(X_axis - 0.2, avg_sat_scores, 0.2, label='avg_sat')
        addlabels(unique_residences, avg_sat_scores)
        plt.xticks(X_axis, unique_residences)
        plt.xlabel("profile_residence")
        plt.ylabel("Scores")
        plt.title("Avgerage test scores")
        plt.legend()
        plt.show()


    def compareResidenceBasedMath(self):
        # compares ACT math scores of diff types of residences
        df = self.updated_students[['profile_residence', 'profile_highest_act_math']]
        g = sns.catplot(
            data=df, kind="bar",
            x="profile_residence", y="profile_highest_act_math", palette="dark", alpha=.6, height=6)

        g.set_axis_labels("profile_residence", "Score in ACT Math")
        g.fig.suptitle("Residence based Scores in ACT Math")
        for ax in g.axes.flat:
            ax.bar_label(ax.containers[0])
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=0)
        plt.show()

    def compareResidenceBasedEnglish(self):
        # compares ACT english scores of diff types of residences
        df = self.updated_students[['profile_residence', 'profile_highest_act_english']]
        g = sns.catplot(
            data=df, kind="bar",
            x="profile_residence", y="profile_highest_act_english", palette="dark", alpha=.6, height=6)

        g.set_axis_labels("profile_residence", "Score in ACT English")
        g.fig.suptitle("Residence based Scores in ACT English")
        for ax in g.axes.flat:
            ax.bar_label(ax.containers[0])
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=0)
        plt.show()

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

if __name__ == "__main__":
    obj = DataVisualization()
    obj.computeCollegeBasedAvgScores()
    obj.computeResidenceBasedAvgScores()
    obj.compareResidenceBasedMath()
    obj.compareResidenceBasedEnglish()
    obj.getNumStudentTypesInEachCollege()
    obj.computeNumOfStudentsInEachCollege()
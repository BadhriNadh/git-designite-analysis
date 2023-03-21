# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import subprocess

import git
import pandas
import csv


def clone():
    url = "https://github.com/google/gson"
    path = "./gson"
    repo = git.Repo.clone_from(url, path)
    commits = list(repo.iter_commits())
    header = ['commit', 'ArchitectureSmells', 'DesignSmells', 'ImplementationSmells', 'Smells', 'LOC']
    with open('report.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    for i in range(0, len(commits), round(len(commits) / 2)):
        repo.git.checkout(commits[i])
        run_dj(str(commits[i]) + '-' + str(i))
        dance(str(commits[i]) + '-' + str(i))


def run_dj(name):
    subprocess.run(['mkdir', name], check=True)
    subprocess.run(['java', '-jar', 'DesigniteJava.jar', '-i', './gson', '-o', './' + name], check=True)


def dance(name):
    architecture_smells = pandas.read_csv('./' + name + '/ArchitectureSmells.csv')
    design_smells = pandas.read_csv('./' + name + '/DesignSmells.csv', usecols=[0])
    implementation_smells = pandas.read_csv('./' + name + '/ImplementationSmells.csv')
    type_metrics = pandas.read_csv('./' + name + '/TypeMetrics.csv')
    smells = len(architecture_smells) + len(design_smells) + len(implementation_smells)
    data = [name, len(architecture_smells), len(design_smells), len(implementation_smells), smells, type_metrics['LOC'].sum(skipna=False)]
    with open('report.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow(data)


if __name__ == '__main__':
    clone()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

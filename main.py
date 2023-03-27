import subprocess
import git
import pandas
import csv


def clone():
    url = "https://github.com/mybatis/mybatis-3.git"
    path = "./repo"
    repo = git.Repo.clone_from(url, path)
    commits = list(repo.iter_commits())
    header = ['commit', 'ArchitectureSmellsDensity', 'DesignSmellsDensity', 'ImplementationSmellsDensity',
              'TotalSmells', 'LOC', 'MAX_LOC', 'AVG_LOC', 'MAX_LCOM', 'AVG_LCOM', 'MAX_WMC', 'AVG_WMC']
    with open('report.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    for i in range(0, len(commits), round(len(commits) / 10)):
        repo.git.checkout(commits[i])
        start_dj(str(commits[i]) + '-' + str(i))
        report_generator(str(commits[i]) + '-' + str(i), url)


def start_dj(name):
    subprocess.run(['mkdir', name], check=True)
    subprocess.run(['java', '-jar', 'DesigniteJava.jar', '-i', './repo', '-o', './' + name], check=True)


def report_generator(name, url):
    architecture_smells = pandas.read_csv('./' + name + '/ArchitectureSmells.csv')
    design_smells = pandas.read_csv('./' + name + '/DesignSmells.csv', usecols=[3])
    implementation_smells = pandas.read_csv('./' + name + '/ImplementationSmells.csv')
    type_metrics = pandas.read_csv('./' + name + '/TypeMetrics.csv')
    total_loc = type_metrics['LOC'].sum(skipna=False)
    smells = len(architecture_smells) + len(design_smells) + len(implementation_smells)
    data = [name,
            len(architecture_smells) * 1000 / total_loc,
            len(design_smells) * 1000 / total_loc,
            len(implementation_smells) * 1000 / total_loc,
            smells,
            total_loc,
            type_metrics['LOC'].max(skipna=False),
            type_metrics['LOC'].mean(skipna=False),
            type_metrics.loc[type_metrics['LCOM'] != -1, 'LCOM'].max(skipna=False),
            type_metrics.loc[type_metrics['LCOM'] != -1, 'LCOM'].mean(skipna=False),
            type_metrics.loc[type_metrics['WMC'] != -1, 'WMC'].max(skipna=False),
            type_metrics.loc[type_metrics['WMC'] != -1, 'WMC'].mean(skipna=False)]
    with open('report.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    finder(url, name, design_smells, 'Design Smell', 'Rebellious Hierarchy')


def flip():
    report = pandas.read_csv('report.csv')
    num_rows = len(report)
    df_flipped = report.iloc[num_rows - 1::-1]
    df_flipped.to_csv('report_flipped.csv', index=False)


def finder(url, commit, dataframe, smell_type, smell_name):
    if dataframe[smell_type].str.contains(smell_name).any():
        data = [url, commit]
        with open('findings.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow(data)


if __name__ == '__main__':
    clone()
    flip()

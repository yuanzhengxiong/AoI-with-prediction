from __future__ import division
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import pandas as pd
import os
import csv

def plot_3d(df_ps, age_type):
    fig = plt.figure()
    for i, df_p in enumerate(df_ps):
        ws = df_p['w'].values
        ss = df_p['s'].values
        avgs = df_p['avg_age'].values
        maxs = df_p['max_age'].values
        ax = fig.add_subplot(3,3,i+1,projection='3d')
        if (age_type == 'avg'):
            ax.plot3D(ws, ss, avgs)
        else:
            ax.plot3D(ws, ss, maxs)
        ax.set_xlabel('w')
        ax.set_ylabel('s')
        if (age_type =='avg'):
            ax.set_zlabel('avg_age')
        else:
            ax.set_zlabel('max_age')
        ax.set_title('p='+str((i+1)/10))

def plot_s_given_pw(df, p, w, age_type, ax, img_path, writer):
    #base_avg_age = df[df.w==1]['avg_age'].values[0]
    #base_max_age = df[df.w==1]['max_age'].values[0]
    age_type = age_type+'_age'
    base_age = df[df.w==1][age_type].values[0]
    df_w = df[df.w==w]
    ss = df_w['s'].values

    vals = df_w[age_type].values
    ax.plot(ss, vals)
    ax.plot([1,w], [base_age, base_age])
    ax.scatter(ss, vals)
    ax.set_ylabel(age_type)
    best_row = df.iloc[df_w[age_type].idxmin()]
    s = best_row['s']
    best_age = best_row[age_type]
    gain = best_age/base_age
    data_dict = {'p': '{:.2f}'.format(p), 
                 'w': '{:03d}'.format(int(w)),
                 's': '{:03d}'.format(int(s)),
                 'base': '{:f}'.format(base_age), 
                 'best': '{:f}'.format(best_age), 
                 'gain': '{:f}'.format(gain)}
    writer.writerow(data_dict)

    # if (age_type =='avg'):
    #     avgs = df_w['avg_age'].values
    #     ax.plot(ss, avgs)
    #     ax.plot([1,w], [base_avg_age, base_avg_age])
    #     ax.scatter(ss, avgs)
    #     ax.set_ylabel('avg_age')
    #     best_row = df.iloc[df_w['avg_age'].idxmin()]
    #     s = best_row['s']
    #     best_avg_age = best_row['avg_age']
    #     gain = best_avg_age/base_avg_age
    #     data_dict = {'p': '{:.2f}'.format(p), 
    #                  'w': '{:03d}'.format(int(w)),
    #                  's': '{:03d}'.format(int(s)),
    #                  'base': '{:f}'.format(base_avg_age), 
    #                  'best': '{:f}'.format(best_avg_age), 
    #                  'gain': '{:f}'.format(gain)}
    #     writer.writerow(data_dict)

    # else:
    #     maxs = df_w['max_age'].values
    #     ax.plot(ss, maxs)
    #     ax.plot([1,w], [base_max_age, base_max_age])
    #     ax.scatter(ss, maxs)
    #     ax.set_ylabel('max_age')

    ax.set_xlabel('s')
    title = 'p={0:.2f}, w={1:03d}'.format(p, w)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(img_path+title+'.png')

def main():
    avg_num = int(1e4)
    time_range = 300
    arrival_type = 'Bernoulli'
    policy = 'equal_spreading' 
    w_range = [1, time_range//10]
    age_type = 'avg'

    img_path = './imgs/av_{0}_tr_{1}_ar_{2}/'.format(avg_num, time_range, arrival_type)
    if not os.path.isdir(img_path):
        os.mkdir(img_path)
    img_path = img_path+age_type+'/'
    if not os.path.isdir(img_path):
        os.mkdir(img_path)

    csv_file = open(img_path+'{:s}_analysis.csv'.format(age_type), mode='w')
    fieldnames=['p', 'w', 's', 'base', 'best', 'gain']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for w in range(2, time_range//10+1):
        for p in [x/100 for x in range(5, 55, 5)]:
            filename = "av_{0}_tr_{1}_ar_{2}_po_{3}_p_{4}_wr_{5}-{6}.csv".format(avg_num, time_range, arrival_type, policy, p, w_range[0], w_range[1])
            path = './data/'+'av_{0}_tr_{1}_ar_{2}/'.format(avg_num, time_range, arrival_type)+filename
            df = pd.read_csv(path, header=0)
            fig = plt.figure() 
            ax = fig.add_subplot(1,1,1)
            plot_s_given_pw(df, p, w, age_type, ax, img_path, writer)
            plt.close(fig)

if __name__ == '__main__':
    main()

from __future__ import division
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import pandas as pd

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

def plot_s(df_ps, w, age_type):
    fig = plt.figure() 
    for i, df_p in enumerate(df_ps):
        base_avg_age = df_p[df_p.w==1]['avg_age'].values[0]
        base_max_age = df_p[df_p.w==1]['max_age'].values[0]
        df_p_w = df_p[df_p.w==w]
        ss = df_p_w['s'].values
        avgs = df_p_w['avg_age'].values
        maxs = df_p_w['max_age'].values
        ax = fig.add_subplot(3,3,i+1)
        if (age_type =='avg'):
            ax.plot(ss, avgs)
        else:
            ax.plot(ss, maxs)
        if (age_type =='avg'):
            ax.plot([1,w], [base_avg_age, base_avg_age])
        else:
            ax.plot([1,w], [base_max_age, base_max_age])
        ax.set_xlabel('s')
        if (age_type =='avg'):
            ax.set_ylabel('avg_age')
        else:
            ax.set_ylabel('max_age')
        ax.set_title('p='+str((i+1)/10)+','+'w='+str(w))
    
def plot_w(df_ps, s, age_type):
    fig = plt.figure() 
    for i, df_p in enumerate(df_ps):
        base_avg_age = df_p[df_p.w==1]['avg_age'].values[0]
        base_max_age = df_p[df_p.w==1]['max_age'].values[0]
        df_p_s = df_p[df_p.s==s]
        ws = df_p_s['w'].values
        avgs = df_p_s['avg_age'].values
        maxs = df_p_s['max_age'].values
        ax = fig.add_subplot(3,3,i+1)
        if (age_type =='avg'):
            ax.plot(ws, avgs)
            ax.scatter(ws, avgs)
        else:
            ax.plot(ws, maxs)
            ax.scatter(ws, maxs)
        if (age_type =='avg'):
            ax.plot([ws[0],ws[-1]], [base_avg_age, base_avg_age])
        else:
            ax.plot([ws[0],ws[-1]], [base_max_age, base_max_age])
        ax.set_xlabel('w')
        if (age_type =='avg'):
            ax.set_ylabel('avg_age')
        else:
            ax.set_ylabel('max_age')
        ax.set_title('p='+str((i+1)/10)+','+'s='+str(s))


def main():
    df = pd.read_csv('./data_for_equal_spreading.csv_100', header=0)
    df_ps = []
    for i in [x/10 for x in range(1, 10)]: 
        df_ps.append(df[df.p==i])
    
    #plot_3d(df_ps, 'avg')

    for i in range(2, 11):
        plot_s(df_ps, i, 'avg') 
        plt.tight_layout()

    #for i in range(1, 11):
    #    plot_w(df_ps, i, 'avg') 
    #    plt.tight_layout()

    plt.show()

if __name__ == '__main__':
    main()


import numpy as np
import matplotlib.pyplot as plt

def parse_results(path):
    pr_seed = []
    pr_adopters = []
    eigen_seed = []
    eigen_adopters = []
    bet_seed = []
    bet_adopters = []
    with open(path, 'r') as fp:
        for line in fp:
            if '#' in line:
                continue
            row = line.split()
            pr_seed.append(row[0])
            pr_adopters.append(row[1])
            eigen_seed.append(row[2])
            eigen_adopters.append(row[3])
            bet_seed.append(row[4])
            bet_adopters.append(row[5])

    fp.close()
    return (np.column_stack((map(int, pr_seed), map(int, pr_adopters))),
           np.column_stack((map(int, eigen_seed), map(int, eigen_adopters))),
           np.column_stack((map(int, bet_seed), map(int, bet_adopters))))

def graph_stats(path):
    edges = []
    clustering = []
    
    with open(path, 'r') as fp:
        for line in fp:
            if '#' and '=' not in line:
                continue
            row = line.split()
            edges.append(int(row[2]))
            clustering.append(float(row[6]))

    fp.close()
    return np.mean(edges), np.mean(clustering)

def get_percentage(data):
    N = np.shape(data)[0]
    seeds = list(set(data[:,0]))
    seeds.sort()
    return [(i, float(len([x for x in data[:,0] if x == i]))/N) for i in seeds]

def get_avg_per_seed(data):
    seeds = list(set(data[:,0]))
    seeds.sort()
    return [(i, np.mean([x for j,x in enumerate(data[:,1]) if i == data[:,0][j]])) for i in seeds]

def draw_pie(perc):
    labels = tuple(['Top {}'.format(t[0]) for t in perc])
    sizes = [p[1]*100 for p in perc]
    explode = tuple(0.0 for _ in xrange(len(sizes)-1))
    explode += 0.1,
    plt.pie(sizes, explode=explode, labels=labels,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    
def draw_bars(pr, eigen, bet, bar_width = 0.32, opacity = 0.4):
    fig, ax = plt.subplots(figsize=(20,15))
    
    loc = np.arange(np.shape(pr)[0])
    rects1 = plt.bar(loc, pr[:,1], bar_width,
                     alpha=opacity,
                     color='b',
                     label='Page Rank')

    rects2 = plt.bar(loc+bar_width, eigen[:,1], bar_width,
                     alpha=opacity,
                     color='r',
                     label='Eigenvector')

    rects3 = plt.bar(loc+2*bar_width, bet[:,1], bar_width,
                     alpha=opacity,
                     color='y',
                     label='Betweenness')

    plt.xlabel('Top 90 - 95 - 100')
    plt.ylabel('Adopters')
    plt.title('Adopters Comparison')
    plt.tick_params(axis='x',
                   which='both',
                   bottom='off',
                   top='off',
                   labelbottom='off')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.subplots_adjust(hspace=0.3)
    plt.tight_layout()

def draw_bars_comparison(title, ylabel, top_seeds, bar_width = 0.35, opacity = 0.4):
    fig, ax = plt.subplots()
    colors = ['b', 'r', 'y', 'c', 'g']
    
    rects = []
    shape = np.shape(top_seeds)[0]
    for i in xrange(shape-1):
        rects.append(plt.bar(i, top_seeds[i,1], bar_width,
                         alpha=opacity,
                         color=colors[i],
                         label='Top {}'.format(int(top_seeds[:,0][i]))))

    
    rects.append(plt.bar(shape, top_seeds[shape-1,1], bar_width,
                     alpha=1,
                     color=colors[-1],
                     label='Complete Avg'))

    plt.xlabel('Seeds')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks([i+0.2 for i in xrange(shape-1)], map(int,top_seeds[:,0]))

    for r in rects:
        autolabel(r, ax)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.subplots_adjust(hspace=0.3)
    plt.tight_layout()
    
def draw_avg_infected(avg_infected, title, xlabel, ylabel, labels=['WikiVote', 'RandomGraph', 'WattsStrogatz', 'GeneralizedWS'], bar_width = 0.35, opacity = 0.4):
    fig, ax = plt.subplots()
    colors = ['b', 'r', 'y', 'c', 'g']
    
    rects = []
    shape = np.shape(avg_infected)[0]
    for i in xrange(shape):
        rects.append(plt.bar(i, avg_infected[i], bar_width,
                         alpha=opacity,
                         color=colors[i],
                         label=labels[i]))

    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks([i+0.2 for i in xrange(shape)], labels)

    for r in rects:
        autolabel(r, ax)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.subplots_adjust(hspace=0.3)
    plt.tight_layout()

def draw_avgs(means, bar_width = 0.35, opacity = 0.4):
    fig, ax = plt.subplots()
    
    

    rects1 = plt.bar(1, means[0], bar_width,
                     alpha=opacity,
                     color='b',
                     label='Page Rank')

    rects2 = plt.bar(2, means[1], bar_width,
                     alpha=opacity,
                     color='r',
                     label='Eigenvector')

    rects3 = plt.bar(3, means[2], bar_width,
                     alpha=opacity,
                     color='y',
                     label='Betweenness')

    plt.xlabel('Centrality Measures')
    plt.ylabel('Adopters Avg')
    plt.title('Avg Adopters Comparison')
    plt.xticks([1.2,2.2,3.2], ('PR', 'E', 'B'))

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    for r in [rects1, rects2, rects3]:
        autolabel(r, ax)

    plt.subplots_adjust(hspace=0.3)
    plt.tight_layout()

def autolabel(rects, ax):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')
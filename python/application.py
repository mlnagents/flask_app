from flask import Flask, render_template
import json
import glob
import re
import numpy as np
import pandas as pd
NUMBERTOSHOW = 100
app = Flask(__name__)
datasets_files = glob.glob('./datasets/*.json')
datasets = {}
def min_max(arr):
    x_min, y_min = np.min(arr, axis=0)
    x_max, y_max = np.max(arr, axis=0)
    return [x_min, y_min, x_max, y_max]
for df in datasets_files:
    file_name = re.findall('/([-\w\d]+).json',df)[0]
    with open(df, 'r') as f:
        data = json.load(f)
    datasets.update({file_name: data})

pd_table = pd.DataFrame([(tn, exmpl_i, obj_i, obj['class'], min_max([[int(p['x']),int(p['y'])] for p in obj['polygon']['vertexes']]), example['source'])
                        for tn in datasets.keys()
                        for exmpl_i, example in enumerate(datasets[tn])
                        for obj_i, obj in enumerate(example['objects'])],
                        columns=['dataset','image','object','class','vert','url'])
@app.route('/')
def hello_world():
    datasets = pd_table['dataset'].unique()
    unique_classes = pd_table['class'].unique()
    return render_template('list_of_markups.html', m_classes = unique_classes,
                           datasets = datasets)

@app.route('/class_view/<m_class>')
def class_view(m_class):
    class_table = pd_table[pd_table['class'] == m_class]
    if len(class_table) < NUMBERTOSHOW:
        sample = class_table
    else:
        sample = class_table.sample(NUMBERTOSHOW)
    return render_template('list_of_images.html', objects=sample.iterrows())

@app.route('/dataset_view/<dataset>')
def dataset_view(dataset):
    dataset_table = pd_table[pd_table['dataset'] == dataset]
    dataset_size = dataset_table['image'].max()+1
    if dataset_size < NUMBERTOSHOW:
        sample = dataset_table
    else:
        rand_int = np.random.choice(dataset_size, NUMBERTOSHOW, replace=False)
        sample = dataset_table[dataset_table['image'].isin(rand_int)]

    sample = [{'image': r[0], 'url': r[1]['url'].iloc[0], 'elements': [[a,b] for a,b in zip(r[1]['class'], r[1]['vert'])]} for r in dataset_table.groupby('image').__iter__()]
    return render_template('dataset_page.html', objects=sample)
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

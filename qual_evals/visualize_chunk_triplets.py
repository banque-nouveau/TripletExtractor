"""This script requries a filename for a csv file  with unique indexes for each chunk, and the headers :
```
idx,subject,subject_type,relation,object,object_type,input,wiki_page
```
The `wiki_page` column is not used

"""
import gradio as gr
import json
import pandas as pd

#filename = "data/combined_df.csv"
# filename = "/Users/rbiswas/doc/sebx/data/kaggle_financial_data/subset/kgtriplets_rephrased_subset.csv"
filename = "data/mistral_knowledge_extraction.csv"
df = pd.read_csv(filename, comment="#")
print(df.columns)
arr = df.idx.unique()
res = df.groupby('idx')


def show(i):
    

    result = res.get_group(arr[i])
    return result.iloc[0].input , gr.DataFrame(result[['subject', 'subject_type', 'relation', 'object', 'object_type']])


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(min_width="30%"):
            slider = gr.Slider(0, len(arr)-1, step=1, label="Select a number for the chunk")
        with gr.Column(min_width="70%"):
            text = gr.Textbox()
    with gr.Row():
            table = gr.DataFrame(headers=['subject', 'subject_type', 'relation', 'object', 'object_type'])

        #text = gr.Textbox()
        #table = gr.DataFrame(headers=['subject', 'subject_type', 'relation', 'object', 'object_type'])

    gr.Button("show chunk").click(
            fn=show,
            inputs=slider,
            outputs=[text, table]
        )
    with gr.Row():
        btn = gr.Button("Flag")

demo.launch()

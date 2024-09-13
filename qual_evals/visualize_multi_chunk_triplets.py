"""This script requries a filename for a csv file  with unique indexes for each chunk, and the headers :
```
idx,subject,subject_type,relation,object,object_type,input,wiki_page
```
The `wiki_page` column is not used

"""
import gradio as gr
import pandas as pd

mistral = "qual_evals/data/mistral_knowledge_extraction.csv"
gpt4omini = "qual_evals/data/gpto-mini_knowledge_extraction_kg.csv"
gpt4o = "qual_evals/data/gpto_knowledge_extraction_kg.csv"
triplex = "qual_evals/data/triplex_knowledge_extraction.csv"
filenames = [mistral, gpt4o, gpt4omini, triplex]
dfs = list(pd.read_csv(filename, comment="#") for filename in filenames)
# print(df.columns for df in dfs)
d = list(df.idx.unique() for df in dfs)
arr = list(set.intersection(*map(set,d)))
cols = 'subject,subject_type,relation,object,object_type'.split(',')

def show(i):

    id = arr[i]
    results = []
    for df in dfs:
        # print(len(df))
        s = df.query('idx == @id')
        input = s.iloc[0].input
        results.append(s[cols])
    return [input] + results

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(min_width="30%"):
            slider = gr.Slider(0, len(arr)-1, step=1, label="Select a number for the chunk")
        with gr.Column(min_width="70%"):
            text = gr.Textbox()
    with gr.Row():
    #with gr.Column():
        table1 = gr.DataFrame(headers=['subject', 'subject_type', 'relation', 'object', 'object_type'], label='Mistral')
    #with gr.Column():
    with gr.Row():
        table2 = gr.DataFrame(headers=['subject', 'subject_type', 'relation', 'object', 'object_type'], label='gpt-4o')
    #with gr.Column():
    with gr.Row():
        table3 = gr.DataFrame(headers=['subject', 'subject_type', 'relation', 'object', 'object_type'], label='gpt-4o Mini')

    with gr.Row():
        table4 = gr.DataFrame(headers=['subject', 'subject_type', 'relation', 'object', 'object_type'], label='triplex')

    gr.Button("show chunk").click(
            fn=show,
            inputs=slider,
            outputs=[text, table1, table2, table3, table4]
        )
    with gr.Row():
        btn = gr.Button("Flag")

demo.launch()

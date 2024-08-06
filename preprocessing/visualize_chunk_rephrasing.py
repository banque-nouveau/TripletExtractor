"""In order for this module to work, we will need to run  rephrase_text.ipynb and populate the directory `data/rephrasing` with json files like `wiki_text_Hilary_Clinton.txt_137.json`

This can then be run by 

import gradio as gr
import json

def greet(fname, counter):
    fname = f"data/rephrasing/wiki_text_{fname}.txt_{counter}.json"
    with open(fname, "r") as f:
        data = json.load(f)
    input = data["input"]
    
    if input.startswith('\n') :
        output = data["output"][3:-3]
    else:
        output = data["output"]
    return input, output

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text","text"],
)

demo.launch()

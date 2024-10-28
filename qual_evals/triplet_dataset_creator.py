import pandas as pd
import gradio as gr
import numpy as np

# Load the CSV file into a pandas DataFrame
filename = "qual_evals/data/curated_dataset.csv"
df = pd.read_csv(filename, comment="#")
print(df.columns)

# Get unique indices and group the DataFrame by 'idx'
arr = df.idx.unique()
res = df.groupby('idx')

def show(i, state):
    """
    Display the input text and relevant table based on the selected index.

    Args:
        i (int): The index selected via the slider.
        state: The current state to store the selected 'idx'.

    Returns:
        tuple: Contains the input text, the filtered table, and the updated state.
    """
    current_idx = arr[i]
    state = current_idx
    res = df.groupby('idx')
    result = res.get_group(current_idx)
    input_text = result.iloc[0].input  # Assuming 'input' is the same across the group
    table = result[['subject', 'subject_type', 'relation', 'object', 'object_type']]
    return input_text, table, state


def add_row(i, state):
    print("Add")
    current_idx = arr[i]
    res = df.groupby('idx')
    result = res.get_group(current_idx)
    input_text = result.iloc[0].input
    df.loc[len(df)] = {
        'idx': current_idx,
        'subject_type':[''],
        'subject':[''], 
        'relation':[''], 
        'object_type':[''],
        'object':[''], 
        'input':[input_text],
        'wiki_page': ['']
    }
    res = df.groupby('idx')
    result = res.get_group(current_idx)
    table = result[['subject', 'subject_type', 'relation', 'object', 'object_type']]

    return input_text, table, state


def save_edit(current_idx, edited_input, edited_table):
    """
    Save the edited input and table back to the DataFrame and CSV file.

    Args:
        current_idx: The current 'idx' being edited.
        edited_input (str): The edited input text.
        edited_table (pd.DataFrame): The edited table data.

    Returns:
        str: Confirmation message.
    """
    # Ensure that a valid index is provided
    if current_idx is None:
        return "No chunk selected to save."

    # Update the 'input' column for the selected group
    mask = df['idx'] == current_idx
    df.loc[mask, 'input'] = edited_input

    # Update the other columns based on the edited table
    for col in ['subject', 'subject_type', 'relation', 'object', 'object_type']:
        df.loc[mask, col] = edited_table[col].values

    try:
        # Write the updated DataFrame back to the CSV file
        df.to_csv(filename, index=False)
        return "Changes saved successfully."
    except Exception as e:
        return f"Error saving changes: {e}"
    

# Define the Gradio Blocks interface
with gr.Blocks() as demo:
    # State to keep track of the current 'idx'
    state = gr.State(None)

    # First row: Slider and Textbox
    with gr.Row():
        with gr.Column(min_width="30%"):
            slider = gr.Slider(
                minimum=0, 
                maximum=len(arr)-1, 
                step=1, 
                label="Select a number for the chunk"
            )
        with gr.Column(min_width="70%"):
            text = gr.Textbox(
                label="Input Text",
                lines=2,
                interactive=True  # Make the textbox editable
            )
    
    # Second row: Editable DataFrame
    with gr.Row():
        table = gr.DataFrame(
            headers=['subject', 'subject_type', 'relation', 'object', 'object_type'],
            interactive=True  # Make the DataFrame editable
        )
    
    # Third row: Buttons for showing and saving chunks
    with gr.Row():
        show_button = gr.Button("Show Chunk")
        save_button = gr.Button("Save Changes")
        add_row_button = gr.Button("Add Row")
    
    # Fourth row: Status message
    with gr.Row():
        status = gr.Textbox(
            label="Status",
            interactive=False  # Read-only textbox for status messages
        )
    
    # Connect the "Show Chunk" button to the show function
    show_button.click(
        fn=show,
        inputs=[slider, state],
        outputs=[text, table, state]
    )
    
    # Connect the "Save Changes" button to the save_edit function
    save_button.click(
        fn=save_edit,
        inputs=[state, text, table],
        outputs=status
    )

    add_row_button.click(
        fn=add_row,
        inputs=[slider, state],
        outputs=[text, table, state]
    )
    
    # Optional: Existing "Flag" button (functionality not modified)
    with gr.Row():
        flag_button = gr.Button("Flag")

# Launch the Gradio app
demo.launch()

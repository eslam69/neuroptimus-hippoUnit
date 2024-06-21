import argparse
from modelHandler import modelHandlerNeuron
import json


# Set up argument parsing
parser = argparse.ArgumentParser(description='Run model handler and get parameters.')
parser.add_argument('model_path', type=str, help='Path to the model')
parser.add_argument('model_modFiles_dir', type=str, help='Directory of mod files')
parser.add_argument('model_base_dir', type=str, help='Base directory of the model')
parser.add_argument('output_file1', type=str, help='File to write the parameters to')
parser.add_argument('output_file2', type=str, help='File to write the sections to')

# Parse arguments
args = parser.parse_args()

# Use the arguments to create a model handler instance
model_handler = modelHandlerNeuron(args.model_path, args.model_modFiles_dir, args.model_base_dir)

# Get parameters from the model handler
params = model_handler.GetParameters()

sections=[]
for n in params:
    sections.append(n[0])
sections=list(set(sections))
sections.append("None")

# Write the parameters to the specified output file
# Assuming params is a dictionary, convert it to a JSON string for writing
with open(args.output_file, 'w') as f:
    json.dump(params, f)

#save json file with sections
with open(args.output_file2, 'w') as f:
    json.dump(sections, f)
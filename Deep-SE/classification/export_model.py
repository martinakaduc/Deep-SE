from keras import backend as K
from keras.models import load_model, model_from_json
import tensorflow as tf
from create_model import PoolingSeq
import os
import sys

K.set_learning_phase(0)
custom = {'PoolingSeq': PoolingSeq}

inputs = os.listdir("bestModels")
inputs = list(filter(lambda x: x[-5:] == ".hdf5" and "dim50" in x and sys.argv[1] in x, inputs))
inputs = [x[:-5] for x in inputs]

def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    Freezes the state of a session into a pruned computation graph.

    Creates a new computation graph where variable nodes are replaced by
    constants taking their current value in the session. The new graph will be
    pruned so subgraphs that are not necessary to compute the requested
    outputs are removed.
    @param session The TensorFlow session to be frozen.
    @param keep_var_names A list of variable names that should not be frozen,
    or None to freeze all the variables in the graph.
    @param output_names Names of the relevant graph outputs.
    @param clear_devices Remove the device directives from the graph for better portability.
    @return The frozen graph definition.
    """
    from tensorflow.compat.v1.graph_util import convert_variables_to_constants
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        # Graph -> GraphDef ProtoBuf
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
                frozen_graph = convert_variables_to_constants(session, input_graph_def,
                output_names, freeze_var_names)
                return frozen_graph


for input_model in inputs:
    model = model_from_json(open("./models/" + input_model + ".json").read(), custom_objects=custom)
    model.load_weights("./bestModels/" + input_model + ".hdf5")

    # print(model.inputs)
    # print(model.outputs)

    frozen_graph = freeze_session(K.get_session(),
                                  output_names=[out.op.name for out in model.outputs])

    tf.io.write_graph(frozen_graph, "../inference/bestModelsPb", input_model + ".pb", as_text=False)

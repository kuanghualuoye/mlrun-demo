%%writefile /home/leixiang/new-proj/workflow.py
from kfp import dsl
from mlrun import mount_v3io

funcs = {}

def init_functions(functions: dict, project=None, secrets=None):
    functions['ingest'].apply(mount_v3io())

@dsl.pipeline(
    name='demo project', description='Shows how to use mlrun project.'
)
def kfpipeline(p1=3):
    # first step build the function container
    builder = funcs['tstfunc'].deploy_step(with_mlrun=False)
    
    ingest = funcs['ingest'].as_step(name='load-data', params={'dataset': 'boston'})

    # first step
    s1 = funcs['tstfunc'].as_step(name='step-one', handler='my_func',
         image=builder.outputs['image'],
         params={'p1': p1})

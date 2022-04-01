# %%
import pandas as pd
from io import StringIO
from graphviz import Digraph
from IPython.display import display, HTML

# %% 0*01$ 正则的状态机
dot = Digraph()
dot.attr(rankdir='LR')
# 普通状态
dot.attr('node',shape='circle')
dot.node('q0')
dot.node('q1')
# 终结状态
dot.attr('node',shape='doublecircle')
dot.node('q2')
# 边
dot.edge('q0','q0',label='0')
dot.edge('q0','q1',label='0')
dot.edge('q1','q2',label='1')
dot

# %% pandas表格
st_table_sio = StringIO("""
s,      0,      1
q0,     q0,     q1
q0,     q1,     q1
q1,     ϕ,      q2
""")
df = pd.read_csv(st_table_sio,index_col=None)
display(HTML(df.to_html(index=False)))

#%%
# -*- encoding:utf8 -*-

import pandas as pd
from define import Define

branch_list_df = pd.read_csv(Define.BRANCH_LIST, encoding='big5', index_col=0, header=0)
get_branch_id = lambda branch_name: branch_list_df.loc[branch_list_df['證券商名稱'] == branch_name].index.values[0]


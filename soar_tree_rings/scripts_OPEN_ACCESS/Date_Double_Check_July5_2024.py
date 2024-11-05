import pandas as pd

"""
After seeing the notes that PENE hand-copied from tree core plastic bags, we need to now check all years. For instance, the tree-core database years are different from the plastic bag notes. What about RLIMS dates? 
"""
# here is the dataframe containing the new 14C data from Pene's work, as well as Rachel's old work (the dates here are from Tree Core database)
# this was created in "Tree_Rings_Second_Check.py"
new_df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\dftotal.xlsx')
new_df = new_df[['R number','Ring year','notes from original sample bag ']].rename(columns={'Ring year':'Ring year TreeCore'})
print(len(new_df))

# here is Jocelyn's original tree ring data that she sent me
og_df = pd.read_excel(r'H:\Science\Datasets\SOARTreeRingData2022-02-01.xlsx')  # read in the Tree Ring data.
og_df = og_df[['R number','DecimalDate','Site']].rename(columns={'DecimalDate':'Decimal_date_JCT'})
print(len(og_df))

df = new_df.merge(og_df, on='R number', how='outer', suffixes=('_NEW','_JCT'))

# a recent rlims history downloaded for an MCC correction, but all of RLIMS is in here and I can filter for the data i need
rlims_df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\sample_table.xlsx')
print(rlims_df.columns)
rlims_df = rlims_df.dropna(subset='Collection date')
rlims_df = rlims_df[['R Composed','Collection date','Location','Contaminants']].rename(columns={'R Composed':'R number', 'Collection date': 'CollectionDate_RLIMS'})
print(len(rlims_df))

df = df.merge(rlims_df, on='R number', how='outer')

df.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\datecheck.xlsx')

#
#

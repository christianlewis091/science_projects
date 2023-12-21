"""
Data Quality Paper 1 = adding descriptors and flagging
Data Quality Ppaer 2 = looking at blanks and making plots
Data Quality Paper 3 = calculate residuals of secondary standards and making plots
Data Quality Paper 4 = this one = create a few figures that overlay different secondaries in a PUBLISHABLE figure.
"""
import pandas as pd
import numpy as np
import warnings
import xlsxwriter
from datetime import date
warnings.simplefilter(action='ignore')
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
today = date.today()
from drawing import *
import seaborn as sns
import statsmodels.api as sm

df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/df_with_residuals.csv')

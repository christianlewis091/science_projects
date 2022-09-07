from Pre_Processing_ANSTO import combine_ANSTO
from Pre_Processing_Heidelberg import combine_heidelberg
from Pre_Processing_SIO_LLNL import combine_SIO
from Pre_Processing_UniMagallanes import combine_Magallanes
import pandas as pd

# add the differences sheet
writer = pd.ExcelWriter('Pre_processing_output.xlsx', engine='openpyxl')
combine_ANSTO.to_excel(writer, sheet_name='ANSTO')
combine_heidelberg.to_excel(writer, sheet_name='Heidelberg')
combine_SIO.to_excel(writer, sheet_name='SIO')
combine_Magallanes.to_excel(writer, sheet_name='Magallanes')
writer.save()

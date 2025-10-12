'''
PieChart_test.py
Author  Niall Naughton
Date    12/10/2025
----------------------------------------------------------------------------------
Description:     
Testing code for notebook called assignment03-pie.ipynb
----------------------------------------------------------------------------------
'''


# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Creating dataset
data_url = 'https://drive.google.com/uc?id=1AWPf-pJodJKeHsARQK_RHiNsE8fjPCVK&export=download'
df = pd.read_csv(data_url)
df['Domain'] = df['Email'].str.split('@').str[1]
domain_counts = df['Domain'].value_counts()

# Creating explode data
explode = (0.2, 0.0, 0.0)

# Wedge properties
wp = {'linewidth': 1, 'edgecolor': "white"}

# Creating autocpt arguments


def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d} g)".format(pct, absolute)


# Creating plot
fig, ax = plt.subplots(figsize=(10, 7))
wedges, texts, autotexts = ax.pie(domain_counts,
                                  autopct='%1.1f%%',
                                  explode=explode,
                                  labels=domain_counts.index,
                                  shadow=True,
                                  startangle=90,
                                  wedgeprops=wp,
                                  textprops=dict(color="magenta"))

# Adding legend
ax.legend(wedges, domain_counts.index,
          title="Domains",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")
ax.set_title("Test Pie Chart")

# show plot
plt.show()
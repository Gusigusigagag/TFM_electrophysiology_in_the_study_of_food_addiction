import pandas as pd
import statsmodels.api as sm
from statsmodels.multivariate.manova import MANOVA

data = '/home/neurophar/Downloads/PFC1.csv'
df = pd.read_csv(data, sep=',')
print(df)

dependent_vars = ['delta', 'ntheta', 'wtheta', 'beta', 'lgamma', 'hgamma', 'fgamma', 'hfo']
manova_data = df[dependent_vars + ['Type']]  #
manova_formula = ' + '.join(dependent_vars) + ' ~ Type'
manova = MANOVA.from_formula(formula=manova_formula, data=manova_data)
print(manova.mv_test())
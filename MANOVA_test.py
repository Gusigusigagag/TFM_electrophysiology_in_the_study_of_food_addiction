import pandas as pd
import statsmodels.api as sm
from statsmodels.multivariate.manova import MANOVA
from statsmodels.formula.api import ols



data = '/home/neurophar/Downloads/HPC1.csv'
df = pd.read_csv(data, sep=',')
print(df)

# MANOVA
dependent_vars = ['delta', 'ntheta', 'wtheta', 'beta', 'lgamma', 'hgamma', 'fgamma', 'hfo']
manova_data = df[dependent_vars + ['Type']]  #
manova_formula = ' + '.join(dependent_vars) + ' ~ Type'
manova = MANOVA.from_formula(formula=manova_formula, data=manova_data)
print(manova.mv_test())

# One way ANOVA
for var in dependent_vars:
    formula = var + ' ~ Type'
    model = ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(f"ANOVA for {var}")
    print(anova_table)
    print()
import pandas as pd

data = [
    {
        "manager": "Vasiliy",
        "sales": 2
    },
    {
        "manager": "Vasiliy",
        "sales": 3
    },
    {
        "manager": "Vasiliy",
        "sales": 4
    },
]

df = pd.DataFrame(data)
df.pivot_table(columns=["manager"], aggfunc=["sum", "count"])

import urllib3
import pandas as pd
from pandas import Series,DataFrame
#統計モデルの推定
import statsmodels.api as sm 
import matplotlib.pyplot as plt
import seaborn as sns

file_name = r'\temp\csv\japan.csv'
csvurl ="https://www.mhlw.go.jp/content/pcr_positive_daily.csv"
req_methods = urllib3.PoolManager()

#URLから最新の陽性者データをダウンロードし保存
res = req_methods.request("GET",csvurl)
with open(file_name,'wb') as f:
    f.write(res.data)

sns.set_style("whitegrid")

#csvファイルの読み込み
corona_df = pd.read_csv(file_name)
#SARIMAモデルを使う(季節自己回帰和分移動平均モデル)
corona_amount = corona_df["PCR 検査陽性者数(単日)"].astype(float)
coronamax = sm.tsa.SARIMAX(corona_amount, order=(2,1,3),
                          seasonal_order=(0,2,2,12),
                          enforce_stationarity=False,
                          enforce_invertibility=False).fit()

#今後の30日間予想する
prediction = coronamax.forecast(30)
#グラフを描写
plt.figure(figsize=(10,5))
#corona_amountをプロット
plt.plot(corona_amount, marker="o", label="actual transition")
#predictionをプロット
plt.plot(prediction, label="change in forecast", marker="x", linestyle="--")
#凡例を最適な場所に表示
plt.legend(loc="best")
plt.show()

import pandas as pd # type: ignore
import matplotlib
# RuntimeError: main thread is not in main loop 오류 관련
# 이 오류는 웹 애플리케이션과 같이 GUI가 없는 환경에서 matplotlib이 GUI를 생성하려고 할 때 발생합니다. matplotlib은 기본적으로 화면에 그래프를 표시하는 대화형 백엔드를 사용하도록 설정되어 있을 수 있습니다.
# 이 문제를 해결하려면 matplotlib이 GUI가 아닌 파일로 이미지를 렌더링하는 'Agg' 백엔드를 사용하도록 명시적으로 설정해야 합니다.
matplotlib.use('Agg')
import matplotlib.pyplot as plt # type: ignore
from ...extensions import db
from ...models.sar_traffic import SarTraffic
import os
from sqlalchemy import or_, and_, cast, String # type: ignore

def get_traffic_data(query=None):
    # SQLAlchemy ORM → Pandas DataFrame
    if query is None:
        query_result = db.session.query(SarTraffic).all()
    else:
        query_result = query.all()

    data = [{
        'datetime': row.date_time,  # This was 'date_time'
        'rx_kbps': row.rxkB_per_second * 8,
        'tx_kbps': row.txkB_per_second * 8,
    } for row in query_result]
    return pd.DataFrame(data)    

def plot_traffic_over_time(df, output_path, hostname, ip_address):
    plt.figure(figsize=(10, 6))
    # - y축에 여러 값을 넣는다는 건 plt.plot()을 여러 번 호출하면 됩니다.

    plt.plot(df['datetime'], df['rx_kbps'], label='rx kbps')
    plt.plot(df['datetime'], df['tx_kbps'], label='tx kbps')

    plt.title(f'Traffic : {hostname} ({ip_address})')
    plt.xlabel('Date')
    plt.ylabel('Traffic (kbps)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
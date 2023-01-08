import os
import json
import pandas as pd
import ast
from request_APIs import call_sepehr, call_login_token, call_input_setting_db
import json
from datetime import datetime as dt
import datetime


def main():
    # start token and expiration date handling
    if 'token_expire_date.txt' in os.listdir():
        with open('token_expire_date.txt', 'r') as f:
            te = f.read()
        expire_date = te.split('token:')[0]
        token = te.split('token:')[1]
        if dt.now() >= dt.strptime(expire_date, '%Y-%m-%d'):
            token, expire_date = call_login_token()
            expire_date = expire_date.split('T')[0]
            with open('token_expire_date.txt', 'w') as f:
                f.write(expire_date + 'token:' + token)
    else:
        token, expire_date = call_login_token()
        expire_date = expire_date.split('T')[0]
        with open('token_expire_date.txt', 'w') as f:
            f.write(expire_date + 'token:' + token)
    # end token and expiration date handling

    data = call_input_setting_db(token)

    # start controlling df_routes for handling start process time
    if 'routes_start_time.csv' in os.listdir():
        df_routes = pd.read_csv('routes_start_time.csv')
        df_routes['route'] = df_routes['route'].map(lambda x: ast.literal_eval(x))
        df_routes['start_process_time'] = pd.to_datetime(df_routes['start_process_time'])
    else:
        df_routes = pd.DataFrame({
            'route': json.loads(data.text)['getAllRouteMonitoringResponseItemViewModels'],
            'start_process_time': [dt.now() - datetime.timedelta(1)] * len(
                json.loads(data.text)['getAllRouteMonitoringResponseItemViewModels'])
        })
    # end
    for index, row in df_routes.iterrows():
        if ((dt.now() - row[1]).total_seconds() / 60) >= row[0]['interval']:
            result = call_sepehr(json.dumps(row[0]))
            if result:
                df_routes.loc[index, 'start_process_time'] = dt.now()
                df_routes.to_csv('routes_start_time.csv',index=False)
            # TODO: API post method should be used here to post the results to the DB2
            else:
                # TODO: here we should add logging.
                continue
        else:
            continue


if __name__ == '__main__':
    main()

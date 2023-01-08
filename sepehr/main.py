import os
import pandas as pd
import ast
import json
from datetime import datetime as dt
import datetime
from request_APIs import call_sepehr, call_login_token, call_input_setting_db


def main():
    # region token and expiration date handling
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
    # endregion

    # region API request for input setting
    data = call_input_setting_db(token)
    # endregion

    # region controlling df_routes for handling start process time
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
    # endregion

    for index, row in df_routes.iterrows():
        if ((dt.now() - row[1]).total_seconds() / 60) >= row[0]['interval']:
            result = call_sepehr(json.dumps(row[0]))
            # TODO: API post method should be used here to post the results to the DB2
            if result:
                df_routes.loc[index, 'start_process_time'] = dt.now()
                df_routes.to_csv('routes_start_time.csv', index=False)
            # TODO: here we should add logging for both error state and without error.
        else:
            continue


if __name__ == '__main__':
    main()

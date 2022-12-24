


def json_parser(data):
    flight_no = data['page1']['flight_no']
    adep = data['page1']['ADEP']
    ades = data['page1']['ADES']
    std = data['page1']['STD']
    sta = data['page1']['STA']
    tail_id = data['page1']['Tail_id']
    metar = data['page2']['METAR']
    runway = data['page2']['Runway']
    flaps = data['page2']['Flaps']
    antiice = data['page2']['AntiIce']
    packs = data['page2']['Packs']
    improved = data['page2']['Improved']
import csv
import json
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Candle

def upload_csv(request):
    if request.method == 'POST':
        # Process CSV file and return JSON response
        csvfile = request.FILES['file']
        timeframe = int(request.POST.get('timeframe', 1))

        candles = process_csv(csvfile)
        candles = convert_timeframe(candles, timeframe)
        json_filename = save_to_json(candles)

        return JsonResponse({'success': True, 'download_link': json_filename})
    else:
        # Render the HTML form for GET requests
        return render(request, 'MainApp/upload_form.html')

def process_csv(file):
    candles = []
    reader = csv.DictReader(file.read().decode('utf-8').splitlines())
    
    for row in reader:
        candle = Candle(
            open=float(row['OPEN']),
            high=float(row['HIGH']),
            low=float(row['LOW']),
            close=float(row['CLOSE']),
            date=datetime.strptime(row['DATE'] + ' ' + row['TIME'], '%Y%m%d %H:%M')
        )
        candles.append(candle)
    
    return candles

def convert_timeframe(candles, timeframe):
    new_candles = []
    current_time = candles[0].date
    current_candle = candles[0]

    for candle in candles:
        if candle.date < current_time + timedelta(minutes=timeframe):
            current_candle.high = max(current_candle.high, candle.high)
            current_candle.low = min(current_candle.low, candle.low)
            current_candle.close = candle.close
        else:
            new_candles.append(current_candle)
            current_time += timedelta(minutes=timeframe)
            while candle.date >= current_time + timedelta(minutes=timeframe):
                current_time += timedelta(minutes=timeframe)
            current_candle = Candle(
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                date=current_time
            )

    return new_candles

def save_to_json(candles):
    json_data = [{'date': candle.date.strftime('%Y-%m-%d %H:%M:%S'),
                  'open': candle.open,
                  'high': candle.high,
                  'low': candle.low,
                  'close': candle.close} for candle in candles]

    json_filename = 'output_data.json'
    with open(json_filename, 'w') as json_file:
        json.dump(json_data, json_file)

    return json_filename
"""Simulated sensor script.
Usage:
python sensor_simulator.py --backend http://localhost:8000/api/push-data --rate 2
"""
import time, random, argparse, json, requests

def gen_item_id(i=0):
    return f"PKG-{1000 + i}"

def generate_reading(i=0):
    return {
        "item_id": gen_item_id(i),
        "temperature": round(random.uniform(2, 38), 2),
        "humidity": round(random.uniform(20, 90), 2),
        "lat": round(17.45 + random.uniform(-0.05, 0.05), 6),
        "lng": round(78.36 + random.uniform(-0.05, 0.05), 6),
        "shock": round(random.uniform(0, 3), 2),
        "timestamp": time.time()
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--backend', default='http://localhost:8000/api/push-data')
    parser.add_argument('--rate', type=float, default=2.0, help='seconds between readings')
    parser.add_argument('--count', type=int, default=0, help='0=run forever, else number of readings')
    args = parser.parse_args()
    i = 0
    try:
        while True:
            payload = generate_reading(i)
            try:
                resp = requests.post(args.backend, json=payload, timeout=5)
                print('sent', payload['item_id'], 'status', resp.status_code, resp.text)
            except Exception as e:
                print('failed to send:', e)
            i += 1
            if args.count and i >= args.count:
                break
            time.sleep(args.rate)
    except KeyboardInterrupt:
        print('stopped')

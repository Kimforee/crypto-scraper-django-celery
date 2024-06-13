import os
import csv
import logging
from celery import shared_task
from .coinmarketcap import CoinMarketCap
from .models import Task

logger = logging.getLogger(__name__)
print("finally here before starting inside task method/////////////////////////////////////////////////////")
from celery import shared_task

# @shared_task
# def test_task():
#     print("Test task executed////////////////////////////////////////////////////////////////")
#     return "Test task executed"

@shared_task
def my_task(arg1, arg2):
    print("hello from my task ////////////////////////////////////")
    result = arg1 + arg2
    return result

@shared_task(bind=True)
def scrape_coin_data(self, task_id):
    print("Here 1: Task started with ID", task_id)
    logger.info(f"Starting task for ID {task_id}")
    try:
        task = Task.objects.get(id=task_id)
        print("Here 2: Task found", task)
        logger.info(f"Task found: {task}")
        coin_scraper = CoinMarketCap(task.coin)
        print("Here 3: CoinMarketCap initialized for", task.coin)
        data = coin_scraper.scrape()
        print("Here 4: Data scraped", data)
        task.output = data
        task.status = 'completed'
        save_to_csv(task.coin, data)
        print("Here 5: Task completed for coin", task.coin)
        logger.info(f"Completed task for coin {task.coin}: {data}")
    except Exception as e:
        task.status = 'failed'
        task.output = {"error": str(e)}
        print("Here 6: Task failed for coin", task.coin, "with error", str(e))
        logger.error(f"Failed task for coin {task.coin}: {str(e)}")
    finally:
        task.save()
        print("Here 7: Task saved")

def save_to_csv(coin, data):
    print("Here 8: Saving data to CSV for coin", coin)
    try:
        # Save the file to the user's home directory
        directory = os.path.expanduser('~')  # User's home directory
        file_path = os.path.join(directory, 'output.csv')
        file_exists = os.path.isfile(file_path)
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow([
                    'Coin', 'Market Cap', 'Volume (24h)', 'Circulating Supply',
                    'Total Supply', 'Fully Diluted Market Cap', 'Official Links',
                    'Socials', 'Network Information', 'UCID'
                ])
            writer.writerow([
                coin,
                data.get('market_cap', ''),
                data.get('volume_24h', ''),
                data.get('circulating_supply', ''),
                data.get('total_supply', ''),
                data.get('fully_diluted_market_cap', ''),
                ', '.join(link['url'] for link in data.get('official_links', [])),
                ', '.join(social['url'] for social in data.get('socials', [])),
                data.get('network_information', ''),
                data.get('ucid', '')
            ])
        print(f"Here 9: Data saved to CSV at {file_path}")
    except Exception as e:
        print(f"Failed to save data to CSV: {e}")
        logger.error(f"Failed to save data to CSV: {e}")
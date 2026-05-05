import subprocess, logging, time, os
from datetime import datetime

os.makedirs("logs", exist_ok=True)
log_file = f"logs/pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
)
log = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 10

STEPS = [
    ("Scraping",  ["python3", "extract/scraper.py"]),
    ("Cleaning",  ["python3", "clean/cleaner.py"]),
    ("Warehouse", ["python3", "warehouse/load_to_warehouse.py"]),
]

def run_step(name, cmd):
    for attempt in range(1, MAX_RETRIES + 1):
        log.info(f" [{name}] Tentative {attempt}/{MAX_RETRIES}")
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if r.stdout: log.info(f"[{name}]\n{r.stdout.strip()}")
            if r.returncode == 0:
                log.info(f" [{name}] Succès")
                return True
            log.error(f" [{name}] Échec (code {r.returncode})\n{r.stderr.strip()}")
        except subprocess.TimeoutExpired:
            log.error(f" [{name}] Timeout")
        except Exception as e:
            log.error(f" [{name}] {e}")

        if attempt < MAX_RETRIES:
            log.info(f" Retry dans {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

    log.critical(f" [{name}] Échec définitif. Pipeline arrêté.")
    return False

def main():
    log.info("=" * 50)
    log.info(" Pipeline Avito démarré")
    log.info("=" * 50)
    start = time.time()

    for name, cmd in STEPS:
        if not run_step(name, cmd):
            exit(1)

    log.info(f" Pipeline terminé en {round(time.time()-start, 2)}s")
    log.info(f" Log: {log_file}")

if __name__ == "__main__":
    main()
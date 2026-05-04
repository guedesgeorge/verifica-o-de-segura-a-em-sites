"""Entry point do bot."""
import logging
import sys

from apscheduler.schedulers.blocking import BlockingScheduler

from core.orchestrator import Orquestrador
from config.settings import SCRAPE_INTERVAL_MINUTES


def configurar_logs():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("bot.log", encoding="utf-8"),
        ],
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)


def main():
    configurar_logs()
    logger = logging.getLogger("main")
    orq = Orquestrador()

    if "--once" in sys.argv:
        logger.info("Modo --once")
        orq.executar_ciclo()
        return

    logger.info(f"Bot iniciado. Intervalo: {SCRAPE_INTERVAL_MINUTES} min")
    try:
        orq.executar_ciclo()
    except Exception as e:
        logger.exception(f"Erro ciclo inicial: {e}")

    scheduler = BlockingScheduler(timezone="America/Campo_Grande")
    scheduler.add_job(orq.executar_ciclo, "interval",
                      minutes=SCRAPE_INTERVAL_MINUTES,
                      max_instances=1, coalesce=True)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Encerrado")


if __name__ == "__main__":
    main()

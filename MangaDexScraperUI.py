import json
from pathlib import Path
import logging
import os

os.environ["MANGADEXDL_CONFIG_ENABLED"] = "1"
from mangadex_downloader.config import config
from mangadex_downloader.main import download  # , download_chapter, download_list


def read_json(filename):
    file_path = Path(filename)
    if file_path.exists():
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    else:
        return []


# noinspection PyBroadException
def write_json(filename, data):
    try:
        file_path = Path(filename)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except:
        return False


def choose_series(data):
    series_name = input("Enter the series name: ")
    for item in data:
        if item.get("series-name").lower() == series_name.lower():
            return item
    return None


def prompt_series_details():
    prompts = {
        "series-name": "Enter series name: ",
        "series-url": "Enter series URL: ",
        "series-start": "Where should it start? : ",
        "series-end": "Where should it end? : ",
        "series-release": "Any specific release group?: ",
    }

    details = {}
    for key, message in prompts.items():
        details[key] = input(message)
    return details


def download_series(series_data):
    logging.info("hit")
    print(series_data)

    config.save_as = "pdf"
    config.language = "en"
    mangapath = Path(__file__).parent / "Outputs" / str(series_data.get("series-name"))
    mangapath.mkdir(parents=True, exist_ok=True)
    config.path = str(mangapath)

    args = {
        "manga_id": series_data.get("series-url"),
    }

    if series_data.get("series-current"):
        args["start_chapter"] = float(series_data.get("series-current"))
    else:
        args["start_chapter"] = float(series_data.get("series-start"))

    if series_data.get("series-end"):
        args["end_chapter"] = float(series_data.get("series-end"))

    if series_data.get("series-release"):
        args["groups"] = series_data.get("series-release")

    download(**args)


def main():
    filename = "data.json"
    data = read_json(filename)

    series_data = choose_series(data)

    if isinstance(series_data, dict):
        # logging.info("Series found! Here are the details:")
        # logging.info(series_data)
        logging.info("Series found. Moving to acquisition.")

        print("Series Found!")
        download_series(series_data)

    else:
        logging.info("Series Unknown. Adding to repository.")
        print("Unknown Series! Let's add it to memory!")
        series_details = prompt_series_details()
        data.append(series_details)
        status = write_json(filename, data)

        if status:
            logging.info("Data saved successfully.")
            print("Data saved successfully!")
        else:
            logging.info("Unable to save file.")
            print(
                "File was unable to be saved. Is the file open, have the appropriate permissions, or does your drive "
                "have enough space?"
            )


if __name__ == "__main__":
    main()

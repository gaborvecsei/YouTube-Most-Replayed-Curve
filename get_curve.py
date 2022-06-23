import aggdraw
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MostReplayedCurve:

    def __init__(self, chrome_driver_path: str) -> None:
        self._driver = self._setup_driver(chrome_driver_path)

    @staticmethod
    def _setup_driver(chrome_driver_path: str = "chromedriver"):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
        return driver

    def _get_heatmap_path_string(self, wait_time_in_secs: int = 10) -> str:
        element_locator = EC.presence_of_element_located((By.CLASS_NAME, "ytp-heat-map-path"))
        yt_heatmap_element = WebDriverWait(self._driver, wait_time_in_secs).until(element_locator)
        return yt_heatmap_element.get_attribute("d")

    def _path_string_to_value(self, heatmap_path_str: str) -> np.ndarray:
        symbol = aggdraw.Symbol(heatmap_path_str)
        # Flattened list of (x, y) coordinates
        c = symbol.coords()
        # Separation of x, y coordinates
        x = c[::2]
        y = np.array(c[1:][::2])
        # As the path start from (0, 100) (defined by the "M" character at the pathstring)
        y = 100 - y
        return np.stack((x, y)).T

    def get_curve(self, youtube_url: str, wait_time_in_secs: int) -> np.ndarray:
        self._driver.get(youtube_url)
        path_string = self._get_heatmap_path_string(wait_time_in_secs=wait_time_in_secs)
        curve = self._path_string_to_value(path_string)
        return curve

    def close(self):
        self._driver.close()

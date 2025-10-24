import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

from river_flows.data.exceptions import UnableToFindONITableException


class ONIScraper:
    def __init__(self):
        self.oni_url = "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php"

    def scrape_oni_data(self) -> pd.DataFrame:
        """
        Scrapes the ONI data from the given NOAA website by specifically targeting
        the data table using BeautifulSoup and then parsing with pandas.
        """
        try:
            response = requests.get(self.oni_url)
            response.raise_for_status()
            html_content = response.text

            soup = BeautifulSoup(html_content, "lxml")

            target_table_html = None
            tables_on_page = soup.find_all("table")

            for i, table in enumerate(tables_on_page):
                table_str = str(table)
                try:
                    temp_dfs = pd.read_html(StringIO(table_str), header=None)
                    if not temp_dfs:
                        continue

                    temp_df = temp_dfs[0]

                    if not temp_df.empty and len(temp_df.columns) == 13:
                        first_cell_content = str(temp_df.iloc[0, 0]).strip()
                        if first_cell_content == "Year":
                            target_table_html = table_str
                            break

                except Exception:
                    print(f"Encountered exception while parsing ONI HTML table: {e}")
                    continue

            if target_table_html is None:
                print("Could not find the specific ONI data table based on 'Year' header and column count.")
                raise UnableToFindONITableException()

            oni_df = pd.read_html(StringIO(target_table_html), header=0)[0]

            oni_df = oni_df.dropna(how="all")
            oni_df = oni_df.dropna(axis=1, how="all")

            if "Year" in oni_df.columns:
                oni_df["Year"] = pd.to_numeric(oni_df["Year"], errors="coerce")
                oni_df = oni_df.dropna(subset=["Year"])
                oni_df["Year"] = oni_df["Year"].astype(int)

            for col in oni_df.columns:
                if col != "Year":
                    oni_df[col] = pd.to_numeric(oni_df[col], errors="coerce")

            oni_df.columns = [col.lower() for col in oni_df.columns]
            oni_df = oni_df.replace({np.nan: None})

            return oni_df

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred during scraping: {e}")
            raise

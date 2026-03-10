'''First file to touch it after user inputs ticker or coin and dates'''


import pandas as pd

from services.data_fetcher import DataFetcher
from data_pipeline.data_cleaner import DataCleaner
from indicators.feature_builder import FeatureBuilder


class MarketDataService:
    """
    Orchestrates market data preparation:
    fetch → clean → add indicators
    """

    def __init__(self):
        self.fetcher = DataFetcher()

    def get_features(self, ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        # 1. FETCH RAW DATA (DIRTY)
        raw_df = self.fetcher.fetch(ticker, start_date=start_date, end_date=end_date)

        # 2. CLEAN DATA (THIS IS WHERE CLEANING HAPPENS)
        clean_df = DataCleaner(raw_df).clean()

        # 3. ADD INDICATORS
        features_df = FeatureBuilder(clean_df).build()

        return features_df

# '''First file to touch it after user inputs ticker or coin and dates'''


# import pandas as pd

# from services.data_fetcher import DataFetcher
# from data_pipeline.data_cleaner import DataCleaner
# from indicators.feature_builder import FeatureBuilder


# class MarketDataService:
#     """
#     Orchestrates market data preparation:
#     fetch → clean → add indicators
#     """

#     def __init__(self):
#         self.fetcher = DataFetcher()

#     def get_features(self, ticker: str) -> pd.DataFrame:
#         # 1. FETCH RAW DATA (DIRTY)
#         raw_df = self.fetcher.fetch(ticker)

#         # 2. CLEAN DATA (THIS IS WHERE CLEANING HAPPENS)
#         clean_df = DataCleaner(raw_df).clean()

#         # 3. ADD INDICATORS
#         features_df = FeatureBuilder(clean_df).build()

#         return features_df




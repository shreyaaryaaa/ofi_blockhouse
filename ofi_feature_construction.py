import pandas as pd
import argparse

def compute_best_level_ofi(df):
    bid_sz = df['bid_sz_00']
    ask_sz = df['ask_sz_00']
    ofi = bid_sz.diff() - ask_sz.diff()
    return ofi.rename("best_level_ofi")

def compute_multi_level_ofi(df, levels=10):
    bid_sum = sum(df[f'bid_sz_0{i}'] for i in range(levels))
    ask_sum = sum(df[f'ask_sz_0{i}'] for i in range(levels))
    ofi = bid_sum.diff() - ask_sum.diff()
    return ofi.rename("multi_level_ofi")

def compute_integrated_ofi(df, levels=10):
    ofi = 0
    for i in range(levels):
        weight = 1 / (i + 1)
        bid_diff = df[f'bid_sz_0{i}'].diff()
        ask_diff = df[f'ask_sz_0{i}'].diff()
        ofi += weight * (bid_diff - ask_diff)
    return ofi.rename("integrated_ofi")

def construct_ofi_features(file_path, test=False):
    df = pd.read_csv(file_path)
    if test:
        df = df.head(100)

    features = pd.DataFrame()
    features['ts_event'] = df['ts_event']
    features['symbol'] = df['symbol']
    features = pd.concat([
        features,
        compute_best_level_ofi(df),
        compute_multi_level_ofi(df),
        compute_integrated_ofi(df)
    ], axis=1)

    return features

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="first_25000_rows.csv", help="Path to input CSV")
    parser.add_argument("--test", action="store_true", help="Run on first 100 rows only")
    args = parser.parse_args()
    result = construct_ofi_features(args.file, test=args.test)
    result.to_csv("ofi_features_output.csv", index=False)
    print("Done.")

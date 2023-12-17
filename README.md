# Tokemak Quant Project

The goal of this project is analyze Curve & Maverick LST pool (Mode-Both on MAV) using on-chain data.

1. Identify various sources of return for an LP
2. Analyze 30 & 90 day return for an LP
3. Recommend which pool is expected to have the best risk-adjusted return for a relatively passive investment strategy

The pools are:

- Curve pool stETH/ETH: 0x06325440D014e39736583c165C2963BA99fAf14E
  - 0xDC24316b9AE028F1497c275EB9192a3Ea0f67022
- MAV pool swETH/ETH: 0x0CE176E1b11A8f88a4Ba2535De80E81F88592bad

## Project Requirements

- use primarily on-chain data. Show code on how the data was pulled and analyzed
- 1-2 pager explaining your thoughts, observation & conclusion

## Example Metrics (Non-Exhaustive)

1. historical total return
2. historical fee return
3. historical volume/turnover/TVL/etc
4. token price volatility

## Project Setup

### Web3 Provider

The project requires an eth node provider for data collection. A public Alchemy URL is in the `example.py` file, but is likely to be rate limited. We recommend getting your own key and adding it to the .env file as `PROVIDER_URL`.

### Dependency Management

The project uses [Poetry](https://python-poetry.org/) as its dependency manager. Below are the steps to get started:

1. install [Poetry](https://python-poetry.org/docs/#installation)
2. run `poetry install` in the root of the project
3. run `poetry run example` (it may be rate limited if you did not add a PROVIDER_URL)

# Result

1. Summary
   This analysis project is not completed. I spent a bit too much time and feeling that I might be going on a wrong direction. Thus decided to stop here and wrap it up. One major issue was that I don't fully understand how the Maverick pool works. On their Github there's only interface but no implementation and the contract is not verified on etherscan as well. I read the whitepaper and analyze it with my understanding.
2. Assumption and Methodology
   My ideas is to find exchange rate of how much underlying asset a LP token can redeem. And how the exchange rate change over time, to decide the return of the investment. i.e. In the beginning I deploy certain capital and get x amount of LP token. Across the time frame I check how much underlying capital I can redeem. The yield of the liquid staking token is intrinsically considered into the reserve. The analysis didn't include additional reward in CRV on Curve, or some boosted reward from Maverick.

   1. Curve
      1. For Curve is straight forward, as the LP token is fungible for the entire pool. So I took the reserve and total_supply snapshot for each day, and use 2 reserve values devided by total supply of the LP token. (convert to ETH using the ratio in the Curve pool.)
   2. Maverick
      1. In Mode-Both, when the price move around, the bin will be moved following the price change. And most of the time the bin would be merged into 1. And the LP token for different mode is separated as well (`kind` varibale in the smart contract). So I took the daily snapshot of the Mode-Both bin, read the reserves and total_supply of the bin, to decide the value of the LP token. (convert to ETH using the price in that Maverick pool)

3. Data collection
   The python scripts queries on-chain states, process csv files and output data to csv files.

   1. Utils
      1. `getBlockNumbers.py`: get the block number of the past 90 days at UTC 00:00:00 for snapshot capture.
   2. Curve
      1. `getCurveReserveDaily.py`: get the daily snapshot for the reserve and total supply.
      2. `calculateCurveLpValue.py`: use the daily snapshot to calculate the LP value. 2 reserves devided by total_supply. and convert the fees into ETH.
      3. `getTradeLogsFromCurve.py`: capture the `TokenExchange` event emitted in the pool contract for swapping events. Used to calcualte fee and volume.
      4. `calculateCurveFeePerSwap.py`: process the trade logs and calculate the fee of each swap.
      5. `aggregateCurveDailyFee.py`: aggregate the fee into daily summed value.
      6. `getCurveReserve.py`: not used in the end. The script was used to query the on-chain state of all the blocks that swap happen. My original plan was to replay that whole swapping history to analyze the activity.
   3. Mavrick
      1. `getMavrickReserveDaily.py`: at the daily snapshot block number, use the `PoolInformation` contract to get the active bins, filter out the mode-both bin, and read its reserve and total_supply.
      2. `calculateMavLpValue.py`: use the daily snapshot to calculate the LP value. In Mavevick mode-both it's easy to be single-sided reserve. So I converted all to ETH.
      3. `getTradeLogsFromMavrick.py`: capture the `Swap` event emitted in the pool contract for swapping events. Used to calcualte fee and volume. (not done)
      4. `getMavrickReserve.py`: not used in the end. The script was used to query the on-chain state of all the blocks that swap happen. My original plan was to replay that whole swapping history to analyze the activity.

4. Output
   The result of Maverick doesn't make much sense. Could be my understanding of Maverick pool is wrong. Or I made some mistake during the analysis. Result generated by `lpValueOutput.py`

   Historical return 30 days (`normalized_lp_values_last_30_days.csv`)
   Curve return: 0.79%
   Mavrick return: -0.32%
   (image)
   Historical return 90 days (`normalized_lp_values_last_90_days.csv`)
   Curve return: 0.76%
   Mavrick return: -2.4%
   (image)

5. Not completed plan
   1. Curve
      1. The swapping fee for Curve is at `aggregated_curve_fees_daily.csv` (output by `aggregateCurveDailyFee.py`)
      2. The volume for Curve is at `curve_daily_volume.csv` (output by `volumeCurve.py`)
      3. The reserve snapshot can be used to generate TVL time-series data, and volume / TVL to get the turnover
   2. Maverick
      1. The swapping fee and volume for Maverick is not analyzed. This would be very complicated as the fee needs to be spilt among all the active bins that involves other modes (mode-static, mode-left, mode-right)
      2. The reserve daily snapshot can be used as TVL data and use volume / TVL to derive turnover
      3. The turnover for Maverick should be much higher than Curve

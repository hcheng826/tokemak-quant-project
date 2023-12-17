# Tokemak Quant Project

The goal of this project is analyze Curve & Maverick LST pool (Mode-Both on MAV) using on-chain data.

  1. Identify various sources of return for an LP
  2. Analyze 30 & 90 day return for an LP
  3. Recommend which pool is expected to have the best risk-adjusted return for a relatively passive investment strategy

The pools are:

  * Curve pool stETH/ETH: 0x06325440D014e39736583c165C2963BA99fAf14E
    * 0xDC24316b9AE028F1497c275EB9192a3Ea0f67022
  * MAV pool swETH/ETH: 0x0CE176E1b11A8f88a4Ba2535De80E81F88592bad

## Project Requirements
* use primarily on-chain data. Show code on how the data was pulled and analyzed
* 1-2 pager explaining your thoughts, observation & conclusion

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


Rewards

MAV
1. index all the swap
2. for each swap find out the active bin and reserve for the bin

3. historical total return
   1. Curve: LP value by day, get reserves, total_supply
   2. Mav: LP value by day
4. historical fee return
   1. Curve: fee value by day
5. historical volume/turnover/TVL/etc
   1. volume by day
   2. TVL by day
6. token price volatility
   1. price curve of ETH, stETH, swETH

generate a csv file
output
id,date,balance_0,balance_1,total_supply

1. read from blockNumbers.csv to get the block number to query
2. at eath blocknumber, use the contract info to get the data


100 ETH on day 0

Curve
price ratio, porportionally deposit
use reserve to compute fee each time

Mavrick
price ratio, porportionally deposit
use reserve to compute fee each time


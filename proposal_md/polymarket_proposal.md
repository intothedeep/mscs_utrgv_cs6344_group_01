# When Polymarket Says 70%, Does It Happen 70% of the Time?

## Prediction Accuracy, Trading Concentration, and Statistical Distributions in Prediction Markets

Team Brier | Group 1
Members: Taek Lim, Zhugang Liu (Tony), Francisco Cortez

## Project Description

Prediction markets like Polymarket allow people to trade contracts based on the outcomes of future events. For example, if a contract pays $1 when an event occurs and its market price is $0.70, the price is commonly interpreted as a 70% implied probability. But does a 70% prediction actually happen about 70% of the time? And how is trading activity distributed among participants?

Using the Polymarket-v1 dataset, we will investigate three questions: (1) How accurately do market prices reflect actual event outcomes? (2) Is trading volume concentrated among a small percentage of wallets? (3) What statistical patterns characterize transaction amounts, trading frequency, and market prices?

## Dataset and Methods

The Polymarket-v1 dataset contains historical trade records, including transaction prices, amounts, timestamps, wallet addresses, and market information. We will use Python and statistical methods rather than machine learning to analyze the data.

## Our analysis will follow this structure:

Research question	Statistical methods
Are market-implied probabilities accurate?	Calibration curves, Brier score, log loss
Do a small number of wallets dominate trading volume?	Pareto analysis, Lorenz curve, Gini coefficient
What do trading and price distributions look like?	Histograms, ECDFs, quantiles, skewness

## Objective

Our goal is to understand how reliable Polymarket’s predictions are and what trading patterns emerge from the market data. By combining probability calibration, wallet-level trading concentration, and distribution analysis, we hope to identify meaningful statistical patterns in prediction markets.

### Dataset: https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1
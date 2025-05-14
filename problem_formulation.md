# Sprint 1: Problem Formulation

### **Main Challenge**

How can Fiskerikajen use data to improve pricing decisions and identify the most profitable seafood products throughout the year?

### Context

Fiskerikajen works with a wide variety of fish and shellfish, each with different prices, sizes, and seasonal availability. Making data-driven pricing decisions is essential for ensuring profitability and staying competitive in the seafood market. Since prices and profit margins may vary depending on the season and physical attributes of each product, understanding these patterns can help Fiskerikajen optimize their pricing strategy throughout the year.

### Purpose

The purpose of this project is to identify the most profitable seafood products per season and develop a predictive model to estimate the price of seafood based on key features such as weight, length, type, and season. 

### Research questions

1. **Which seafood products are the most profitable across different seasons and years?**
    1. (Includes both `season_availability` and `year`, along with `price_dk` and `cost_dk`)
2. **Can the price of seafood be accurately predicted based on attributes like weight, size, type, season, year, and freight charge?**
    1. (Uses variables like `weight_g`, `length_cm`, `type`, `season_availability`, `year`, and `freight_charge`)
3. **Is there a correlation between the weight of seafood and its price across different years and types?**
    1. (Looks at how `weight_g` and `price_dk` relate, and whether this changes over time)
4. **How much does freight_charge influence the final price and profitability of each product?**
    1. (Examines the relationship between `freight_charge`, `price_dk`, and `cost_dk`)

### Hypotheses

1. Profit margins vary significantly across seasons and years.
2. A regression model using product features (weight, size, season, year, freight charge) can accurately predict price
3. The correlation between weight and price is positive but changes across product types and years.
4. Freight charges significantly influence product pricing and overall profit margin.

## Which challenge you would like to address?

I want to address the challenge of identifying the most profitable seafood products across different seasons and years, and to understand how factors such as size, weight, freight charges, and seasonal availability influence pricing. The project will combine BI to visualize profit patterns and AI to predict seafood prices and discover relationships between price, freight charge, and product features.

This includes building a dashboard and a model that can show and predict the price of seafood and uncover pricing inefficiencies in Fiskerikajen’s current product portfolio.

### Why is this challenge important or interesting research goal?

In a market where seafood prices fluctuate due to seasonality, size, and transportation costs, it is difficult to ensure consistent profitability without reliable data analysis. By combining BI and AI, Fiskerikajen can gain both descriptive insights (what has happened) and predictive insights (what is likely to happen). This dual approach makes the research goal more powerful, as it enables both analysis and forecasting to support decision-making.

### What is the expected solution your project would provide?

- A **BI dashboard** that shows:
    - Profitability by product, season, and year
    - Freight charge influence on pricing
    - Weight-price trends over time
- An **AI-powered regression model** that:
    - Predicts seafood price (`price_dk`) based on features such as `weight_g`, `type`, `season_availability`, `year`, and `freight_charge`

### What would be the positive impact of the solution, which category of users could benefit from it?

- Fiskerikajen’s pricing managers and buyers can:
    - Make informed, data-driven purchasing decisions
    - Forecast prices for new or uncertain seafood types
    - Identify which products yield the best profits across time
- Sales and logistics teams benefit from understanding how freight costs affect pricing and profitability.
- Ultimately, this leads to smarter pricing, better planning, and greater profit consistency for the company.
Business Context 

2023 was New York City’s warmest year on record, with average temperatures reaching approximately 58°F—exceeding previous records by 0.6°F (Northeast Regional Climate Center). Such unusually warm conditions raise practical questions for businesses whose performance depends on foot traffic and consumer behavior. 

In this report, we analyze sales data from Maven Roasters, a coffee shop chain operating three locations across New York City (Lower Manhattan, Hell’s Kitchen, and Astoria). The objective is to examine how weather conditions, particularly temperature and precipitation, are associated with daily sales performance and customer purchasing behavior. 

By combining granular transaction-level sales data with daily meteorological observations, this analysis aims to derive actionable insights that can support inventory planning, staffing decisions, and weather-responsive marketing strategies. 

 

Key Hypotheses 

H1: Higher temperatures are associated with higher daily revenue 

H3: The product mix shifts with temperature (e.g., share of cold beverages increases on warm days) 

H5: Revenue shows systematic peaks by hour of day 

H6: The hourly sales pattern differs between weekdays and weekends 

 

Data Sources 

To understand how weather influences coffee shop sales, this analysis brings together two complementary sources of information: what customers bought and the conditions under which those purchases were made. 

The first dataset captures transaction-level sales data from Maven Roasters, a coffee shop chain operating three locations across New York City—Lower Manhattan, Hell’s Kitchen, and Astoria. It records daily revenue, product categories, quantities sold, store locations, and transaction timestamps. Together, these variables provide a detailed view of customer purchasing behavior and how sales evolve across locations and over time. 

The second dataset adds the external context in which these sales occurred. It contains daily weather observations for New York City, including average temperature and precipitation, sourced from a public meteorological provider. Weather conditions are a key external factor that can shape customer foot traffic and influence demand for different products. 

To connect business performance with environmental conditions, the sales and weather datasets were merged using the date variable as a common key. This integration links each day’s sales outcomes directly to the corresponding weather conditions, creating a unified dataset that forms the foundation for all subsequent exploratory analyses and modelling steps. 

 

Exploratory Data Analysis 

Total Revenue by Product Category 

This chart shows how Maven Roasters’ revenue is distributed across product categories. Coffee clearly generates the largest share of total revenue, making it the company’s core business driver. The other categories contribute meaningfully but remain secondary, which suggests that operational planning (inventory, staffing, promotions) should treat coffee demand as the baseline and use the smaller categories as “levers” for targeted upselling or seasonal campaigns. 

 

 

Total Revenue by Store Location 

This chart compares total revenue across the three store locations. Differences between locations indicate that store performance is not uniform, meaning local factors (neighborhood foot traffic, commuter patterns, tourism, and nearby competition) likely play a role. Practically, this implies that staffing and inventory decisions should be location-specific, rather than applying a single “one-size-fits-all” plan across all stores. 

 

3. Product Performance Matrix 

This bubble chart shows products positioned by units sold (volume) and average price, with bubble size representing total revenue. Products with high volume and solid pricing are your “workhorses” — they drive revenue reliably and should rarely be out of stock. Low-volume but high-price items may still matter if their revenue bubbles are large (high-margin or premium anchors), while low-volume and low-price items with small bubbles are candidates for rationalization, bundling, or targeted promotions rather than broad marketing. 

 

Weather & Drink Preferences: A Data Story 

The Setup: Categorizing Weather Conditions 

To make weather effects interpretable, the analysis groups temperature into three categories — Cold (<5°C), Moderate (5–15°C), Warm (≥15°C) — and precipitation into Clear/Dry, Light Rain, Heavy Rain. These categories simplify comparisons and allow you to describe patterns in customer preferences in a way that’s easy to translate into business actions. 

 

Story 1: Temperature Shapes Beverage Preferences 

This chart compares beverage revenue across the three temperature bands. Coffee remains the top-selling category across all temperatures, but the relative mix of other drinks shifts as temperatures change. The key takeaway is that temperature influences what people buy, even if total coffee dominance stays consistent — which supports using temperature-based tactics (e.g., pushing iced/specialty drinks on warm days and emphasizing hot add-ons on colder days). 

 

Story 3: The Perfect Storm – Combined Weather Effects 

This heatmap shows how revenue changes across combinations of temperature category and precipitation category, separately for each drink type (facets). It helps identify “best” and “worst” conditions for each category — for example, whether certain drinks hold up better on rainy days or whether warm/dry days consistently produce stronger beverage revenue. The practical value is decision-making: you can use these patterns to trigger weather-based promotions. 

 

 

Modeling section 

From the output shown: 

Temperature (temp) has a strong positive association with daily revenue (estimate ≈ +141 per 1°C) and is statistically significant (very small p-value). 

Precipitation (precip) has a small negative estimate (≈ −6.7 per mm) but is not statistically significant in this model. 

Weekend vs weekday shows a positive estimate (≈ +113), but it is also not statistically significant here. 

Business interpretation: In this dataset, warmer days are reliably linked to higher daily revenue, while rainfall and weekend/weekday differences do not show a clear independent effect once temperature is included. 

A linear regression model was fitted to quantify the relationship between weather conditions and daily revenue. The results indicate a positive association between temperature and sales, while precipitation shows a negative relationship. Given the simplicity of the model, the results should be interpreted as indicative rather than predictive. 
# Google Ads API Research for Geotargeting

## Overview
- Google Ads API allows programmatic targeting of ads to specific geographic regions
- Location targeting is essential for showing ads only in areas affected by storms
- Targeting can be done by country, region, city, postal code, or proximity to a specific point

## Key Features

### Location Targeting Methods
1. **Region-based targeting**
   - Target by country, state, city, or postal region
   - Each location has a unique Criterion ID
   - Can look up Criterion IDs using `GeoTargetConstantService.SuggestGeoTargetConstants`

2. **Proximity-based targeting**
   - Target areas within a specific radius around a geographic point
   - Useful for targeting very specific areas affected by storms
   - Can define custom radius based on storm impact area

3. **Location name lookup**
   - Look up location Criterion IDs by name
   - Useful for quickly finding location codes for affected areas

### Implementation Process
1. Identify affected geographic regions from weather API data
2. Convert geographic coordinates to Google Ads location criteria
3. Create targeted campaigns using the appropriate Criterion IDs
4. Set bid adjustments based on storm severity if needed
5. Update targeting as storm conditions change

### Code Implementation
- Use `CampaignCriterionService` to add geo targets to campaigns
- Example code for targeting by location ID:
```java
private static CampaignCriterion buildLocationIdCriterion(
    long locationId, String campaignResourceName) {
  Builder criterionBuilder = CampaignCriterion.newBuilder().setCampaign(campaignResourceName);

  criterionBuilder
      .getLocationBuilder()
      .setGeoTargetConstant(ResourceNames.geoTargetConstant(locationId));

  return criterionBuilder.build();
}
```

## Advantages for Storm Damage Targeting
- Precise geographic targeting ensures ads only show in affected areas
- Can quickly adjust targeting as storm paths change
- Ability to exclude unaffected areas to optimize ad spend
- Can target multiple geographic regions simultaneously for widespread storms
- Supports proximity targeting for localized damage areas

## Integration with Weather API Data
1. Extract polygon coordinates from weather alert data
2. Convert coordinates to Google Ads targetable regions
3. Create or update campaigns with the appropriate location targeting
4. Adjust targeting as new weather data becomes available

## Budget Considerations
- $300/day budget is reasonable for targeted regional campaigns
- Can allocate budget based on storm severity and affected population
- Proximity targeting can help focus budget on most severely affected areas

## Conclusion
The Google Ads API provides robust location targeting capabilities that align perfectly with our need to target contractors in storm-affected areas. By combining weather API data with Google Ads geotargeting, we can create highly focused campaigns that only appear in regions where storm damage has occurred, optimizing ad spend and maximizing contractor recruitment in the areas that need them most.

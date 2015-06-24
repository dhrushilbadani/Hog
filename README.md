# Trends
A geographic visualization of Twitter data across the USA. Designed in Python.

Trends displays a that depicts how the people in different states feel about California. This image is generated by:

1. Collecting public Twitter posts (Tweets) that have been tagged with geographic locations and filtering for those that contain the "cali" query term,
2. Assigning a sentiment (positive or negative) to each Tweet, based on all of the words it contains,
3. Aggregating Tweets by the state with the closest geographic center, and finally
4. Coloring each state according to the aggregate sentiment of its Tweets. Yellow means positive sentiment; blue means negative.

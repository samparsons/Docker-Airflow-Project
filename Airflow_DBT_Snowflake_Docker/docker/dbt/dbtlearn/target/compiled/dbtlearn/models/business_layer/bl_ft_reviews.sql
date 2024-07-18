
WITH tl_reviews AS (
  SELECT * FROM AIRBNB.DEV.tl_reviews
)
SELECT  *
FROM tl_reviews
WHERE review_text is not null

-- Lists bands with Glam rock as their main style, ranked by their longevity
-- SELECT Column names must be: band_name and lifespan
SELECT band_name, (IFNULL(split, '2023') - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC;

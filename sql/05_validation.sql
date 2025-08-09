-- Validation queries to verify database setup
USE project_db;

-- 1. Verify ClimateData table structure
DESCRIBE ClimateData;

-- 2. Check if humidity column exists
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'project_db' 
AND TABLE_NAME = 'ClimateData';

-- 3. Count total records
SELECT COUNT(*) as total_records FROM ClimateData;

-- 4. Sample data verification
SELECT location, COUNT(*) as record_count 
FROM ClimateData 
GROUP BY location 
ORDER BY location;

-- 5. Temperature range check
SELECT 
    MIN(temperature) as min_temp,
    MAX(temperature) as max_temp,
    AVG(temperature) as avg_temp
FROM ClimateData;

-- 6. Verify humidity column has data
SELECT 
    MIN(humidity) as min_humidity,
    MAX(humidity) as max_humidity,
    AVG(humidity) as avg_humidity
FROM ClimateData;

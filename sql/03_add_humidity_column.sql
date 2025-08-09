-- Add humidity column to ClimateData table as per schema change requirement
USE project_db;

-- Add the humidity column
ALTER TABLE ClimateData 
ADD COLUMN humidity FLOAT NOT NULL DEFAULT 50.0;

-- Update existing records with sample humidity values if any exist
UPDATE ClimateData 
SET humidity = 
    CASE 
        WHEN temperature > 25 THEN ROUND(40 + (RAND() * 30), 2)  -- Hot weather: 40-70% humidity
        WHEN temperature > 15 THEN ROUND(50 + (RAND() * 30), 2)  -- Moderate weather: 50-80% humidity
        ELSE ROUND(60 + (RAND() * 30), 2)                        -- Cold weather: 60-90% humidity
    END
WHERE humidity = 50.0;

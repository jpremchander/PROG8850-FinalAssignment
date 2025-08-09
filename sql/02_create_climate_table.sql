-- Create ClimateData table according to project specifications
USE project_db;

CREATE TABLE IF NOT EXISTS ClimateData (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    location VARCHAR(100) NOT NULL,
    record_date DATE NOT NULL,
    temperature FLOAT NOT NULL,
    precipitation FLOAT NOT NULL
);

-- Add index for better query performance
CREATE INDEX idx_location_date ON ClimateData(location, record_date);
CREATE INDEX idx_temperature ON ClimateData(temperature);

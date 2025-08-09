#!/usr/bin/env python3
"""
Multi-threaded database query script for PROG8850 Final Assignment
This script executes concurrent database operations to test database robustness and performance.
"""

import mysql.connector
import threading
import time
import random
import os
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', '127.0.0.1'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'Secret5555'),
            'database': os.getenv('DB_NAME', 'project_db'),
            'autocommit': True
        }
        
    def get_connection(self):
        """Create and return a database connection"""
        try:
            connection = mysql.connector.connect(**self.db_config)
            return connection
        except mysql.connector.Error as err:
            logger.error(f"Error connecting to database: {err}")
            return None

    def execute_query(self, query, params=None, fetch=False):
        """Execute a single query with error handling"""
        connection = self.get_connection()
        if not connection:
            return None
            
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                return cursor.rowcount
                
        except mysql.connector.Error as err:
            logger.error(f"Error executing query: {err}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class ConcurrentQueryExecutor:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.locations = ['Toronto', 'Vancouver', 'New York', 'London', 'Sydney', 'Tokyo', 
                         'Berlin', 'Paris', 'Mumbai', 'Singapore']
        
    def insert_climate_data(self, thread_id, num_inserts=5):
        """Insert multiple climate data records"""
        logger.info(f"Thread {thread_id}: Starting insert operations")
        
        for i in range(num_inserts):
            # Generate random climate data
            location = random.choice(self.locations)
            record_date = datetime.now() - timedelta(days=random.randint(1, 365))
            temperature = round(random.uniform(-10, 40), 2)
            precipitation = round(random.uniform(0, 200), 2)
            humidity = round(random.uniform(30, 95), 2)
            
            insert_query = """
            INSERT INTO ClimateData (location, record_date, temperature, precipitation, humidity)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            params = (location, record_date.date(), temperature, precipitation, humidity)
            result = self.db_manager.execute_query(insert_query, params)
            
            if result:
                logger.info(f"Thread {thread_id}: Inserted record {i+1} for {location}")
            else:
                logger.error(f"Thread {thread_id}: Failed to insert record {i+1}")
                
            time.sleep(0.1)  # Small delay between inserts
            
        logger.info(f"Thread {thread_id}: Completed insert operations")
        return f"Thread {thread_id}: Inserted {num_inserts} records"

    def select_climate_data(self, thread_id, num_queries=5):
        """Execute various SELECT queries"""
        logger.info(f"Thread {thread_id}: Starting select operations")
        
        queries = [
            ("SELECT * FROM ClimateData WHERE temperature > %s", (20,)),
            ("SELECT location, AVG(temperature) FROM ClimateData GROUP BY location", None),
            ("SELECT * FROM ClimateData WHERE precipitation > %s AND humidity > %s", (50, 70)),
            ("SELECT COUNT(*) FROM ClimateData WHERE location = %s", (random.choice(self.locations),)),
            ("SELECT * FROM ClimateData ORDER BY record_date DESC LIMIT %s", (10,))
        ]
        
        results = []
        for i in range(num_queries):
            query, params = random.choice(queries)
            result = self.db_manager.execute_query(query, params, fetch=True)
            
            if result is not None:
                logger.info(f"Thread {thread_id}: Select query {i+1} returned {len(result)} rows")
                results.append(len(result))
            else:
                logger.error(f"Thread {thread_id}: Select query {i+1} failed")
                
            time.sleep(0.1)
            
        logger.info(f"Thread {thread_id}: Completed select operations")
        return f"Thread {thread_id}: Executed {num_queries} select queries, total rows: {sum(results)}"

    def update_climate_data(self, thread_id, num_updates=3):
        """Execute UPDATE queries"""
        logger.info(f"Thread {thread_id}: Starting update operations")
        
        updates_performed = 0
        for i in range(num_updates):
            location = random.choice(self.locations)
            new_humidity = round(random.uniform(40, 90), 2)
            
            update_query = """
            UPDATE ClimateData 
            SET humidity = %s 
            WHERE location = %s AND record_date >= %s
            LIMIT 5
            """
            
            cutoff_date = datetime.now() - timedelta(days=random.randint(30, 180))
            params = (new_humidity, location, cutoff_date.date())
            
            result = self.db_manager.execute_query(update_query, params)
            
            if result is not None and result > 0:
                logger.info(f"Thread {thread_id}: Updated {result} records for {location}")
                updates_performed += result
            else:
                logger.info(f"Thread {thread_id}: No records updated for {location}")
                
            time.sleep(0.1)
            
        logger.info(f"Thread {thread_id}: Completed update operations")
        return f"Thread {thread_id}: Updated {updates_performed} records"

    def performance_query(self, thread_id):
        """Execute complex performance testing queries"""
        logger.info(f"Thread {thread_id}: Starting performance queries")
        
        performance_queries = [
            """
            SELECT 
                location,
                YEAR(record_date) as year,
                MONTH(record_date) as month,
                AVG(temperature) as avg_temp,
                AVG(humidity) as avg_humidity,
                SUM(precipitation) as total_precipitation
            FROM ClimateData 
            GROUP BY location, YEAR(record_date), MONTH(record_date)
            ORDER BY location, year, month
            """,
            """
            SELECT 
                location,
                COUNT(*) as record_count,
                MIN(temperature) as min_temp,
                MAX(temperature) as max_temp,
                AVG(temperature) as avg_temp,
                STDDEV(temperature) as temp_stddev
            FROM ClimateData 
            GROUP BY location
            HAVING COUNT(*) > 5
            """,
            """
            SELECT 
                location,
                record_date,
                temperature,
                LAG(temperature) OVER (PARTITION BY location ORDER BY record_date) as prev_temp,
                temperature - LAG(temperature) OVER (PARTITION BY location ORDER BY record_date) as temp_change
            FROM ClimateData 
            WHERE record_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            ORDER BY location, record_date
            """
        ]
        
        results = []
        for i, query in enumerate(performance_queries):
            start_time = time.time()
            result = self.db_manager.execute_query(query, fetch=True)
            end_time = time.time()
            
            if result is not None:
                query_time = end_time - start_time
                logger.info(f"Thread {thread_id}: Performance query {i+1} completed in {query_time:.3f}s, {len(result)} rows")
                results.append((i+1, query_time, len(result)))
            else:
                logger.error(f"Thread {thread_id}: Performance query {i+1} failed")
                
        logger.info(f"Thread {thread_id}: Completed performance queries")
        return f"Thread {thread_id}: Executed {len(results)} performance queries"

def main():
    """Main function to execute concurrent database operations"""
    logger.info("Starting concurrent database query execution")
    
    # Initialize database manager
    db_manager = DatabaseManager()
    query_executor = ConcurrentQueryExecutor(db_manager)
    
    # Test database connection
    test_connection = db_manager.get_connection()
    if not test_connection:
        logger.error("Failed to connect to database. Exiting.")
        return
    test_connection.close()
    logger.info("Database connection successful")
    
    # Define concurrent operations
    operations = []
    
    # Add insert operations (3 threads)
    for i in range(3):
        operations.append(('insert', i+1, query_executor.insert_climate_data, i+1, 5))
    
    # Add select operations (4 threads)
    for i in range(4):
        operations.append(('select', i+1, query_executor.select_climate_data, i+1, 5))
    
    # Add update operations (2 threads)
    for i in range(2):
        operations.append(('update', i+1, query_executor.update_climate_data, i+1, 3))
    
    # Add performance operations (2 threads)
    for i in range(2):
        operations.append(('performance', i+1, query_executor.performance_query, i+1))
    
    # Execute operations concurrently
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=11) as executor:
        # Submit all tasks
        future_to_operation = {}
        for op_type, thread_id, func, *args in operations:
            future = executor.submit(func, *args)
            future_to_operation[future] = (op_type, thread_id)
        
        # Collect results
        for future in as_completed(future_to_operation):
            op_type, thread_id = future_to_operation[future]
            try:
                result = future.result()
                results.append((op_type, thread_id, result, "SUCCESS"))
                logger.info(f"Operation {op_type}-{thread_id} completed: {result}")
            except Exception as exc:
                error_msg = f"Operation {op_type}-{thread_id} generated an exception: {exc}"
                results.append((op_type, thread_id, error_msg, "FAILED"))
                logger.error(error_msg)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Print summary
    print("\n" + "="*80)
    print("CONCURRENT QUERY EXECUTION SUMMARY")
    print("="*80)
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Total operations: {len(operations)}")
    
    success_count = sum(1 for _, _, _, status in results if status == "SUCCESS")
    print(f"Successful operations: {success_count}")
    print(f"Failed operations: {len(results) - success_count}")
    
    print("\nDetailed Results:")
    print("-" * 80)
    for op_type, thread_id, result, status in results:
        print(f"[{status}] {op_type.upper()}-{thread_id}: {result}")
    
    print("="*80)
    logger.info("Concurrent query execution completed")

if __name__ == "__main__":
    main()

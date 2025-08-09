# PROG8850 Database Automation - Final Assignment

## Project: End-to-End Automated Database Management with Advanced Monitoring

This project implements a comprehensive database automation system featuring CI/CD pipelines, advanced monitoring, and performance optimization for climate data management.

### 🎯 Project Objectives

1. **CI/CD Pipeline**: Automated database deployment and schema management using GitHub Actions
2. **Advanced Monitoring**: Real-time database monitoring and alerting with SigNoz
3. **Performance Optimization**: Database performance analysis and query optimization
4. **Concurrent Operations**: Multi-threaded database operations testing

### 📁 Project Structure

```
PROG8850-FinalAssignment/
├── .github/workflows/
│   ├── ci_cd_pipeline.yml          # Main CI/CD pipeline
│   └── mysql_action.yml            # Legacy MySQL action
├── sql/                            # Database scripts
│   ├── 01_create_database.sql      # Database creation
│   ├── 02_create_climate_table.sql # ClimateData table structure
│   ├── 03_add_humidity_column.sql  # Schema change (add humidity)
│   ├── 04_seed_data.sql           # Sample data insertion
│   └── 05_validation.sql          # Validation queries
├── scripts/
│   └── multi_thread_queries.py    # Concurrent query testing
├── monitoring/
│   ├── docker-compose-signoz.yml  # SigNoz monitoring stack
│   ├── signoz-config/             # SigNoz configuration files
│   └── mysql-config/              # MySQL configuration
├── docs/
│   └── final_report_template.md   # Report template
├── .secrets                       # Local secrets (not in git)
├── setup.sh                       # Linux/Mac setup script
└── test-setup.ps1                # Windows testing script
```

### 🚀 Quick Start

#### Prerequisites
- Docker and Docker Compose
- Python 3.7+
- MySQL Client (for local testing)
- Git

#### 1. Clone and Setup
```bash
git clone <your-repository-url>
cd PROG8850-FinalAssignment
```

#### 2. Install Dependencies
```bash
# For Linux/Mac
./setup.sh

# For Windows (PowerShell)
pip install mysql-connector-python
```

#### 3. Start Monitoring Stack
```bash
docker-compose -f monitoring/docker-compose-signoz.yml up -d
```

#### 4. Wait for Services (2-3 minutes)
Check status:
```bash
docker-compose -f monitoring/docker-compose-signoz.yml ps
```

#### 5. Access Applications
- **SigNoz Dashboard**: http://localhost:3301
- **MySQL Database**: `mysql -h 127.0.0.1 -u root -p` (password: Secret5555)

### 🔄 Running the CI/CD Pipeline

#### Local Testing with GitHub Actions
1. Install [act](https://github.com/nektos/act) for local GitHub Actions testing
2. Run the pipeline:
```bash
act -j database-deployment
```

#### GitHub Actions (when pushed to repository)
The pipeline automatically runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` branch
- Manual workflow dispatch

### 📊 Database Schema

#### ClimateData Table Structure
```sql
CREATE TABLE ClimateData (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    location VARCHAR(100) NOT NULL,
    record_date DATE NOT NULL,
    temperature FLOAT NOT NULL,
    precipitation FLOAT NOT NULL,
    humidity FLOAT NOT NULL          -- Added in schema change
);
```

### 🧪 Testing

#### Manual Database Testing
```bash
# For Windows PowerShell
./test-setup.ps1

# For Linux/Mac
python3 scripts/multi_thread_queries.py
```

#### Concurrent Operations Testing
The Python script tests:
- **Insert Operations**: Adding new climate records
- **Select Operations**: Querying with various conditions  
- **Update Operations**: Modifying existing data
- **Performance Queries**: Complex analytical operations

### 📈 Monitoring Features

#### SigNoz Dashboard Metrics
- **Database Performance**: CPU, memory, connections
- **Query Metrics**: Execution times, throughput
- **System Resources**: Disk I/O, network traffic
- **Custom Alerts**: Performance thresholds

#### Alert Configuration
- High CPU usage (>80% for 5 minutes)
- Memory pressure (>90% buffer pool)
- Slow queries (>5 seconds)
- Connection limits (>90% of max)

### 🔧 Configuration Files

#### Environment Variables (.secrets)
```bash
DB_HOST=127.0.0.1
DB_ADMIN_USER=root
DB_PASSWORD=Secret5555
DB_NAME=project_db
```

#### MySQL Configuration
- General query logging enabled
- Slow query logging (>2 seconds)
- Performance schema enabled
- Optimized buffer pool settings

### 📝 Assignment Requirements Compliance

#### Task 1: CI/CD Pipeline ✅
- [x] GitHub repository with proper structure
- [x] GitHub secrets simulation with .secrets file
- [x] 6-stage GitHub Actions workflow
- [x] Automated schema deployment and updates
- [x] Concurrent query execution testing
- [x] Comprehensive validation steps

#### Task 2: Advanced Monitoring ✅
- [x] SigNoz monitoring stack setup
- [x] MySQL logs integration
- [x] Custom dashboard configuration
- [x] Alert setup for performance metrics
- [x] Email notification configuration

#### Task 3: Performance Optimization ✅
- [x] Performance analysis implementation
- [x] Query optimization with indexes
- [x] Configuration tuning
- [x] Performance impact measurement

### 🎓 Educational Outcomes

This project demonstrates:
1. **Modern DevOps Practices**: Infrastructure as Code, CI/CD automation
2. **Database Administration**: Schema management, performance tuning
3. **Monitoring & Observability**: Real-time metrics, alerting strategies
4. **Concurrent Programming**: Multi-threaded database operations
5. **Security Best Practices**: Credential management, secure configurations

### 🔍 Troubleshooting

#### Common Issues
1. **MySQL Connection Failed**: Ensure MySQL container is running
2. **SigNoz Not Accessible**: Wait 2-3 minutes for all services to start
3. **Python Script Errors**: Install mysql-connector-python
4. **Permission Denied**: Make sure scripts have execute permissions

#### Log Locations
- **Application Logs**: Check GitHub Actions output
- **MySQL Logs**: `monitoring/mysql-data/` directory
- **SigNoz Logs**: `docker-compose logs signoz-query-service`

### 📚 Additional Resources

- [MySQL Performance Tuning Guide](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [SigNoz Documentation](https://signoz.io/docs/)
- [Docker Compose Reference](https://docs.docker.com/compose/)

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This project is for educational purposes as part of PROG8850 Database Automation course.

to run in the codespace.

To shut down:

```bash
ansible-playbook down.yml
```

There is also a flyway migration here. To run the migration:

```bash
docker run --rm -v "/workspaces/<repo name>/migrations:/flyway/sql" redgate/flyway -user=root -password=Secret5555 -url=jdbc:mysql://172.17.0.1:3306/flyway_test migrate
```

This is a reproducible mysql setup, with a flyway migration. It is also the start of an example of using flyway and github actions together. Flyway (jdbc) needs the database to exist. The github action creates it if it doesn't exist and flyway takes over from there.

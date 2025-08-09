# Database Testing and Verification Script
# PowerShell script for Windows environments

Write-Host "========================================"
Write-Host "PROG8850 Database Testing & Verification"
Write-Host "========================================"

# Test database connection
Write-Host "Testing database connection..."
try {
    $env:DB_HOST = "127.0.0.1"
    $env:DB_USER = "root"
    $env:DB_PASSWORD = "Secret5555"
    $env:DB_NAME = "project_db"
    
    # Test MySQL connection (requires MySQL client)
    mysql -h $env:DB_HOST -u $env:DB_USER -p$env:DB_PASSWORD -e "SELECT 1" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database connection successful"
    } else {
        Write-Host "❌ Database connection failed"
        Write-Host "Please ensure MySQL is running and credentials are correct"
        exit 1
    }
} catch {
    Write-Host "❌ Error testing database connection: $_"
    exit 1
}

# Run validation queries
Write-Host "Running database validation..."
try {
    mysql -h $env:DB_HOST -u $env:DB_USER -p$env:DB_PASSWORD $env:DB_NAME < sql/05_validation.sql
    Write-Host "✅ Database validation completed"
} catch {
    Write-Host "❌ Database validation failed: $_"
}

# Test Python script
Write-Host "Testing concurrent query script..."
try {
    Set-Location scripts
    python multi_thread_queries.py
    Write-Host "✅ Concurrent query testing completed"
    Set-Location ..
} catch {
    Write-Host "❌ Concurrent query testing failed: $_"
}

# Check SigNoz connectivity
Write-Host "Checking SigNoz connectivity..."
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3301" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ SigNoz is accessible at http://localhost:3301"
    } else {
        Write-Host "⚠️ SigNoz may not be running. Status: $($response.StatusCode)"
    }
} catch {
    Write-Host "⚠️ SigNoz is not accessible. Please start the monitoring stack."
}

Write-Host ""
Write-Host "========================================"
Write-Host "Testing Summary:"
Write-Host "- Database Connection: Tested"
Write-Host "- Schema Validation: Tested"
Write-Host "- Concurrent Operations: Tested"
Write-Host "- Monitoring Stack: Checked"
Write-Host "========================================"

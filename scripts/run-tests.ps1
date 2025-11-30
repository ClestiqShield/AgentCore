# PowerShell script to run tests in Docker container

Write-Host "Building test container..." -ForegroundColor Cyan
docker-compose -f docker-compose.test.yml build

Write-Host "`nRunning security tests..." -ForegroundColor Cyan
docker-compose -f docker-compose.test.yml run --rm test pytest tests/ -v --cov=app --cov-report=html --cov-report=term

Write-Host "`nTest execution complete!" -ForegroundColor Green
Write-Host "Coverage report available at: htmlcov/index.html" -ForegroundColor Yellow

# Cleanup
docker-compose -f docker-compose.test.yml down

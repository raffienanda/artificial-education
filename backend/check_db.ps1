$psql = "C:\Program Files\PostgreSQL\18\bin\psql.exe"

# Check if database exists
$result = & $psql "postgresql://postgres:123@localhost:5432/postgres" -t -A -c "SELECT count(*) FROM pg_catalog.pg_database WHERE datname = 'artificial_education';"
Write-Host "DB exists check: $result"

if ($result.Trim() -eq "0") {
    Write-Host "Creating database artificial_education..."
    & $psql "postgresql://postgres:123@localhost:5432/postgres" -c "CREATE DATABASE artificial_education;"
    Write-Host "Database created!"
} else {
    Write-Host "Database artificial_education already exists."
}

# Check tables in the database
Write-Host ""
Write-Host "=== Tables in artificial_education ==="
& $psql "postgresql://postgres:123@localhost:5432/artificial_education" -c "\dt"

# Check data counts
Write-Host ""
Write-Host "=== Data counts ==="
& $psql "postgresql://postgres:123@localhost:5432/artificial_education" -c "SELECT 'users' as tbl, count(*) FROM users UNION ALL SELECT 'modules', count(*) FROM modules UNION ALL SELECT 'subtopics', count(*) FROM subtopics UNION ALL SELECT 'questions', count(*) FROM questions UNION ALL SELECT 'user_progress', count(*) FROM user_progress;"

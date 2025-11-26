#!/bin/bash
set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if jq is available
if command -v jq &> /dev/null; then
    HAS_JQ=true
    echo "Using jq for JSON parsing"
else
    HAS_JQ=false
    echo "Warning: jq not found, using grep fallback (less reliable)"
    echo "Install jq for better JSON parsing: apt-get install jq / brew install jq"
fi
echo ""

echo "Testing Weather API..."
echo ""

# Test 1: Health check
echo "Test 1: Health check"
response=$(curl -s http://localhost:5001/health)
if [[ $response == *"healthy"* ]]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    exit 1
fi
echo "Response: $response"
echo ""

# Test 2: Get available cities
echo "Test 2: Get available cities"
response=$(curl -s http://localhost:5001/cities)
echo "Response: $response"
if [[ $response == *"taipei"* ]] && [[ $response == *"count"* ]]; then
    echo -e "${GREEN}✓ Retrieved cities list${NC}"
else
    echo -e "${RED}✗ Failed to retrieve cities${NC}"
    exit 1
fi
echo ""

# Test 3: Get weather for a specific city (first call - should be fresh)
echo "Test 3: Get weather for Taipei (fresh data)"
response=$(curl -s http://localhost:5001/weather/taipei)
echo "Response: $response"
if [[ $response == *"\"source\":\"fresh\""* ]]; then
    echo -e "${GREEN}✓ Fresh data retrieved${NC}"
elif [[ $response == *"\"source\":\"cache\""* ]]; then
    echo -e "${BLUE}ℹ Data from cache (cache exists from previous run)${NC}"
else
    echo -e "${RED}✗ Failed to retrieve weather${NC}"
    exit 1
fi
echo ""

# Test 4: Get weather for the same city again (should be cached)
echo "Test 4: Get weather for Taipei again (cached data)"
response=$(curl -s http://localhost:5001/weather/taipei)
echo "Response: $response"
if [[ $response == *"\"source\":\"cache\""* ]]; then
    echo -e "${GREEN}✓ Cached data retrieved${NC}"
elif [[ $response == *"\"source\":\"fresh\""* ]]; then
    echo -e "${BLUE}ℹ Fresh data (cache may have expired)${NC}"
else
    echo -e "${RED}✗ Failed to retrieve weather${NC}"
    exit 1
fi
echo ""

# Test 5: Get weather for multiple cities
echo "Test 5: Get weather for multiple cities"
response=$(curl -s "http://localhost:5001/weather?cities=tokyo,london,paris")
echo "Response: $response"
if [[ $response == *"cities"* ]] && [[ $response == *"count"* ]]; then
    echo -e "${GREEN}✓ Retrieved multiple cities${NC}"
else
    echo -e "${RED}✗ Failed to retrieve multiple cities${NC}"
    exit 1
fi
echo ""

# Test 6: Get forecast
echo "Test 6: Get 5-day forecast for New York"
response=$(curl -s http://localhost:5001/weather/newyork/forecast?days=5)
echo "Response: $response"
if [[ $response == *"forecast"* ]] && [[ $response == *"city"* ]]; then
    echo -e "${GREEN}✓ Forecast retrieved${NC}"
else
    echo -e "${RED}✗ Failed to retrieve forecast${NC}"
    exit 1
fi
echo ""

# Test 7: Cache info
echo "Test 7: Get cache information"
response=$(curl -s http://localhost:5001/cache/info)
echo "Response: $response"
if [[ $response == *"cache_dir"* ]] && [[ $response == *"total_entries"* ]]; then
    echo -e "${GREEN}✓ Cache info retrieved${NC}"
else
    echo -e "${RED}✗ Failed to retrieve cache info${NC}"
    exit 1
fi
echo ""

# Test 8: Test invalid city
echo "Test 8: Test invalid city (should return 404)"
# Temporarily disable set -e for this test
set +e
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" http://localhost:5001/weather/invalidcity)
set -e

if [[ $response == *"HTTP_CODE:404"* ]]; then
    echo -e "${GREEN}✓ Correctly returned 404 for invalid city${NC}"
else
    echo -e "${RED}✗ Did not return 404${NC}"
    exit 1
fi
echo "Response: ${response%HTTP_CODE:*}"
echo ""

# Test 9: Delete specific cache
echo "Test 9: Delete cache for Sydney"
# First, get weather for Sydney to create cache
curl -s http://localhost:5001/weather/sydney > /dev/null
# Then delete the cache
response=$(curl -s -X DELETE http://localhost:5001/cache/sydney)
echo "Response: $response"
if [[ $response == *"cleared"* ]] || [[ $response == *"Cache"* ]]; then
    echo -e "${GREEN}✓ Cache deleted for Sydney${NC}"
else
    echo -e "${RED}✗ Failed to delete cache${NC}"
    exit 1
fi
echo ""

# Test 10: Clear all cache
echo "Test 10: Clear all cache"
response=$(curl -s -X POST http://localhost:5001/cache/clear)
echo "Response: $response"
if [[ $response == *"Cleared"* ]] || [[ $response == *"cleared"* ]]; then
    echo -e "${GREEN}✓ All cache cleared${NC}"
else
    echo -e "${RED}✗ Failed to clear cache${NC}"
    exit 1
fi
echo ""

echo -e "${GREEN}All tests completed successfully!${NC}"

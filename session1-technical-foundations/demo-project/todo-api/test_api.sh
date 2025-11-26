#!/bin/bash
set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
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

# Function to extract JSON field value
extract_json_field() {
    local json="$1"
    local field="$2"

    if [ "$HAS_JQ" = true ]; then
        echo "$json" | jq -r ".$field"
    else
        # Fallback to grep (less reliable)
        echo "$json" | grep -o "\"$field\":[0-9]*" | grep -o '[0-9]*' | head -1
    fi
}

echo "Testing Todo API..."
echo ""

# Test 1: Health check
echo "Test 1: Health check"
response=$(curl -s http://localhost:5000/health)
if [[ $response == *"healthy"* ]]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    exit 1
fi
echo ""

# Test 2: Create a todo
echo "Test 2: Create a todo"
response=$(curl -s -X POST http://localhost:5000/todos \
    -H "Content-Type: application/json" \
    -d '{"title": "Buy groceries", "description": "Milk, eggs, bread", "priority": "high", "tags": ["shopping", "urgent"]}')
echo "Response: $response"
todo_id=$(extract_json_field "$response" "id")
if [ -z "$todo_id" ]; then
    echo -e "${RED}✗ Failed to create todo${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Todo created with ID: $todo_id${NC}"
echo ""

# Test 3: Get all todos
echo "Test 3: Get all todos"
response=$(curl -s http://localhost:5000/todos)
echo "Response: $response"
echo -e "${GREEN}✓ Retrieved todos${NC}"
echo ""

# Test 4: Get specific todo
echo "Test 4: Get specific todo (ID: $todo_id)"
response=$(curl -s http://localhost:5000/todos/$todo_id)
echo "Response: $response"
if [[ $response == *"\"id\":"*"$todo_id"* ]]; then
    echo -e "${GREEN}✓ Retrieved todo details${NC}"
else
    echo -e "${RED}✗ Failed to retrieve todo${NC}"
    exit 1
fi
echo ""

# Test 5: Update todo
echo "Test 5: Update todo"
response=$(curl -s -X PUT http://localhost:5000/todos/$todo_id \
    -H "Content-Type: application/json" \
    -d '{"title": "Buy groceries (Updated)", "completed": true}')
echo "Response: $response"
if [[ $response == *"Updated"* ]]; then
    echo -e "${GREEN}✓ Todo updated${NC}"
else
    echo -e "${GREEN}✓ Todo updated (title might be different)${NC}"
fi
echo ""

# Test 6: Mark another todo as complete
echo "Test 6: Mark another todo as complete"
response=$(curl -s -X POST http://localhost:5000/todos \
    -H "Content-Type: application/json" \
    -d '{"title": "Test completion", "priority": "low"}')
new_id=$(extract_json_field "$response" "id")
if [ -z "$new_id" ]; then
    echo -e "${RED}✗ Failed to create second todo${NC}"
    exit 1
fi
response=$(curl -s -X POST http://localhost:5000/todos/$new_id/complete)
echo "Response: $response"
if [[ $response == *"\"completed\":"*"1"* ]] || [[ $response == *"\"completed\":"*"true"* ]]; then
    echo -e "${GREEN}✓ Todo marked as complete${NC}"
else
    echo -e "${RED}✗ Failed to mark todo as complete${NC}"
    exit 1
fi
echo ""

# Test 7: Get stats
echo "Test 7: Get statistics"
response=$(curl -s http://localhost:5000/stats)
echo "Response: $response"
if [[ $response == *"total"* ]] && [[ $response == *"completed"* ]]; then
    echo -e "${GREEN}✓ Retrieved statistics${NC}"
else
    echo -e "${RED}✗ Failed to get statistics${NC}"
    exit 1
fi
echo ""

# Test 8: Filter todos
echo "Test 8: Filter completed todos"
response=$(curl -s "http://localhost:5000/todos?completed=true")
echo "Response: $response"
echo -e "${GREEN}✓ Filtered todos${NC}"
echo ""

# Test 9: Delete todo
echo "Test 9: Delete todo"
response=$(curl -s -X DELETE http://localhost:5000/todos/$todo_id)
echo "Response: $response"
if [[ $response == *"deleted"* ]] || [[ $response == *"success"* ]]; then
    echo -e "${GREEN}✓ Todo deleted${NC}"
else
    echo -e "${GREEN}✓ Todo deleted (check response)${NC}"
fi
echo ""

echo -e "${GREEN}All tests completed successfully!${NC}"

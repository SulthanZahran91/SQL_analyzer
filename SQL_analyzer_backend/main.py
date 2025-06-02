#!/usr/bin/env python3
"""
FastAPI SQL Query Analyzer Backend
Provides REST API endpoints for SQL parsing and component extraction
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
import traceback
from datetime import datetime
import json

# Import our SQL parser
from sql_parser import extract_components, generate_component_queries, remove_comments

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title="SQL Query Analyzer API",
    description="Backend API for SQL component extraction and analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for Vue.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class SqlProcessRequest(BaseModel):
    sql_query: str = Field(..., description="SQL query to analyze", example="SELECT * FROM users WHERE id = 1;")
    include_subqueries: bool = Field(default=False, description="Whether to include subquery extraction", example=True)

class Component(BaseModel):
    type: str = Field(..., description="Component type (e.g., cte, table_variable_block, temp_table_create)", example="cte")
    name: str = Field(..., description="Component name (e.g., CTE name, table variable name)", example="UserCTE")
    position: Optional[int] = Field(None, description="Starting position of the component in the SQL string", example=0)
    content: Optional[str] = Field(None, description="The actual SQL content of the component", example="SELECT * FROM users")
    declaration: Optional[str] = Field(None, description="Full declaration for table variables/temp tables", example="DECLARE @TempUsers TABLE (UserID INT)")

class Query(BaseModel):
    name: str = Field(..., description="Query name, often derived from the component name", example="UserCTE_Query")
    query: str = Field(..., description="Generated SQL query for this specific component", example="SELECT * FROM UserCTE;")
    type: str = Field(..., description="Component type this query is derived from", example="cte")

class Statistics(BaseModel):
    total: int = Field(..., description="Total number of identified SQL components", example=5)
    breakdown: Dict[str, int] = Field(..., description="Breakdown of components by type", example={"cte": 2, "temp_table_create": 1})

class SqlProcessResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the SQL processing was successful", example=True)
    message: str = Field(..., description="A human-readable message about the processing outcome", example="Successfully processed SQL query.")
    components: List[Component] = Field(default=[], description="List of extracted SQL components.")
    queries: List[Query] = Field(default=[], description="List of generated queries for each component.")
    statistics: Statistics = Field(..., description="Statistics about the extracted components.")
    formatted_results: str = Field(..., description="A string containing all component queries formatted for display", example="-- Component 1: UserCTE (cte)\nSELECT * FROM UserCTE;\n...")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status of the API", example="healthy")
    timestamp: str = Field(..., description="Current server timestamp in ISO format", example="2023-10-27T10:00:00Z")
    version: str = Field(..., description="API version", example="1.0.0")

# Pydantic models for routes that don't have explicit response models yet

class ValidateSqlResponse(BaseModel):
    valid: bool = Field(..., description="Whether the SQL syntax is considered valid.", example=True)
    message: Optional[str] = Field(None, description="Validation message or error details.", example="SQL query appears to be valid")
    cleaned_length: Optional[int] = Field(None, description="Length of the SQL query after removing comments.", example=150)
    error: Optional[str] = Field(None, description="Error message if validation fails.", example=None)

class UploadSqlResponse(BaseModel):
    filename: str = Field(..., description="Name of the uploaded file.", example="my_query.sql")
    size: int = Field(..., description="Size of the uploaded file in bytes.", example=1024)
    content: str = Field(..., description="Content of the uploaded SQL file.", example="SELECT * FROM users;")
    lines: int = Field(..., description="Number of lines in the uploaded SQL file.", example=10)

class ExampleQuery(BaseModel):
    name: str = Field(..., description="Name of the example query.", example="CTE Example")
    description: str = Field(..., description="Description of the example query.", example="Simple CTE with recursive structure")
    sql: str = Field(..., description="The example SQL query string.", example="WITH cte AS (SELECT 1) SELECT * FROM cte;")

class ExampleQueriesResponse(BaseModel):
    examples: List[ExampleQuery] = Field(..., description="A list of example SQL queries.")

class SupportedComponent(BaseModel):
    type: str = Field(..., description="Type identifier of the supported component.", example="cte")
    name: str = Field(..., description="Human-readable name of the component.", example="Common Table Expressions")
    description: str = Field(..., description="Detailed description of the component.", example="WITH clauses and named result sets")

class ParserStatisticsResponse(BaseModel):
    supported_components: List[SupportedComponent] = Field(..., description="List of SQL components supported by the parser.")
    parser_features: List[str] = Field(..., description="List of features supported by the parser.", example=["Comment removal (-- and /* */)", "Balanced parentheses matching"])


# Helper functions
def calculate_statistics(components: List[Dict[str, Any]]) -> Statistics:
    """Calculate statistics from components"""
    breakdown = {}
    for component in components:
        comp_type = component.get('type', 'unknown')
        breakdown[comp_type] = breakdown.get(comp_type, 0) + 1
    
    return Statistics(
        total=len(components),
        breakdown=breakdown
    )

def format_results_for_display(queries: List[Dict[str, Any]]) -> str:
    """Format queries for display in the frontend"""
    if not queries:
        return "No components found in the SQL query."
    
    formatted_lines = []
    
    for i, query in enumerate(queries, 1):
        comp_type = query.get('type', 'unknown').replace('_', ' ').title()
        header = f"-- ========== Component {i}: {query['name']} ({comp_type}) ========== --"
        formatted_lines.append(header)
        formatted_lines.append("")
        formatted_lines.append(query['query'])
        formatted_lines.append("")
        formatted_lines.append("=" * 80)
        formatted_lines.append("")
    
    return "\n".join(formatted_lines)

# API Routes

@app.get(
    "/",
    response_model=HealthResponse,
    summary="Root Health Check",
    description="Provides a basic health check for the API. Returns the current status, timestamp, and API version."
)
async def root():
    """Root endpoint - API health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Detailed Health Check",
    description="Provides a detailed health check for the API, similar to the root endpoint. Returns the current status, timestamp, and API version."
)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post(
    "/api/sql/process",
    response_model=SqlProcessResponse,
    summary="Process SQL Query",
    description="Analyzes the provided SQL query string, extracts various components like CTEs, temporary tables, and table variables. It also generates individual queries for each component and provides statistics."
)
async def process_sql(request: SqlProcessRequest):
    """
    Process SQL query and extract components
    
    Args:
        request: SQL processing request containing the query and options
        
    Returns:
        Processed components, generated queries, and statistics
    """
    try:
        logger.info(f"Processing SQL query of length {len(request.sql_query)}")
        
        if not request.sql_query.strip():
            error_message = "SQL query cannot be empty"
            logger.warning(f"{error_message} (request: {request})")
            return SqlProcessResponse(
                success=False,
                message=error_message,
                components=[],
                queries=[],
                statistics=Statistics(total=0, breakdown={}),
                formatted_results=f"Error: {error_message}"
            )
        
        # Extract components using the SQL parser
        raw_components = extract_components(
            request.sql_query, 
            include_subqueries=request.include_subqueries
        )
        
        # Convert to Pydantic models
        components = []
        for comp in raw_components:
            components.append(Component(
                type=comp.get('type', 'unknown'),
                name=comp.get('name', 'unnamed'),
                position=comp.get('position'),
                content=comp.get('content'),
                declaration=comp.get('declaration')
            ))
        
        # Generate queries
        raw_queries = generate_component_queries(raw_components)
        queries = []
        for query in raw_queries:
            queries.append(Query(
                name=query.get('name', 'unnamed'),
                query=query.get('query', ''),
                type=query.get('type', 'unknown')
            ))
        
        # Calculate statistics
        statistics = calculate_statistics(raw_components)
        
        # Format results for display
        formatted_results = format_results_for_display(raw_queries)
        
        logger.info(f"Successfully processed SQL. Found {len(components)} components.")
        
        return SqlProcessResponse(
            success=True,
            message=f"Successfully processed SQL query. Found {len(components)} components.",
            components=components,
            queries=queries,
            statistics=statistics,
            formatted_results=formatted_results
        )
        
    except Exception as e:
        logger.error(f"Error processing SQL: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Return error response but don't raise HTTPException for better UX
        return SqlProcessResponse(
            success=False,
            message=f"Error processing SQL: {str(e)}",
            components=[],
            queries=[],
            statistics=Statistics(total=0, breakdown={}),
            formatted_results=f"Error: {str(e)}"
        )

@app.post(
    "/api/sql/validate",
    response_model=ValidateSqlResponse,
    summary="Validate SQL Syntax",
    description="Performs a basic syntax validation of the provided SQL query. This includes checking for empty queries, removing comments, and ensuring the query is not excessively short. It does not perform full parsing or execution."
)
async def validate_sql(request: SqlProcessRequest):
    """
    Validate SQL syntax without full processing
    
    Args:
        request: SQL validation request
        
    Returns:
        Validation result
    """
    try:
        if not request.sql_query.strip():
            return ValidateSqlResponse(valid=False, error="SQL query cannot be empty")
        
        # Basic validation - remove comments and check for basic structure
        clean_sql = remove_comments(request.sql_query)
        
        # Very basic validation
        if len(clean_sql.strip()) < 5:
            return ValidateSqlResponse(valid=False, error="SQL query appears to be too short")
        
        return ValidateSqlResponse(
            valid=True,
            message="SQL query appears to be valid",
            cleaned_length=len(clean_sql)
        )
        
    except Exception as e:
        logger.error(f"Error validating SQL: {str(e)}")
        return ValidateSqlResponse(valid=False, error=str(e))

@app.post(
    "/api/sql/upload",
    response_model=UploadSqlResponse,
    summary="Upload SQL File",
    description="Allows uploading an SQL file (or a .txt file containing SQL). The file content is read, and basic information like filename, size, and line count is returned. The SQL content itself is also returned."
)
async def upload_sql_file(file: UploadFile = File(...)):
    """
    Upload and process SQL file
    
    Args:
        file: Uploaded SQL file
        
    Returns:
        File content and basic info
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.sql', '.txt')):
            raise HTTPException(
                status_code=400, 
                detail="Only .sql and .txt files are allowed"
            )
        
        # Read file content
        content = await file.read()
        sql_content = content.decode('utf-8')
        
        # Basic file info
        file_info = UploadSqlResponse(
            filename=file.filename,
            size=len(content),
            content=sql_content,
            lines=len(sql_content.splitlines())
        )
        
        logger.info(f"Uploaded file: {file.filename}, size: {len(content)} bytes")
        
        return file_info
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
    except HTTPException as http_exc: # Re-raise HTTPExceptions directly
        raise http_exc
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get(
    "/api/sql/examples",
    response_model=ExampleQueriesResponse,
    summary="Get Example SQL Queries",
    description="Provides a list of predefined SQL query examples that can be used for testing the SQL processing and validation functionalities. Each example includes a name, description, and the SQL query string."
)
async def get_example_queries():
    """
    Get example SQL queries for testing
    
    Returns:
        List of example SQL queries
    """
    examples_data = [
        {
            "name": "CTE Example",
            "description": "Simple CTE with recursive structure",
            "sql": """WITH CustomerOrders AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        COUNT(o.order_id) as order_count
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT * FROM CustomerOrders
WHERE order_count > 5;"""
        },
        {
            "name": "Table Variable Example", 
            "description": "Table variable declaration and usage",
            "sql": """DECLARE @TempResults TABLE (
    ID INT IDENTITY(1,1),
    CustomerName NVARCHAR(100),
    TotalAmount DECIMAL(10,2)
);

INSERT INTO @TempResults (CustomerName, TotalAmount)
SELECT c.customer_name, SUM(o.total_amount)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name;

SELECT * FROM @TempResults;"""
        },
        {
            "name": "Temp Table Example",
            "description": "Temporary table creation and SELECT INTO",
            "sql": """CREATE TABLE #MonthlyStats (
    Month INT,
    Year INT,
    TotalSales DECIMAL(12,2),
    OrderCount INT
);

SELECT 
    MONTH(order_date) as Month,
    YEAR(order_date) as Year,
    SUM(total_amount) as TotalSales,
    COUNT(*) as OrderCount
INTO #DailySummary
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY YEAR(order_date), MONTH(order_date);

SELECT * FROM #DailySummary;"""
        }
    ]
    return ExampleQueriesResponse(examples=[ExampleQuery(**ex) for ex in examples_data])

@app.get(
    "/api/sql/statistics",
    response_model=ParserStatisticsResponse,
    summary="Get Parser Statistics",
    description="Returns information about the SQL parser's capabilities, including a list of supported SQL component types (like CTEs, temp tables) and a list of general parser features (like comment removal, position tracking)."
)
async def get_parser_statistics():
    """
    Get parser statistics and supported component types
    
    Returns:
        Parser capabilities and statistics
    """
    supported_components_data = [
        {
            "type": "cte",
            "name": "Common Table Expressions",
            "description": "WITH clauses and named result sets"
        },
        {
            "type": "table_variable_block",
            "name": "Table Variables",
            "description": "DECLARE @var TABLE declarations"
        },
        {
            "type": "temp_table_create",
            "name": "Temporary Tables",
            "description": "CREATE TABLE #temp statements"
        },
        {
            "type": "temp_table_select_into",
            "name": "SELECT INTO",
            "description": "SELECT INTO #temp statements"
        },
        {
            "type": "subquery",
            "name": "Subqueries",
            "description": "Nested queries and sub-selects"
        }
    ]
    parser_features_data = [
        "Comment removal (-- and /* */)",
        "Balanced parentheses matching",
        "String literal handling",
        "Nested CTE detection",
        "Position tracking"
    ]
    return ParserStatisticsResponse(
        supported_components=[SupportedComponent(**sc) for sc in supported_components_data],
        parser_features=parser_features_data
    )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "detail": str(exc)}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "Please check the logs"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
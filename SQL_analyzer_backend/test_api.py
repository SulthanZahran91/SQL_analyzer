import unittest
import json
from fastapi.testclient import TestClient
from main import app # Assuming your FastAPI app instance is named 'app' in main.py
import io

class TestApiEndpoints(unittest.TestCase):

    def setUp(self):
        """Set up the test client before each test."""
        self.client = TestClient(app)

    def test_01_health_check_root(self):
        """Test the root health check endpoint /."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("timestamp", data)
        self.assertEqual(data["version"], "1.0.0")

    def test_02_health_check_health(self):
        """Test the /health health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("timestamp", data)
        self.assertEqual(data["version"], "1.0.0")

    def test_03_process_sql_valid_query(self):
        """Test POST /api/sql/process with a valid SQL query."""
        payload = {"sql_query": "SELECT * FROM Users;"}
        response = self.client.post("/api/sql/process", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("Successfully processed SQL query", data["message"])
        self.assertIn("components", data)
        self.assertIn("queries", data)
        self.assertIn("statistics", data)
        self.assertIn("formatted_results", data)
        # Depending on your parser, you might want to assert specific component counts for a known query

    def test_04_process_sql_empty_query(self):
        """Test POST /api/sql/process with an empty SQL query."""
        payload = {"sql_query": "  "}
        response = self.client.post("/api/sql/process", json=payload)
        # The current implementation returns 200 with success=False for better UX
        self.assertEqual(response.status_code, 200) 
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("SQL query cannot be empty", data["message"]) 

    def test_05_process_sql_with_subqueries_option(self):
        """Test POST /api/sql/process with include_subqueries=true."""
        sql_with_subquery = "WITH cte AS (SELECT id FROM (SELECT id FROM table1) s) SELECT * FROM cte;"
        payload = {"sql_query": sql_with_subquery, "include_subqueries": True}
        response = self.client.post("/api/sql/process", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        # Add more specific assertions based on expected subquery component extraction

    def test_06_validate_sql_valid_query(self):
        """Test POST /api/sql/validate with a valid SQL query."""
        payload = {"sql_query": "SELECT column FROM AnotherTable;"}
        response = self.client.post("/api/sql/validate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["valid"])
        self.assertEqual(data["message"], "SQL query appears to be valid")

    def test_07_validate_sql_empty_query(self):
        """Test POST /api/sql/validate with an empty SQL query."""
        payload = {"sql_query": ""}
        response = self.client.post("/api/sql/validate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["valid"])
        self.assertEqual(data["error"], "SQL query cannot be empty")

    def test_08_validate_sql_too_short(self):
        """Test POST /api/sql/validate with a very short (likely invalid) query."""
        payload = {"sql_query": "abc"}
        response = self.client.post("/api/sql/validate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["valid"])
        self.assertEqual(data["error"], "SQL query appears to be too short")

    def test_09_upload_sql_file_valid_sql(self):
        """Test POST /api/sql/upload with a valid .sql file."""
        sql_content = "SELECT * FROM TestUpload;\n-- Another line"
        file_content = io.BytesIO(sql_content.encode('utf-8'))
        files = {'file': ('test.sql', file_content, 'text/plain')}
        response = self.client.post("/api/sql/upload", files=files)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["filename"], "test.sql")
        self.assertEqual(data["content"], sql_content)
        self.assertGreater(data["size"], 0)
        self.assertEqual(data["lines"], 2)

    def test_10_upload_sql_file_valid_txt(self):
        """Test POST /api/sql/upload with a valid .txt file."""
        sql_content = "DECLARE @Var INT;"
        file_content = io.BytesIO(sql_content.encode('utf-8'))
        files = {'file': ('test.txt', file_content, 'text/plain')}
        response = self.client.post("/api/sql/upload", files=files)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["filename"], "test.txt")
        self.assertEqual(data["content"], sql_content)

    def test_11_upload_sql_file_invalid_type(self):
        """Test POST /api/sql/upload with an invalid file type (e.g., .zip)."""
        file_content = io.BytesIO(b"PKZIP archive data")
        files = {'file': ('test.zip', file_content, 'application/zip')}
        response = self.client.post("/api/sql/upload", files=files)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "Only .sql and .txt files are allowed")

    def test_12_upload_sql_file_invalid_content_not_utf8(self):
        """Test POST /api/sql/upload with a non-UTF-8 encoded file."""
        # ISO-8859-1 (Latin-1) content that will fail UTF-8 decoding
        invalid_content = b"SELECT caf\xe9;"
        file_content = io.BytesIO(invalid_content)
        files = {'file': ('test_bad_encoding.sql', file_content, 'text/plain')}
        response = self.client.post("/api/sql/upload", files=files)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "File must be valid UTF-8 text")

    def test_13_get_example_queries(self):
        """Test GET /api/sql/examples."""
        response = self.client.get("/api/sql/examples")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("examples", data)
        self.assertIsInstance(data["examples"], list)
        self.assertGreater(len(data["examples"]), 0)
        for example in data["examples"]:
            self.assertIn("name", example)
            self.assertIn("sql", example)

    def test_14_get_parser_statistics(self):
        """Test GET /api/sql/statistics."""
        response = self.client.get("/api/sql/statistics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("supported_components", data)
        self.assertIsInstance(data["supported_components"], list)
        self.assertGreater(len(data["supported_components"]), 0)
        self.assertIn("parser_features", data)
        self.assertIsInstance(data["parser_features"], list)

    def test_15_not_found_endpoint(self):
        """Test a non-existent endpoint to ensure 404 handling."""
        response = self.client.get("/api/non_existent_path")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["error"], "Endpoint not found")

if __name__ == '__main__':
    unittest.main() 
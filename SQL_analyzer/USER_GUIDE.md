# SQL Query Analyzer - User Guide

## Introduction

Welcome to the SQL Query Analyzer! This tool is designed to help you understand the structure of your SQL queries by breaking them down into their core components. It can identify Common Table Expressions (CTEs), temporary tables, table variables, and subqueries, providing insights into how your SQL code is organized and executed.

This guide will walk you through the features of the frontend application and how to use them effectively.

## Getting Started

To begin analyzing an SQL query, you have two main options:

1.  **Direct Input**: Type or paste your SQL query directly into the designated text area.
2.  **File Upload**: Upload a file containing your SQL query.

These actions are typically performed in the "SQL Input" or a similarly named section of the application.

## Understanding the Interface

The application is generally organized into several tabs or sections to manage input, view results, and see additional information.

### SQL Input Tab

This is where you provide the SQL query you want to analyze.

*   **Entering SQL Queries Directly**:
    *   Locate the main text area, often labeled "Enter SQL Query" or similar.
    *   You can type your SQL query here or paste it from your clipboard.
    *   Once your query is entered, look for a button like "Analyze", "Process SQL", or "Submit" to start the analysis.

*   **Using the File Upload Feature**:
    *   Find the "Upload SQL File" button or drag-and-drop area.
    *   Click the button to browse for a file on your computer or drag a file onto the designated area.
    *   The application typically accepts files with `.sql` or `.txt` extensions.
    *   After uploading, the content of the file will usually populate the SQL input area, or the analysis might start automatically.

*   **"Include Subqueries" Option**:
    *   You may see a checkbox or toggle labeled "Include Subqueries" or "Extract Subqueries".
    *   **Checked/Enabled**: The analyzer will attempt to identify and extract subqueries (queries nested within other queries) as separate components. This provides a more granular breakdown but can result in a larger number of components.
    *   **Unchecked/Disabled**: Subqueries will be treated as part of their parent component and not extracted individually.

### Results Tab

After processing your query, the results are typically displayed in this tab. It usually contains two main parts:

*   **Extracted Components and Generated Queries**:
    *   This section lists each identified component (e.g., CTE, Temp Table) with its name and type.
    *   For each component, the analyzer often generates an individual, executable SQL query. This helps you isolate and test parts of your larger script.
    *   Components might be displayed in a list, table, or as expandable sections.

*   **Formatted Results / Main Query View**:
    *   This area usually shows a consolidated view of all the generated component queries, often formatted with comments to delineate each component.
    *   The formatting aims to make it easy to read and understand the structure of the original query by seeing each part clearly separated. For example:
        ```sql
        -- ========== Component 1: MyCTE (Common Table Expression) ========== --

        WITH MyCTE AS (
          SELECT id, name FROM source_table
        )
        SELECT * FROM MyCTE;

        -- ================================================================================ --

        -- ========== Component 2: TempResults (Temporary Table) ========== --

        CREATE TABLE #TempResults (
          data_value VARCHAR(100)
        );
        INSERT INTO #TempResults (data_value) VALUES ('Example');
        SELECT * FROM #TempResults;

        -- ================================================================================ --
        ```
    *   This view is useful for getting an overview of all extracted parts in sequence.

### Statistics Tab

This tab provides a quantitative summary of the components extracted from your SQL query.

*   **Total Components**: Shows the total number of individual SQL components identified in your query.
*   **Breakdown by Type**: Displays a count for each type of component found (e.g., CTEs: 2, Temporary Tables: 1, Table Variables: 0). This helps you quickly see the kinds of structures present in your SQL.

### Debug Log Tab

The Debug Log tab is primarily for advanced users or for troubleshooting purposes.

*   **Purpose**: It may display detailed logging information from the backend about the parsing process, including any warnings or errors encountered internally.
*   If you encounter unexpected behavior, the information in this tab might be helpful for diagnosing the issue, or you might be asked to provide it if seeking support.

## Tips for Use

*   **Start Simple**: If you're new to the tool, start with smaller, less complex queries to get a feel for how it works.
*   **Iterate**: For very large and complex SQL scripts, consider analyzing smaller sections if the overall output is overwhelming.
*   **Use Component Queries**: The individual queries generated for each component can be very useful for testing or understanding specific parts of your script in isolation.
*   **Check Statistics**: The statistics tab can give you a quick overview of the complexity and types of structures in your query.

## Troubleshooting

*   **Query Not Processing**:
    *   Ensure your SQL syntax is valid. While the analyzer tries to be robust, significant syntax errors can prevent processing.
    *   Check for very large queries; there might be practical limits on query size depending on the deployment.
    *   Look for any error messages displayed in the UI or in the Debug Log tab.

*   **File Upload Issues**:
    *   Make sure your file is a plain text file (`.sql` or `.txt`). Binary files or other formats will not work.
    *   Ensure the file is not empty.

*   **Unexpected Component Breakdown**:
    *   The SQL parsing logic has certain rules for identifying components. If the breakdown isn't what you expect, review your SQL structure. The parser looks for common patterns like `WITH ... AS`, `CREATE TABLE #...`, `DECLARE @... TABLE`.
    *   If you believe there's an issue with the parsing itself, note the specific SQL and the unexpected output. The Debug Log might contain clues.

*   **Browser Issues**:
    *   Try clearing your browser cache or using an incognito/private window to rule out issues with cached data or browser extensions.
    *   Ensure you are using a modern, up-to-date web browser.

If you continue to experience issues, check if there's a support or feedback mechanism associated with the SQL Analyzer application.
---
This guide provides a general overview. Specific labels and layout may vary slightly in the actual application.

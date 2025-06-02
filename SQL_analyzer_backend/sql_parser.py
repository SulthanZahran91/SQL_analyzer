#!/usr/bin/env python3
"""
SQL Parser Module
Extracts components from SQL Server queries including CTEs, table variables, temp tables, and subqueries.
Uses a hybrid approach combining sqlparse tokenization with custom parsing logic.
"""

import re
import logging
import sqlparse
from typing import List, Dict, Any, Optional, Tuple, Set
from collections import OrderedDict
import uuid

# Configure logging
logger = logging.getLogger(__name__)


def remove_comments(sql: str) -> str:
    """
    Remove SQL comments while preserving string literals.
    Handles both single-line (--) and multi-line (/* */) comments.
    
    Args:
        sql: SQL string potentially containing comments
        
    Returns:
        SQL string with comments removed
    """
    result = []
    i = 0
    
    while i < len(sql):
        # Check for string literal
        if sql[i] == "'":
            # Find the end of the string literal
            j = i + 1
            while j < len(sql):
                if sql[j] == "'":
                    if j + 1 < len(sql) and sql[j + 1] == "'":
                        # Escaped quote
                        j += 2
                    else:
                        # End of string
                        j += 1
                        break
                else:
                    j += 1
            result.append(sql[i:j])
            i = j
            
        # Check for single-line comment
        elif i + 1 < len(sql) and sql[i:i+2] == '--':
            # Skip until end of line
            while i < len(sql) and sql[i] not in '\n\r':
                i += 1
            if i < len(sql):
                result.append(sql[i])  # Keep the newline
                i += 1
                
        # Check for multi-line comment
        elif i + 1 < len(sql) and sql[i:i+2] == '/*':
            # Skip until */
            i += 2
            while i + 1 < len(sql):
                if sql[i:i+2] == '*/':
                    i += 2
                    break
                i += 1
            result.append(' ')  # Replace with space to preserve word boundaries
            
        else:
            result.append(sql[i])
            i += 1
    
    return ''.join(result)


def find_balanced_parentheses(text: str, start_pos: int) -> int:
    """
    Find the position of the closing parenthesis that matches the opening parenthesis at start_pos.
    
    Args:
        text: The text to search in
        start_pos: Position of the opening parenthesis
        
    Returns:
        Position of the matching closing parenthesis, or -1 if not found
    """
    if start_pos >= len(text) or text[start_pos] != '(':
        return -1
    
    depth = 0
    i = start_pos
    
    while i < len(text):
        char = text[i]
        
        # Handle string literals
        if char == "'":
            i += 1
            while i < len(text):
                if text[i] == "'":
                    if i + 1 < len(text) and text[i + 1] == "'":
                        i += 2  # Skip escaped quote
                    else:
                        i += 1
                        break
                else:
                    i += 1
            continue
        
        # Handle comments
        if i + 1 < len(text):
            if text[i:i+2] == '--':
                # Skip to end of line
                while i < len(text) and text[i] != '\n':
                    i += 1
                i += 1
                continue
            elif text[i:i+2] == '/*':
                # Skip to */
                i += 2
                while i + 1 < len(text) and text[i:i+2] != '*/':
                    i += 1
                i += 2
                continue
            
        # Handle parentheses
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0:
                return i
                
        i += 1
    
    return -1


def is_valid_table_variable_declaration(sql: str, start_pos: int) -> bool:
    """
    Check if a table variable declaration is valid (has proper closing parenthesis).
    
    Args:
        sql: The SQL string
        start_pos: Position after the TABLE keyword
        
    Returns:
        True if the declaration is valid, False otherwise
    """
    # Find the opening parenthesis
    paren_pos = sql.find('(', start_pos)
    if paren_pos == -1:
        return False
    
    # Check if there's a matching closing parenthesis
    close_paren = find_balanced_parentheses(sql, paren_pos)
    return close_paren != -1


def parse_cte_definitions(sql: str, start_pos: int, parsing_issues: List[Dict[str, Any]], nested: bool = False) -> List[Dict[str, Any]]:
    """
    Parse CTE definitions starting from a WITH keyword.
    
    Args:
        sql: The SQL string
        start_pos: Position after the WITH keyword
        parsing_issues: List to store parsing issues
        nested: Whether this is a nested CTE (inside a subquery)
        
    Returns:
        List of CTE components
    """
    ctes = []
    pos = start_pos
    
    # Skip whitespace
    while pos < len(sql) and sql[pos].isspace():
        pos += 1
    
    while pos < len(sql):
        # Extract CTE name
        name_match = re.match(r'(\w+)\s*AS\s*\(', sql[pos:], re.IGNORECASE | re.DOTALL)
        if not name_match:
            break
            
        cte_name = name_match.group(1)
        name_end = pos + name_match.end() - 1  # Position of opening parenthesis
        
        # Find the matching closing parenthesis
        close_paren = find_balanced_parentheses(sql, name_end)
        if close_paren == -1:
            parsing_issues.append({
                'type': 'warning',
                'message': f"Could not find closing parenthesis for CTE {cte_name}",
                'component_name': cte_name,
                'position': name_end
            })
            logger.warning(f"Could not find closing parenthesis for CTE {cte_name}")
            break
            
        # Extract the CTE content
        cte_content = sql[name_end + 1:close_paren]
        
        # Don't add nested CTEs as regular CTEs
        if not nested:
            ctes.append({
                'type': 'cte',
                'name': cte_name,
                'position': pos,
                'content': cte_content
            })
            
            logger.info(f"Found CTE: {cte_name} at position {pos}")
        
        # Move past the closing parenthesis
        pos = close_paren + 1
        
        # Skip whitespace
        while pos < len(sql) and sql[pos].isspace():
            pos += 1
            
        # Check for comma (more CTEs)
        if pos < len(sql) and sql[pos] == ',':
            pos += 1
            while pos < len(sql) and sql[pos].isspace():
                pos += 1
        else:
            # No more CTEs
            break
    
    return ctes


def extract_components(sql: str, include_subqueries: bool = False) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Extract SQL components from a SQL string.
    
    Args:
        sql: SQL string to parse
        include_subqueries: Whether to include subquery extraction
        
    Returns:
        A tuple containing:
            - List of components, each with 'type', 'name', and other attributes
            - List of parsing issues encountered
    """
    logger.info("SQLPARSE_V3_IMPL_FIX_IDENTIFIERLIST: Starting component extraction...")
    
    parsing_issues = []

    # Remove comments first
    clean_sql = remove_comments(sql)
    
    components = []
    
    # Use regex to find all components
    
    # 1. Extract table variables with full declaration
    table_var_pattern = r'DECLARE\s+(@\w+)\s+TABLE\s*\('
    for match in re.finditer(table_var_pattern, clean_sql, re.IGNORECASE):
        var_name = match.group(1)
        position = match.start()
        
        # Find the opening parenthesis position
        paren_pos = match.end() - 1
        
        # Check if this is a valid declaration and find closing parenthesis
        close_paren = find_balanced_parentheses(clean_sql, paren_pos)
        if close_paren != -1:
            # Extract the full declaration including the closing parenthesis
            full_declaration = clean_sql[position:close_paren + 1]
            
            components.append({
                'type': 'table_variable_block',
                'name': var_name,
                'position': position,
                'declaration': full_declaration
            })
            logger.info(f"SQLPARSE_V3_IMPL_FIX_IDENTIFIERLIST: Found Table Variable: {var_name} @ ~{position}")
    
    # 2. Extract CTEs
    # Find all WITH clauses that are not inside parentheses (not nested)
    with_pattern = r'\bWITH\s+'
    for match in re.finditer(with_pattern, clean_sql, re.IGNORECASE):
        # Check if this WITH is inside parentheses (nested)
        before_with = clean_sql[:match.start()]
        open_parens = before_with.count('(')
        close_parens = before_with.count(')')
        
        if open_parens > close_parens:
            # This is a nested WITH, skip it for regular CTE extraction
            continue
            
        cte_components = parse_cte_definitions(clean_sql, match.end(), parsing_issues)
        components.extend(cte_components)
    
    # 3. Extract CREATE TABLE for temp tables with full declaration
    create_temp_pattern = r'(CREATE\s+TABLE\s+(#\w+)\s*\([^)]*\))'
    for match in re.finditer(create_temp_pattern, clean_sql, re.IGNORECASE | re.DOTALL):
        full_declaration = match.group(1)
        table_name = match.group(2)
        position = match.start()
        
        # Find the matching closing parenthesis for the CREATE TABLE
        paren_start = match.group(0).find('(') + match.start()
        close_paren = find_balanced_parentheses(clean_sql, paren_start)
        if close_paren != -1:
            full_declaration = clean_sql[position:close_paren + 1]
        
        components.append({
            'type': 'temp_table_create',
            'name': table_name,
            'position': position,
            'declaration': full_declaration
        })
        logger.info(f"SQLPARSE_V3_IMPL_FIX_IDENTIFIERLIST: Found Temp Table Create: {table_name} @ ~{position}")
    
    # 4. Extract SELECT INTO for temp tables
    # Need to ensure we're matching SELECT INTO, not INSERT INTO
    # Look for pattern where INTO is preceded by SELECT (with possible columns/expressions between)
    select_into_pattern = r'SELECT\s+(?:.*?)\s+INTO\s+(#\w+)'
    for match in re.finditer(select_into_pattern, clean_sql, re.IGNORECASE | re.DOTALL):
        table_name = match.group(1)
        # Find the position of INTO keyword
        into_pos = match.start() + match.group(0).rfind('INTO')
        position = into_pos
        components.append({
            'type': 'temp_table_select_into',
            'name': table_name,
            'position': position
        })
        logger.info(f"SQLPARSE_V3_IMPL_FIX_IDENTIFIERLIST: Found SelectInto: {table_name} @ ~{position}")
    
    # 5. Extract subqueries if requested
    if include_subqueries:
        # Look for WITH...AS within parentheses (nested CTEs in subqueries)
        nested_cte_pattern = r'\(\s*WITH\s+(\w+)\s+AS'
        for match in re.finditer(nested_cte_pattern, clean_sql, re.IGNORECASE):
            cte_name = match.group(1)
            position = match.start()
            
            # Add as subquery
            components.append({
                'type': 'subquery',
                'name': f"Level3_{cte_name}",
                'position': position
            })
            
            # Parse the nested CTE but don't add it as a regular CTE
            # We already have the logic to skip nested CTEs in parse_cte_definitions
    
    # Sort by position for consistent ordering
    components.sort(key=lambda x: x.get('position', 0))
    
    logger.info(f"SQLPARSE_V3_IMPL_FIX_IDENTIFIERLIST: Total components extracted: {len(components)}")
    logger.debug(f"SQLPARSE_V3_IMPL_FIX_IDENTIFIERLIST: Final Components: {components}")
    
    return components, parsing_issues


def generate_component_queries(components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate executable queries from extracted components.
    
    Args:
        components: List of component dictionaries
        
    Returns:
        List of query dictionaries with 'name' and 'query' fields
    """
    logger.info("GEN_QUERIES_SQLPARSE_V3_FIX_IDENTIFIERLIST: Starting query generation...")
    
    queries = []
    
    for component in components:
        comp_type = component.get('type')
        comp_name = component.get('name')
        
        if not comp_type or not comp_name:
            continue
            
        query = None
        
        if comp_type == 'cte':
            # Generate a SELECT from the CTE
            query = f"WITH {comp_name} AS ({component.get('content', 'SELECT 1')}) SELECT * FROM {comp_name};"
            
        elif comp_type == 'table_variable_block':
            # Generate a query with the full declaration followed by SELECT
            declaration = component.get('declaration', f'DECLARE {comp_name} TABLE (ID INT)')
            query = f"{declaration};\nSELECT * FROM {comp_name};"
            
        elif comp_type in ['temp_table_create', 'temp_table_select_into']:
            # For CREATE TABLE, include the declaration if available
            if comp_type == 'temp_table_create' and 'declaration' in component:
                declaration = component.get('declaration')
                query = f"{declaration};\nSELECT * FROM {comp_name};"
            else:
                # For SELECT INTO, we can't recreate the table easily, just select from it
                query = f"-- Note: {comp_name} was created via SELECT INTO\nSELECT * FROM {comp_name};"
            
        elif comp_type == 'subquery':
            # For subqueries, just note them
            query = f"-- Subquery: {comp_name}"
            
        if query:
            queries.append({
                'name': comp_name,
                'query': query,
                'type': comp_type  # Include type in the output
            })
    
    logger.info(f"GenQueries: Generated {len(queries)} queries.")
    
    return queries
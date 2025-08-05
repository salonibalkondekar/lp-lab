"""Gemini-based LP problem formulator"""

import os
import json
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from google import genai

from .prompts import SYSTEM_PROMPT, EXAMPLE_PROBLEMS
from ..config import (
    GEMINI_MODEL,
    GEMINI_API_KEY,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_TOKENS,
)
from ..utils.logger import get_logger

# Get logger for this module
logger = get_logger("ai.formulator")


# Pydantic models for structured output
class LPFormulation(BaseModel):
    """Linear Programming formulation structure"""
    variables: List[str] = Field(description="List of decision variable names")
    variable_descriptions: Dict[str, str] = Field(description="Description of each variable")
    objective_type: str = Field(description="Either 'maximize' or 'minimize'", pattern="^(maximize|minimize)$")
    objective_function: str = Field(description="The objective function expression (without Max/Min prefix)")
    constraints: List[str] = Field(description="List of constraint expressions")
    constraint_descriptions: Dict[str, str] = Field(description="Description of each constraint")
    explanation: str = Field(description="Brief explanation of the formulation")


class LPFormulator:
    """Convert natural language problems to LP format using Gemini"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini client with API key"""
        # Allow override from parameter, environment, or use config default
        self.api_key = (
            api_key 
            or os.getenv("GEMINI_API_KEY") 
            or os.getenv("GOOGLE_API_KEY")
            or GEMINI_API_KEY
        )
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY or GOOGLE_API_KEY environment variable."
            )

        # Initialize client with API key
        self.client = genai.Client(api_key=self.api_key)
        self.model = GEMINI_MODEL

    def formulate_problem(self, problem_description: str) -> Dict:
        """
        Convert natural language problem description to LP format
        
        Args:
            problem_description: Natural language description of the problem
            
        Returns:
            Dictionary with LP formulation or error information
        """
        try:
            logger.info("Starting problem formulation")
            logger.debug(f"Problem description length: {len(problem_description)} chars")
            
            # Build the prompt
            prompt = self._build_prompt(problem_description)
            logger.debug(f"Built prompt with length: {len(prompt)} chars")
            
            # Generate content - use simple JSON format
            json_structure = {
                "variables": ["x1", "x2"],
                "variable_descriptions": {"x1": "...", "x2": "..."},
                "objective_type": "maximize or minimize",
                "objective_function": "objective expression without Max/Min prefix",
                "constraints": ["constraint1", "constraint2"],
                "constraint_descriptions": {"constraint1": "...", "constraint2": "..."},
                "explanation": "brief explanation"
            }
            
            json_prompt = prompt + "\n\nReturn the formulation as a JSON object with this structure:\n" + json.dumps(json_structure, indent=2)
            logger.debug(f"Full prompt length: {len(json_prompt)} chars")
            
            logger.info(f"Calling Gemini API with model: {self.model}")
            response = self.client.models.generate_content(
                model=self.model,
                contents=json_prompt,
                config={
                    "temperature": GEMINI_TEMPERATURE,
                    "top_p": 0.95,
                    "max_output_tokens": GEMINI_MAX_TOKENS,
                }
            )
            logger.info("Received response from Gemini API")
            
            # Parse the response
            # Extract JSON from the response text
            response_text = response.text.strip()
            logger.debug(f"Response text length: {len(response_text)} chars")
            
            # Find JSON content (might be wrapped in markdown code blocks)
            if '```json' in response_text:
                logger.debug("Found JSON in markdown code block")
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                json_text = response_text[start:end].strip()
            elif '{' in response_text:
                logger.debug("Found raw JSON object")
                # Find the JSON object
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_text = response_text[start:end]
            else:
                logger.debug("Using entire response as JSON")
                json_text = response_text
            
            logger.debug(f"Attempting to parse JSON of length: {len(json_text)} chars")
            result_dict = json.loads(json_text)
            logger.info("Successfully parsed JSON response")
            
            # Convert to our expected format
            formatted_result = self._format_result(result_dict)
            logger.info(f"Formulation successful: {formatted_result.get('success', False)}")
            
            return formatted_result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.debug(f"Failed to parse: {json_text[:200] if 'json_text' in locals() else 'N/A'}...")
            return {
                "error": f"Failed to parse AI response as JSON: {str(e)}",
                "success": False
            }
        except Exception as e:
            logger.error(f"Formulation error: {e}", exc_info=True)
            return {
                "error": f"Failed to formulate problem: {str(e)}",
                "success": False
            }
    
    def _build_prompt(self, problem_description: str) -> str:
        """Build the prompt with system instructions and examples"""
        # Create prompt content
        prompt = f"""{SYSTEM_PROMPT}

Here are some examples:

Example 1:
Problem: {EXAMPLE_PROBLEMS[0]['description']}

Formulation: {EXAMPLE_PROBLEMS[0]['formulation']}

Example 2:
Problem: {EXAMPLE_PROBLEMS[1]['description']}

Formulation: {EXAMPLE_PROBLEMS[1]['formulation']}

Now formulate this problem:

{problem_description}"""
        
        return prompt
    
    def _format_result(self, result: Dict) -> Dict:
        """Format the Gemini result for our application"""
        try:
            # Build objective string
            obj_type = result.get("objective_type", "maximize").capitalize()
            objective = f"{obj_type} Z = {result['objective_function']}"
            
            # Join constraints
            constraints = "\n".join(result.get("constraints", []))
            
            return {
                "success": True,
                "objective": objective,
                "constraints": constraints,
                "variables": result.get("variables", []),
                "variable_descriptions": result.get("variable_descriptions", {}),
                "constraint_descriptions": result.get("constraint_descriptions", {}),
                "explanation": result.get("explanation", ""),
                "raw_result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to format result: {str(e)}",
                "raw_result": result
            }
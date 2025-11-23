"""
Content Analyzer - Analyzes content for frameworks, tone, case studies, etc.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
MODEL_NAME = "gemini-2.0-flash-exp"  # Fast model, same as initial run

def extract_json_from_text(text: str) -> Dict:
    """Extract JSON from text, handling markdown code blocks"""
    import re
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except:
            pass
    
    # Try to find JSON without code blocks
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except:
            pass
    
    return {}

class ContentAnalyzer:
    """Analyzes content for various attributes."""
    
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)
    
    def analyze_content(self, content: str, file_metadata: Dict) -> Dict:
        """
        Comprehensive content analysis.
        
        Args:
            content: Text content to analyze
            file_metadata: Metadata about the file
        
        Returns:
            Analysis results dictionary
        """
        prompt = f"""Analyze this content and extract:

1. **Content Type** (article, framework, case study, training material, sales script, etc.)
2. **Key Topics** (main subjects covered)
3. **Frameworks** (any structured methodologies, processes, or systems mentioned)
4. **Case Studies/Examples** (specific client stories, results, or examples)
5. **Tone of Voice** (writing style, formality, directness)
6. **Key Messages** (main points or takeaways)
7. **Target Audience** (who this is written for)
8. **Actionable Insights** (specific advice, steps, or recommendations)
9. **Data/Statistics** (numbers, metrics, results mentioned)
10. **Content Quality Score** (0-100 based on specificity, clarity, usefulness)

Content:
{content[:10000]}  # Limit to first 10k chars for analysis

Return JSON format:
{{
  "content_type": "string",
  "key_topics": ["topic1", "topic2"],
  "frameworks": [
    {{
      "name": "framework name",
      "description": "what it is",
      "components": ["component1", "component2"]
    }}
  ],
  "case_studies": [
    {{
      "description": "brief description",
      "result": "outcome or metric if mentioned"
    }}
  ],
  "tone_of_voice": {{
    "style": "conversational/formal/technical",
    "directness": "direct/indirect",
    "formality": "casual/professional/formal"
  }},
  "key_messages": ["message1", "message2"],
  "target_audience": "description",
  "actionable_insights": ["insight1", "insight2"],
  "data_statistics": ["stat1", "stat2"],
  "quality_score": 85,
  "summary": "brief summary of the content"
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text
            analysis = extract_json_from_text(result_text)
            
            # Add metadata
            analysis["file_metadata"] = file_metadata
            analysis["analyzed_at"] = datetime.now().isoformat()
            
            return analysis
        except Exception as e:
            print(f"❌ Error analyzing content: {e}")
            return {
                "error": str(e),
                "file_metadata": file_metadata,
                "analyzed_at": datetime.now().isoformat()
            }
    
    def extract_frameworks(self, content: str) -> List[Dict]:
        """Extract frameworks from content."""
        prompt = f"""Extract all frameworks, methodologies, processes, or structured systems from this content.

A framework is:
- A named system or process (e.g., "The 5-Step Sales Process")
- A structured methodology with components
- A repeatable approach or model

Content:
{content[:5000]}

Return JSON array:
[
  {{
    "name": "framework name",
    "type": "process/methodology/model/system",
    "description": "what it is and how it works",
    "components": ["step1", "step2", "step3"],
    "use_case": "when to use this",
    "example": "brief example if provided"
  }}
]
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text
            frameworks = extract_json_from_text(result_text)
            
            if isinstance(frameworks, list):
                return frameworks
            elif isinstance(frameworks, dict) and "frameworks" in frameworks:
                return frameworks["frameworks"]
            else:
                return []
        except Exception as e:
            print(f"❌ Error extracting frameworks: {e}")
            return []
    
    def analyze_tone(self, content: str) -> Dict:
        """Analyze tone of voice."""
        prompt = f"""Analyze the tone of voice in this content.

Consider:
- Formality level (casual, professional, formal)
- Directness (direct, indirect, conversational)
- Writing style (narrative, instructional, persuasive)
- Voice characteristics (authoritative, friendly, technical, etc.)

Content:
{content[:3000]}

Return JSON:
{{
  "formality": "casual/professional/formal",
  "directness": "direct/indirect/conversational",
  "style": "narrative/instructional/persuasive/analytical",
  "characteristics": ["authoritative", "friendly", "technical"],
  "sentence_length": "short/medium/long",
  "use_of_examples": "frequent/moderate/rare",
  "tone_description": "overall description"
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text
            tone = extract_json_from_text(result_text)
            return tone
        except Exception as e:
            print(f"❌ Error analyzing tone: {e}")
            return {"error": str(e)}


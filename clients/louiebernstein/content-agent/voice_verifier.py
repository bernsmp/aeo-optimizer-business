#!/usr/bin/env python3
"""
Louie Bernstein Voice Verification System

Analyzes content against Louie's voice guide to ensure consistency.
Returns a detailed score and recommendations for improvement.
"""

import re
import json
from typing import Dict, List, Tuple
from pathlib import Path


class LouieVoiceVerifier:
    """Verifies content matches Louie Bernstein's voice patterns."""
    
    def __init__(self):
        self.voice_guide_path = Path(__file__).parent.parent / "LOUIE-BERNSTEIN-VOICE-GUIDE.md"
        
        # Banned phrases (from voice guide)
        self.banned_phrases = [
            r'\bleverage\b',
            r'\bsynergy\b',
            r'\boptimize\b',
            r'\butilize\b',
            r'\bfacilitate\b',
            r'\bsignificantly\b',
            r'\ba lot\b',
            r'\bmany\b',
            r'\bseveral\b',
            r'\bmight\b',
            r'\bperhaps\b',
            r'\bpotentially\b',
            r'\bcould be\b',
        ]
        
        # Signature phrases (should appear)
        self.signature_phrases = [
            r"Here's why",
            r"Here's what",
            r"Here's the problem",
            r"I got a note",
            r"I once",
            r"Founders,",
            r"Sales Leaders,",
            r"Salespeople,",
            r"EVERYONE will be better off",
            r"Do this",
            r"Put it in writing",
            r"Save yourself the headaches",
        ]
        
        # Target metrics
        self.targets = {
            'avg_sentence_length': (12, 18),
            'number_density': (3, 6),  # per 100 words
            'you_density': (15, 25),  # per 100 words
            'active_voice_pct': (85, 95),
            'paragraph_length': (2, 4),  # sentences per paragraph
        }
    
    def analyze(self, content: str) -> Dict:
        """Analyze content against Louie's voice guide."""
        
        # Basic metrics
        words = self._count_words(content)
        sentences = self._split_sentences(content)
        paragraphs = self._split_paragraphs(content)
        
        # Calculate metrics
        metrics = {
            'word_count': words,
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_sentence_length': sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0,
            'avg_paragraph_length': sum(len(self._split_sentences(p)) for p in paragraphs) / len(paragraphs) if paragraphs else 0,
        }
        
        # Number analysis
        numbers = self._extract_numbers(content)
        metrics['number_count'] = len(numbers)
        metrics['number_density'] = (len(numbers) / words * 100) if words > 0 else 0
        
        # Direct address analysis
        you_count = len(re.findall(r'\byou\b', content, re.IGNORECASE))
        your_count = len(re.findall(r'\byour\b', content, re.IGNORECASE))
        metrics['you_count'] = you_count
        metrics['your_count'] = your_count
        metrics['you_density'] = ((you_count + your_count) / words * 100) if words > 0 else 0
        
        # Active/passive voice
        active_pct, passive_pct = self._analyze_voice(sentences)
        metrics['active_voice_pct'] = active_pct
        metrics['passive_voice_pct'] = passive_pct
        
        # Banned patterns
        banned_found = self._detect_banned_patterns(content)
        
        # Signature phrases
        signatures_found = self._detect_signature_phrases(content)
        
        # Score calculation
        scores = self._calculate_scores(metrics, banned_found, signatures_found)
        
        # Recommendations
        recommendations = self._generate_recommendations(metrics, banned_found, signatures_found, scores)
        
        return {
            'metrics': metrics,
            'banned_patterns': banned_found,
            'signature_phrases': signatures_found,
            'scores': scores,
            'recommendations': recommendations,
            'overall_score': scores['overall'],
            'status': self._get_status(scores['overall']),
        }
    
    def _count_words(self, text: str) -> int:
        """Count words in text (ignoring markdown)."""
        # Remove markdown syntax
        text = re.sub(r'#+\s*', '', text)  # Headers
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Italic
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Links
        text = re.sub(r'`([^`]+)`', r'\1', text)  # Code
        text = re.sub(r'[-*+]\s+', '', text)  # Bullets
        text = re.sub(r'\d+\.\s+', '', text)  # Numbered lists
        
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Remove markdown first
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        
        # Split on sentence endings
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip() and not p.strip().startswith('#')]
    
    def _extract_numbers(self, text: str) -> List[Dict]:
        """Extract all numbers from text."""
        numbers = []
        
        # Years
        years = re.findall(r'\b(19|20)\d{2}\b', text)
        numbers.extend([{'type': 'year', 'value': y} for y in years])
        
        # Percentages
        percentages = re.findall(r'\b\d+%', text)
        numbers.extend([{'type': 'percentage', 'value': p} for p in percentages])
        
        # Dollar amounts
        dollars = re.findall(r'\$[\d,]+(?:\.\d+)?(?:[MBK])?', text)
        numbers.extend([{'type': 'dollar', 'value': d} for d in dollars])
        
        # Quantities (X calls, X years, etc.)
        quantities = re.findall(r'\b(\d+)\s+(calls|years|months|days|hours|minutes|percent|people|companies|salespeople|reps|founders)', text, re.IGNORECASE)
        numbers.extend([{'type': 'quantity', 'value': f"{q[0]} {q[1]}"} for q in quantities])
        
        # Standalone numbers (likely quantities)
        standalone = re.findall(r'\b(\d{2,})\b', text)
        # Filter out years we already captured
        standalone = [s for s in standalone if not (s.startswith('19') or s.startswith('20'))]
        numbers.extend([{'type': 'number', 'value': s} for s in standalone[:10]])  # Limit to avoid noise
        
        return numbers
    
    def _analyze_voice(self, sentences: List[str]) -> Tuple[float, float]:
        """Analyze active vs passive voice."""
        passive_indicators = [
            r'\bwas\s+\w+ed\b',
            r'\bwere\s+\w+ed\b',
            r'\bis\s+\w+ed\b',
            r'\bare\s+\w+ed\b',
            r'\bhas\s+been\s+\w+ed\b',
            r'\bhave\s+been\s+\w+ed\b',
            r'\bhad\s+been\s+\w+ed\b',
        ]
        
        total = len(sentences)
        if total == 0:
            return 100.0, 0.0
        
        passive_count = 0
        for sentence in sentences:
            for pattern in passive_indicators:
                if re.search(pattern, sentence, re.IGNORECASE):
                    passive_count += 1
                    break
        
        passive_pct = (passive_count / total) * 100
        active_pct = 100 - passive_pct
        
        return active_pct, passive_pct
    
    def _detect_banned_patterns(self, text: str) -> List[Dict]:
        """Detect banned phrases."""
        found = []
        
        for pattern in self.banned_phrases:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get context
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end]
                
                found.append({
                    'pattern': pattern,
                    'text': match.group(),
                    'location': f"Character {match.start()}",
                    'context': context,
                    'severity': 'high' if pattern in ['might', 'perhaps', 'potentially'] else 'medium',
                })
        
        return found
    
    def _detect_signature_phrases(self, text: str) -> List[Dict]:
        """Detect Louie's signature phrases."""
        found = []
        
        for pattern in self.signature_phrases:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                found.append({
                    'phrase': pattern,
                    'text': match.group(),
                    'location': f"Character {match.start()}",
                })
        
        return found
    
    def _calculate_scores(self, metrics: Dict, banned_found: List, signatures_found: List) -> Dict:
        """Calculate voice scores."""
        scores = {}
        
        # Directness score (based on sentence length and clarity)
        avg_sent_len = metrics['avg_sentence_length']
        if 12 <= avg_sent_len <= 18:
            scores['directness'] = 25
        elif 10 <= avg_sent_len < 12 or 18 < avg_sent_len <= 20:
            scores['directness'] = 20
        elif 8 <= avg_sent_len < 10 or 20 < avg_sent_len <= 25:
            scores['directness'] = 15
        else:
            scores['directness'] = 10
        
        # Specificity score (based on number density)
        num_density = metrics['number_density']
        if 5 <= num_density <= 6:
            scores['specificity'] = 25
        elif 3 <= num_density < 5:
            scores['specificity'] = 20
        elif 1 <= num_density < 3:
            scores['specificity'] = 15
        elif num_density > 6:
            scores['specificity'] = 22  # Slightly over but still good
        else:
            scores['specificity'] = 5
        
        # Experience-based authority (based on signature phrases and "I" usage)
        i_count = len(re.findall(r'\bI\b', metrics.get('sample_text', '')))
        sig_score = min(15, len(signatures_found) * 2)  # Up to 15 points
        i_score = min(5, i_count / 10)  # Up to 5 points
        scores['authority'] = sig_score + i_score
        
        # Tone & empathy (based on "you" density and banned patterns)
        you_density = metrics['you_density']
        if 15 <= you_density <= 25:
            tone_score = 12
        elif 10 <= you_density < 15 or 25 < you_density <= 30:
            tone_score = 9
        else:
            tone_score = 6
        
        # Penalize banned patterns
        banned_penalty = min(3, len(banned_found) * 0.5)
        scores['tone'] = max(0, tone_score - banned_penalty)
        
        # Sentence structure score
        avg_para_len = metrics['avg_paragraph_length']
        if 2 <= avg_para_len <= 4:
            scores['structure'] = 10
        elif 1 <= avg_para_len < 2 or 4 < avg_para_len <= 6:
            scores['structure'] = 7
        else:
            scores['structure'] = 4
        
        # Active voice score
        active_pct = metrics['active_voice_pct']
        if active_pct >= 85:
            scores['voice'] = 5
        elif active_pct >= 70:
            scores['voice'] = 3
        else:
            scores['voice'] = 1
        
        # Overall score
        scores['overall'] = sum(scores.values())
        
        return scores
    
    def _generate_recommendations(self, metrics: Dict, banned_found: List, 
                                 signatures_found: List, scores: Dict) -> List[str]:
        """Generate specific recommendations."""
        recommendations = []
        
        # Banned patterns
        if banned_found:
            recommendations.append(f"❌ Found {len(banned_found)} banned phrase(s). Replace with Louie's preferred language.")
            for banned in banned_found[:3]:  # Show first 3
                recommendations.append(f"   - Replace '{banned['text']}' (found at {banned['location']})")
        
        # Number density
        num_density = metrics['number_density']
        if num_density < 3:
            needed = int((3 - num_density) * metrics['word_count'] / 100)
            recommendations.append(f"⚠️ Add {needed} more specific numbers (years, percentages, quantities, dollar amounts)")
        elif num_density > 6:
            recommendations.append("✅ Number density is excellent - maintain this level")
        else:
            recommendations.append("✅ Number density is good")
        
        # Sentence length
        avg_sent_len = metrics['avg_sentence_length']
        if avg_sent_len < 12:
            recommendations.append(f"⚠️ Average sentence length ({avg_sent_len:.1f} words) is too short. Add some medium-length sentences (12-18 words)")
        elif avg_sent_len > 18:
            recommendations.append(f"⚠️ Average sentence length ({avg_sent_len:.1f} words) is too long. Break up some sentences")
        else:
            recommendations.append(f"✅ Sentence length ({avg_sent_len:.1f} words) is perfect")
        
        # You density
        you_density = metrics['you_density']
        if you_density < 15:
            recommendations.append(f"⚠️ Direct address ('you'/'your') density ({you_density:.1f} per 100 words) is low. Target: 15-25 per 100 words")
        elif you_density > 25:
            recommendations.append(f"⚠️ Direct address density ({you_density:.1f} per 100 words) is high. Consider reducing slightly")
        else:
            recommendations.append(f"✅ Direct address density ({you_density:.1f} per 100 words) is perfect")
        
        # Active voice
        active_pct = metrics['active_voice_pct']
        if active_pct < 85:
            recommendations.append(f"⚠️ Active voice ({active_pct:.1f}%) is below target (85%+). Convert passive constructions to active")
        else:
            recommendations.append(f"✅ Active voice ({active_pct:.1f}%) is excellent")
        
        # Signature phrases
        if len(signatures_found) == 0:
            recommendations.append("⚠️ No signature phrases found. Consider adding phrases like 'Here's why...', 'Here's what I did...', 'Founders,'")
        elif len(signatures_found) < 3:
            recommendations.append(f"✅ Found {len(signatures_found)} signature phrase(s) - consider adding 1-2 more")
        else:
            recommendations.append(f"✅ Found {len(signatures_found)} signature phrases - excellent")
        
        # Paragraph length
        avg_para_len = metrics['avg_paragraph_length']
        if avg_para_len > 4:
            recommendations.append(f"⚠️ Average paragraph length ({avg_para_len:.1f} sentences) is too long. Target: 2-4 sentences")
        else:
            recommendations.append(f"✅ Paragraph length ({avg_para_len:.1f} sentences) is good")
        
        return recommendations
    
    def _get_status(self, score: float) -> str:
        """Get status based on score."""
        if score >= 90:
            return "excellent"
        elif score >= 85:
            return "good"
        elif score >= 75:
            return "fair"
        elif score >= 60:
            return "poor"
        else:
            return "fail"
    
    def verify_file(self, file_path: str) -> Dict:
        """Verify content from a file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.analyze(content)
    
    def verify_text(self, text: str) -> Dict:
        """Verify content from text string."""
        return self.analyze(text)


def main():
    """CLI interface for voice verification."""
    import sys
    
    verifier = LouieVoiceVerifier()
    
    if len(sys.argv) < 2:
        print("Usage: python voice_verifier.py <file_path>")
        print("   or: python voice_verifier.py --text '<content>'")
        sys.exit(1)
    
    if sys.argv[1] == '--text':
        content = ' '.join(sys.argv[2:])
        result = verifier.verify_text(content)
    else:
        file_path = sys.argv[1]
        result = verifier.verify_file(file_path)
    
    # Print results
    print("\n" + "="*60)
    print("LOUIE BERNSTEIN VOICE VERIFICATION")
    print("="*60)
    print(f"\nOverall Score: {result['overall_score']:.1f}/100 ({result['status'].upper()})")
    print(f"\nBreakdown:")
    print(f"  Directness:        {result['scores']['directness']}/25")
    print(f"  Specificity:       {result['scores']['specificity']}/25")
    print(f"  Authority:         {result['scores']['authority']}/20")
    print(f"  Tone & Empathy:    {result['scores']['tone']}/15")
    print(f"  Structure:         {result['scores']['structure']}/10")
    print(f"  Active Voice:      {result['scores']['voice']}/5")
    
    print(f"\nMetrics:")
    print(f"  Word Count:        {result['metrics']['word_count']}")
    print(f"  Sentences:         {result['metrics']['sentence_count']}")
    print(f"  Avg Sentence:     {result['metrics']['avg_sentence_length']:.1f} words")
    print(f"  Numbers Found:    {result['metrics']['number_count']}")
    print(f"  Number Density:    {result['metrics']['number_density']:.1f} per 100 words")
    print(f"  You/Your Density: {result['metrics']['you_density']:.1f} per 100 words")
    print(f"  Active Voice:     {result['metrics']['active_voice_pct']:.1f}%")
    
    if result['banned_patterns']:
        print(f"\n⚠️  Banned Patterns Found: {len(result['banned_patterns'])}")
        for banned in result['banned_patterns'][:5]:
            print(f"   - '{banned['text']}' at {banned['location']}")
    
    if result['signature_phrases']:
        print(f"\n✅ Signature Phrases Found: {len(result['signature_phrases'])}")
        for sig in result['signature_phrases'][:5]:
            print(f"   - '{sig['text']}' at {sig['location']}")
    
    print(f"\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  {rec}")
    
    print("\n" + "="*60)
    
    # Return exit code based on score
    if result['overall_score'] >= 85:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Needs improvement


if __name__ == '__main__':
    main()


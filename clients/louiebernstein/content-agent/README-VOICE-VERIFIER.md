# Louie Bernstein Voice Verifier

Automated voice verification system to ensure content matches Louie's authentic voice patterns.

## Quick Start

```bash
# Verify an article file
python voice_verifier.py articles/my-article.md

# Verify text directly
python voice_verifier.py --text "Your article content here..."
```

## What It Does

The voice verifier analyzes content against Louie's voice guide and provides:

1. **Overall Score** (0-100, target: 85+)
2. **Detailed Breakdown:**
   - Directness (25 points)
   - Specificity (25 points)
   - Authority (20 points)
   - Tone & Empathy (15 points)
   - Structure (10 points)
   - Active Voice (5 points)

3. **Metrics:**
   - Word count, sentence count
   - Average sentence length
   - Number density (per 100 words)
   - Direct address density ("you"/"your" per 100 words)
   - Active vs. passive voice percentage

4. **Pattern Detection:**
   - Banned phrases found (should be 0)
   - Signature phrases found (should be 3+)

5. **Specific Recommendations:**
   - What to fix
   - What to add
   - What's working well

## Score Interpretation

- **90-100:** Excellent - Publication ready ✅
- **85-89:** Good - Minor tweaks needed ✅
- **75-84:** Fair - Needs revision ⚠️
- **60-74:** Poor - Major revision needed ❌
- **<60:** Fail - Complete rewrite needed ❌

## Integration with Article Expansion

The voice verifier is integrated into the article expansion workflow:

1. Draft article using `ARTICLE-EXPANSION-SYSTEM.md`
2. Run voice verification: `python voice_verifier.py article.md`
3. Review recommendations and fix issues
4. Re-run until score ≥ 85
5. Publish

## Example Output

```
============================================================
LOUIE BERNSTEIN VOICE VERIFICATION
============================================================

Overall Score: 87.5/100 (GOOD)

Breakdown:
  Directness:        23/25
  Specificity:       22/25
  Authority:        18/20
  Tone & Empathy:    13/15
  Structure:         9/10
  Active Voice:      4/5

Metrics:
  Word Count:        1850
  Sentences:         125
  Avg Sentence:      14.8 words
  Numbers Found:     12
  Number Density:    6.5 per 100 words
  You/Your Density:  18.2 per 100 words
  Active Voice:      88.0%

✅ Signature Phrases Found: 4
   - 'Here's why' at Character 245
   - 'Founders,' at Character 512
   - 'Here's what I did' at Character 890
   - 'Put it in writing' at Character 1234

Recommendations:
  ✅ Number density is excellent - maintain this level
  ✅ Sentence length (14.8 words) is perfect
  ✅ Direct address density (18.2 per 100 words) is perfect
  ✅ Active voice (88.0%) is excellent
  ✅ Found 4 signature phrases - excellent
  ✅ Paragraph length (3.2 sentences) is good

============================================================
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Usage Tips

1. **Run early and often:** Check voice during drafting, not just at the end
2. **Fix banned patterns first:** These are high-priority issues
3. **Add numbers:** If number density is low, add specific years, percentages, quantities
4. **Use signature phrases:** Add "Here's why...", "Founders,", etc.
5. **Check sentence length:** Mix short (3-8 words) and medium (12-18 words) sentences

## Reference

See `LOUIE-BERNSTEIN-VOICE-GUIDE.md` for complete voice specifications and examples.


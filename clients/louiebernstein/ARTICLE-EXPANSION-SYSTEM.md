# Article Expansion System for Louie Bernstein

## Adapted from Jay Article Writer Prompts

This system expands LinkedIn posts into full articles optimized for Louie's voice, frameworks, and AEO.

---

## LOUIE'S VOICE CALIBRATION

**Louie's Voice Characteristics:**
- Direct, practical sales leadership advice
- Real-world examples from 9+ years as Fractional Sales Leader
- Focus on $1M-$10M ARR companies
- Systematic frameworks and processes
- Clear, actionable guidance
- Less contrarian than Jay - more "here's what works"

**Key Differences from Jay:**
- Louie: Practical, systematic, process-focused
- Jay: Contrarian, asset-focused, revenue multiplication
- Louie: Sales leadership and team building
- Jay: Business strategy and hidden assets

---

## ARTICLE STRUCTURE (Adapted for Louie)

### 1. HOOK (Problem/Story Opening)
- Start with the real-world problem or story
- Use specific numbers when available
- Connect to sales leadership pain point
- 150-200 words

### 2. THE PROBLEM (Expanded Context)
- Why this matters for $1M-$10M ARR companies
- Common mistakes sales leaders make
- Cost of not addressing this
- 200-300 words

### 3. THE FRAMEWORK/SOLUTION
- Present Louie's systematic approach
- Reference relevant frameworks from his content
- Step-by-step process
- 400-600 words

### 4. CASE STUDIES/EXAMPLES
- Use real examples from Louie's content
- Reference frameworks in action
- Show results (numbers when available)
- 300-400 words

### 5. IMPLEMENTATION GUIDE
- How to implement this
- Common pitfalls to avoid
- Tools/resources needed
- 300-400 words

### 6. CLOSING/CTA
- Summary of key points
- Clear next step
- Link to consultation/scheduling
- 100-150 words

**Total Target:** 1,500-2,000 words

---

## LOUIE'S FRAMEWORKS TO REFERENCE

From ingested content:
1. **CEO's Sales System** - Core sales framework
2. **One-on-One Meetings** - Manager-rep communication
3. **Onboarding System** - Getting new reps productive
4. **TSP Feedback Model** - Truthful, Specific, Positive
5. **Position Contract** - Clear job descriptions
6. **Sales Process** - Consistent, repeatable process
7. **Sales Cadence Calendar** - Structured outreach

---

## CASE STUDIES TO USE

From ingested content:
- BankMarketingCenter.com - Improved consistency and measurability
- ZBS POS - Improved sales performance
- 61% year-over-year increase (fractional sales manager case)
- Sales rep achieving 135% quota but put on PIP (the LinkedIn post story)

---

## VOICE REQUIREMENTS

**Reference:** See `LOUIE-BERNSTEIN-VOICE-GUIDE.md` for complete voice specifications.

✓ Direct, practical language
✓ Specific examples and numbers
✓ Focus on $1M-$10M ARR companies
✓ Systematic, process-oriented
✓ Actionable guidance
✓ Reference frameworks when relevant
✓ Real-world sales leadership context

**Voice Metrics Targets:**
- Sentence length: 12-18 words average
- Number density: 3-6 specific numbers per 100 words
- Direct address: 15-25 instances of "you"/"your" per 100 words
- Active voice: 85-95% active voice
- Paragraph length: 2-4 sentences per paragraph

**Avoid:**
- Overly contrarian statements
- Generic business advice
- Vague promises
- Corporate jargon ("leverage", "optimize", "utilize")
- Passive voice
- Banned phrases (see voice guide Section 10)

---

## AEO OPTIMIZATION

**Include:**
- Clear H2/H3 headings
- FAQ section (3-5 questions)
- Specific numbers and metrics
- Framework names clearly stated
- Actionable steps
- Internal linking opportunities

**Keywords to naturally include:**
- Fractional sales leader
- Sales team management
- Sales process
- Job descriptions
- Performance improvement plans
- Sales accountability
- $1M-$10M ARR

---

## OUTPUT FORMAT

# [Article Title]

[Hook/Opening - 150-200 words]

## The Problem: [Clear Problem Statement]

[Expanded context - 200-300 words]

## The Solution: [Framework Name or Approach]

[Step-by-step solution - 400-600 words]

## Real Examples: [Case Studies]

[Examples from Louie's content - 300-400 words]

## How to Implement This

[Actionable steps - 300-400 words]

## Frequently Asked Questions

[3-5 relevant FAQs]

## Conclusion

[Summary and CTA - 100-150 words]

---

## QUALITY CHECKLIST

Before finalizing article:
- [ ] Uses Louie's frameworks where relevant
- [ ] Includes specific numbers/metrics
- [ ] References real case studies
- [ ] Actionable, step-by-step guidance
- [ ] Clear headings and structure
- [ ] FAQ section included
- [ ] AEO keywords naturally integrated
- [ ] CTA to consultation/scheduling
- [ ] 1,500-2,000 words total
- [ ] Voice matches Louie's practical, systematic style
- [ ] **Voice verification score ≥85/100** (run `python content-agent/voice_verifier.py <article_file>`)

## VOICE VERIFICATION

**Required Step:** After drafting the article, run voice verification:

```bash
# Verify a file
python content-agent/voice_verifier.py articles/my-article.md

# Verify text directly
python content-agent/voice_verifier.py --text "Your article content here..."
```

**Target Score:** 85+ out of 100

**What It Checks:**
- Directness (sentence length, clarity)
- Specificity (number density, concrete examples)
- Authority (signature phrases, experience markers)
- Tone & Empathy (direct address, banned patterns)
- Structure (paragraph length, rhythm)
- Active Voice (85%+ active voice)

**If Score < 85:**
- Review recommendations from voice verifier
- Fix banned patterns first (high priority)
- Add specific numbers if density is low
- Adjust sentence length if needed
- Add signature phrases if missing
- Re-run verification until score ≥ 85


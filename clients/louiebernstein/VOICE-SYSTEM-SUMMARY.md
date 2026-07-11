# Louie Bernstein Voice System - Complete Setup

**Date Created:** November 23, 2025

---

## ✅ What's Been Created

### 1. **Voice Guide** (`LOUIE-BERNSTEIN-VOICE-GUIDE.md`)
Complete 20-section voice reference guide covering:
- Core voice characteristics
- Sentence structure & rhythm
- Tone & style markers
- Audience address patterns
- Number & specificity usage
- Storytelling patterns
- List & framework patterns
- Question usage
- Active vs. passive voice
- Power words & phrases
- Content themes
- Personal brand elements
- CTA patterns
- Emoji & formatting
- Voice verification checklist
- Voice scoring system
- Common mistakes
- Format adaptation
- Perfect examples
- Quick reference

### 2. **Voice Verifier Script** (`content-agent/voice_verifier.py`)
Automated Python script that:
- Analyzes content against Louie's voice patterns
- Calculates voice score (0-100, target: 85+)
- Detects banned phrases
- Identifies signature phrases
- Provides specific recommendations
- Can be run from command line or imported as module

### 3. **Updated Article Expansion System** (`ARTICLE-EXPANSION-SYSTEM.md`)
Integrated voice verification into the article expansion workflow:
- Added voice metrics targets
- Added voice verification step to quality checklist
- Included instructions for using the verifier

### 4. **Documentation** (`content-agent/README-VOICE-VERIFIER.md`)
Complete usage guide for the voice verifier

---

## 🚀 How to Use

### For Content Creation:

1. **Reference the Voice Guide:**
   - Read `LOUIE-BERNSTEIN-VOICE-GUIDE.md` before writing
   - Use Section 20 (Quick Reference) during writing
   - Check Section 15 (Verification Checklist) before publishing

2. **Use the Article Expansion System:**
   - Follow `ARTICLE-EXPANSION-SYSTEM.md` for structure
   - Reference Louie's frameworks and case studies
   - Ensure voice matches practical, systematic style

3. **Verify Voice Before Publishing:**
   ```bash
   # Verify an article file
   python3 content-agent/voice_verifier.py articles/my-article.md
   
   # Verify text directly
   python3 content-agent/voice_verifier.py --text "Your content here..."
   ```

4. **Fix Issues:**
   - Review recommendations from verifier
   - Fix banned patterns first (high priority)
   - Add specific numbers if density is low
   - Adjust sentence length if needed
   - Add signature phrases if missing
   - Re-run until score ≥ 85

---

## 📊 Voice Metrics Targets

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| **Sentence Length** | 12-18 words avg | Louie's voice is direct but explanatory |
| **Number Density** | 3-6 per 100 words | Specificity builds credibility |
| **Direct Address** | 15-25 "you"/"your" per 100 words | Creates connection with audience |
| **Active Voice** | 85-95% | Direct, actionable language |
| **Paragraph Length** | 2-4 sentences | Easy to scan and digest |
| **Signature Phrases** | 3+ per article | Establishes Louie's voice patterns |

---

## 🎯 Voice Score Interpretation

- **90-100:** Excellent - Publication ready ✅
- **85-89:** Good - Minor tweaks needed ✅
- **75-84:** Fair - Needs revision ⚠️
- **60-74:** Poor - Major revision needed ❌
- **<60:** Fail - Complete rewrite needed ❌

---

## 🔍 What Gets Checked

### Directness (25 points)
- Sentence length (12-18 words ideal)
- Clarity and actionability

### Specificity (25 points)
- Number density (3-6 per 100 words)
- Concrete examples vs. vague language

### Authority (20 points)
- Signature phrases ("Here's why...", "Founders,")
- Experience markers ("I once...", "I've found...")

### Tone & Empathy (15 points)
- Direct address ("you"/"your" density)
- Absence of banned phrases

### Structure (10 points)
- Paragraph length (2-4 sentences)
- Rhythm and flow

### Active Voice (5 points)
- 85%+ active voice
- Clear, direct action statements

---

## 🚫 Banned Phrases

Never use these (automatically flagged):
- leverage, synergy, optimize, utilize, facilitate
- significantly, a lot, many, several
- might, perhaps, potentially, could be

**Replace with:**
- "use" instead of "leverage/utilize"
- Specific numbers instead of "many/several"
- "will/should" instead of "might/perhaps"

---

## ✅ Signature Phrases

Should appear in content (3+ per article):
- "Here's why..."
- "Here's what I did..."
- "Here's the problem:"
- "I got a note..."
- "I once..."
- "Founders," / "Sales Leaders," / "Salespeople,"
- "EVERYONE will be better off because you did."
- "Do this."
- "Put it in writing."
- "Save yourself the headaches."

---

## 📝 Example Workflow

1. **Draft Article** using `ARTICLE-EXPANSION-SYSTEM.md`
2. **Run Verification:**
   ```bash
   python3 content-agent/voice_verifier.py articles/draft.md
   ```
3. **Review Output:**
   - Check overall score (target: 85+)
   - Review banned patterns (should be 0)
   - Check recommendations
4. **Fix Issues:**
   - Replace banned phrases
   - Add specific numbers
   - Adjust sentence length
   - Add signature phrases
5. **Re-verify** until score ≥ 85
6. **Publish**

---

## 🎓 Key Insights from Voice Analysis

**Louie's Voice is:**
- **Practical** - Always actionable, never theoretical
- **Experienced** - Grounded in 22 years running a business, 50+ years in sales
- **Empathetic** - Acknowledges struggle, then provides solution
- **Direct** - No fluff, straight to the point
- **Specific** - Numbers, dates, concrete examples
- **Authoritative** - Confident from experience
- **Helpful** - Focused on helping others succeed

**Remember:** If it doesn't sound like Louie would say it across the table to a Founder or Sales Leader, it's not his voice.

---

## 📚 Files Reference

- **Voice Guide:** `LOUIE-BERNSTEIN-VOICE-GUIDE.md`
- **Voice Verifier:** `content-agent/voice_verifier.py`
- **Verifier Docs:** `content-agent/README-VOICE-VERIFIER.md`
- **Article System:** `ARTICLE-EXPANSION-SYSTEM.md`
- **This Summary:** `VOICE-SYSTEM-SUMMARY.md`

---

## 🔄 Next Steps

1. ✅ Voice guide created
2. ✅ Voice verifier script created
3. ✅ Article expansion system updated
4. ✅ Documentation created
5. ⏭️ Test with real article drafts
6. ⏭️ Refine scoring based on feedback
7. ⏭️ Integrate into content creation workflow

---

**Questions?** Refer to the voice guide or verifier documentation for detailed information.


# Monthly AEO Progress Report

**Client:** {{CLIENT_NAME}}
**Period:** {{MONTH}} {{YEAR}}
**Prepared by:** Max Bernstein, AEO Machine

---

## Executive Summary

{{EXECUTIVE_SUMMARY}}

---

## AEO Score Progress

| Metric | Last Month | This Month | Delta |
|--------|-----------|------------|-------|
| **Composite Score** | {{PREV_SCORE}}/100 | {{CURR_SCORE}}/100 | {{DELTA}} |
| **Grade** | {{PREV_GRADE}} | {{CURR_GRADE}} | |

### Score Trajectory

```
Score
100 |
 90 |
 80 |
 70 |                                          {{MONTH_6_BAR}}
 60 |                              {{MONTH_5_BAR}}
 50 |                  {{MONTH_4_BAR}}
 40 |      {{MONTH_3_BAR}}
 30 |  {{MONTH_2_BAR}}
 20 |{{MONTH_1_BAR}}
 10 |
  0 +----+----+----+----+----+----+
     M1   M2   M3   M4   M5   M6
```

---

## Dimension Breakdown

| Dimension | Weight | Last Month | This Month | Delta | Trend |
|-----------|--------|-----------|------------|-------|-------|
| Citability & Structure | 20% | {{PREV_CITE}}/100 | {{CURR_CITE}}/100 | {{D_CITE}} | {{T_CITE}} |
| AI Mentions | 15% | {{PREV_AI}}/100 | {{CURR_AI}}/100 | {{D_AI}} | {{T_AI}} |
| Off-Site Authority | 15% | {{PREV_AUTH}}/100 | {{CURR_AUTH}}/100 | {{D_AUTH}} | {{T_AUTH}} |
| Schema & Structured Data | 15% | {{PREV_SCHEMA}}/100 | {{CURR_SCHEMA}}/100 | {{D_SCHEMA}} | {{T_SCHEMA}} |
| Answer Content (FAQ) | 10% | {{PREV_FAQ}}/100 | {{CURR_FAQ}}/100 | {{D_FAQ}} | {{T_FAQ}} |
| AI Crawler Access | 10% | {{PREV_CRAWL}}/100 | {{CURR_CRAWL}}/100 | {{D_CRAWL}} | {{T_CRAWL}} |
| Freshness Signals | 10% | {{PREV_FRESH}}/100 | {{CURR_FRESH}}/100 | {{D_FRESH}} | {{T_FRESH}} |
| llms.txt | 5% | {{PREV_LLMS}}/100 | {{CURR_LLMS}}/100 | {{D_LLMS}} | {{T_LLMS}} |

*Rubric rebalanced 2026-06-11. First report after the rebalance: re-baseline rather than compare deltas against pre-rebalance scores.*

**Trend key:** Improving / Stable / Declining

---

## Platform Readiness

| Platform | Last Month | This Month | Delta |
|----------|-----------|------------|-------|
| Google AI Overviews | {{PREV_AIO}}/100 | {{CURR_AIO}}/100 | {{D_AIO}} |
| ChatGPT | {{PREV_GPT}}/100 | {{CURR_GPT}}/100 | {{D_GPT}} |
| Perplexity | {{PREV_PERP}}/100 | {{CURR_PERP}}/100 | {{D_PERP}} |
| Gemini | {{PREV_GEM}}/100 | {{CURR_GEM}}/100 | {{D_GEM}} |
| Bing Copilot | {{PREV_BING}}/100 | {{CURR_BING}}/100 | {{D_BING}} |

---

## Brand Authority Score

| Platform | Weight | Last Month | This Month | Delta |
|----------|--------|-----------|------------|-------|
| YouTube (0.737 correlation) | 25% | | | |
| Reddit | 25% | | | |
| Wikipedia/Wikidata | 20% | | | |
| LinkedIn | 15% | | | |
| Other Platforms | 15% | | | |
| **Composite** | **100%** | | | |

---

## AI Crawler Access

| Crawler | User Agent | Tier | Status | Change |
|---------|-----------|------|--------|--------|
| OpenAI Search | OAI-SearchBot | Search | {{OAI_STATUS}} | {{OAI_CHANGE}} |
| Anthropic Search | Claude-SearchBot | Search | {{CLAUDESEARCH_STATUS}} | {{CLAUDESEARCH_CHANGE}} |
| Perplexity | PerplexityBot | Search | {{PERP_STATUS}} | {{PERP_CHANGE}} |
| OpenAI (user fetch) | ChatGPT-User | User | {{GPTUSER_STATUS}} | {{GPTUSER_CHANGE}} |
| Anthropic (user fetch) | Claude-User | User | {{CLAUDEUSER_STATUS}} | {{CLAUDEUSER_CHANGE}} |
| OpenAI (training) | GPTBot | Training | {{GPTBOT_STATUS}} | {{GPTBOT_CHANGE}} |
| Anthropic (training) | ClaudeBot | Training | {{CLAUDE_STATUS}} | {{CLAUDE_CHANGE}} |
| Google AI (training) | Google-Extended | Training | {{GOOGLE_STATUS}} | {{GOOGLE_CHANGE}} |
| Common Crawl | CCBot | Training | {{CC_STATUS}} | {{CC_CHANGE}} |
| Edge/CDN filtering | (differential test) | All | {{EDGE_STATUS}} | {{EDGE_CHANGE}} |

---

## Action Plan Progress

### Completed This Month

- [ ] {{ACTION_1}} -- {{IMPACT_1}}
- [ ] {{ACTION_2}} -- {{IMPACT_2}}
- [ ] {{ACTION_3}} -- {{IMPACT_3}}

### In Progress

- [ ] {{ACTION_4}} -- ETA: {{ETA_4}}
- [ ] {{ACTION_5}} -- ETA: {{ETA_5}}

### Planned for Next Month

- [ ] {{ACTION_6}}
- [ ] {{ACTION_7}}
- [ ] {{ACTION_8}}

---

## Wins This Month

{{WINS_NARRATIVE}}

---

## New Issues Identified

{{ISSUES_NARRATIVE}}

---

## Next Month Focus

**Primary objective:** {{PRIMARY_OBJECTIVE}}

**Key actions:**
1. {{NEXT_ACTION_1}}
2. {{NEXT_ACTION_2}}
3. {{NEXT_ACTION_3}}

---

## 6-Month Trajectory

Based on current velocity and planned actions:

| Month | Projected Score | Key Milestone |
|-------|----------------|---------------|
| Month 1 (current) | {{CURR_SCORE}}/100 | Baseline established |
| Month 2 | {{PROJ_M2}}/100 | {{MILE_M2}} |
| Month 3 | {{PROJ_M3}}/100 | {{MILE_M3}} |
| Month 4 | {{PROJ_M4}}/100 | {{MILE_M4}} |
| Month 5 | {{PROJ_M5}}/100 | {{MILE_M5}} |
| Month 6 | {{PROJ_M6}}/100 | {{MILE_M6}} |

---

## Delta Interpretation Guide

| Delta Range | Meaning |
|-------------|---------|
| +10 or more | Major improvement, likely from a structural change (schema, llms.txt, robots.txt) |
| +5 to +9 | Good progress, content and optimization work paying off |
| +1 to +4 | Incremental improvement, stay the course |
| 0 | No change, may need to reassess strategy |
| -1 to -4 | Minor regression, check for removed content or broken schemas |
| -5 or worse | Significant regression, investigate immediately |

---

*Report generated by AEO Machine. Next report: {{NEXT_REPORT_DATE}}*

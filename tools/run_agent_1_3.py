#!/usr/bin/env python3
"""Run Agent 1.3 in two phases (options + locked brief)."""

import sys
import os
import json
import re
sys.path.insert(0, '.')

from agents.prompts import (
    ARCHITECT_PHASE1_SYSTEM_PROMPT,
    ARCHITECT_SYSTEM_PROMPT
)
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model_name = "gemini-2.5-pro"


def call_agent(agent_name, system_prompt, user_input):
    """Call Gemini agent"""
    print(f"\n🤖 {agent_name} is thinking...")
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt
    )
    response = model.generate_content(user_input)
    print(f"✅ {agent_name} finished.")
    return response.text


def load_data(folder):
    """Load textual data from folder"""
    content = ''
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.endswith(('.md', '.txt')):
                with open(os.path.join(folder, file), 'r') as f:
                    content += f.read() + '\n\n'
    return content[:8000] if len(content) > 8000 else content


def extract_json_from_markdown(text):
    """Extract JSON blob from markdown or raw text"""
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    json_match = re.search(r'(\{(?:[^{}]|(?:\{[^{}]*\}))*\})', text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    return text


def display_options(options):
    print("\n================ POTENTIAL ANGLES ================")
    for idx, angle in enumerate(options.get("potential_angles", []), 1):
        print(f"\n[{idx}] {angle.get('angle')}")
        print(f"   Contrarian Strength: {angle.get('contrarian_strength')}")
        print(f"   Emotional Hook: {angle.get('emotional_hook')}")
        print(f"   Why it works: {angle.get('why_this_works')}")

    print("\n================ POTENTIAL FRAMEWORKS ================")
    for idx, framework in enumerate(options.get("potential_frameworks", []), 1):
        print(f"\n[{idx}] {framework.get('framework')}")
        print(f"   Fit Score: {framework.get('fit_score')}")
        print(f"   Why it fits: {framework.get('why_it_fits')}")

    print("\n================ ANGLE + FRAMEWORK COMBINATIONS ================")
    combos = options.get("angle_framework_combinations", [])
    for idx, combo in enumerate(combos, 1):
        print(f"\n[{idx}] Angle: {combo.get('angle')}")
        print(f"     Framework: {combo.get('framework')}")
        print(f"     Score: {combo.get('combination_score')}")
        print(f"     Why it works: {combo.get('why_this_works')}")
    print("\n====================================================")


def choose_combination(options):
    combos = options.get("angle_framework_combinations", [])
    if not combos:
        print("❌ No combinations returned. Regenerating...")
        return None

    while True:
        choice = input("Select combination number (or 'r' to regenerate, 'q' to quit): ").strip().lower()
        if choice == 'q':
            print("❌ Cancelled.")
            sys.exit(1)
        if choice == 'r':
            return 'regenerate'
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(combos):
                selected_combo = combos[idx-1]
                print(f"\n✅ Selected: {selected_combo.get('angle')} + {selected_combo.get('framework')}")
                return selected_combo
        print("Invalid choice. Try again.")


def find_detail(items, key, value):
    for item in items:
        if item.get(key) == value:
            return item
    return {}


def main():
    article_folder = 'output/article_1'
    analysis_file = f'{article_folder}/02_analysis.md'
    research_file = f'{article_folder}/01_research.json'

    if not os.path.exists(analysis_file):
        print(f'❌ Analysis file not found: {analysis_file}')
        print('   Run Agent 1.2 first!')
        sys.exit(1)

    if not os.path.exists(research_file):
        print(f'❌ Research file not found: {research_file}')
        print('   Run Agent 1.1 first!')
        sys.exit(1)

    with open(analysis_file, 'r') as f:
        analysis_content = f.read()

    with open(research_file, 'r') as f:
        research_content = json.load(f)

    titles = load_data('data/titles')
    rules = load_data('data/rules')

    # Phase 1: Generate options until user selects one
    options_data = None
    selected_combo = None

    while selected_combo is None:
        architect_phase1_input = f"ANALYSIS:\n{analysis_content}\n\nTITLES:\n{titles}\n\nRULES:\n{rules}"
        raw_phase1 = call_agent('Agent 1.3 (Architect Phase 1)', ARCHITECT_PHASE1_SYSTEM_PROMPT, architect_phase1_input)
        json_str = extract_json_from_markdown(raw_phase1)
        try:
            options_data = json.loads(json_str)
            os.makedirs(article_folder, exist_ok=True)
            with open(f'{article_folder}/03_angle_options.json', 'w') as f:
                json.dump(options_data, f, indent=2)
            display_options(options_data)
            result = choose_combination(options_data)
            if result == 'regenerate':
                continue
            selected_combo = result
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print("Raw output:", raw_phase1[:500])
            continue

    potential_angles = options_data.get("potential_angles", [])
    potential_frameworks = options_data.get("potential_frameworks", [])

    selected_angle = find_detail(potential_angles, "angle", selected_combo.get("angle"))
    selected_framework = find_detail(potential_frameworks, "framework", selected_combo.get("framework"))

    selection_payload = {
        "selected_combo": selected_combo,
        "selected_angle": selected_angle,
        "selected_framework": selected_framework
    }

    with open(f'{article_folder}/03_angle_selection.json', 'w') as f:
        json.dump(selection_payload, f, indent=2)

    # Phase 2: Build locked brief
    phase2_input = (
        f"CHOSEN ANGLE:\n{json.dumps(selected_angle, indent=2)}\n\n"
        f"CHOSEN FRAMEWORK:\n{json.dumps(selected_framework, indent=2)}\n\n"
        f"ANGLE + FRAMEWORK COMBINATION:\n{json.dumps(selected_combo, indent=2)}\n\n"
        f"ANALYSIS:\n{analysis_content}\n\n"
        f"RESEARCH:\n{json.dumps(research_content, indent=2)}\n\n"
        f"TITLES:\n{titles}\n\n"
        f"RULES:\n{rules}"
    )

    print('\n--- AGENT 1.3: ARCHITECT (Locked Brief) ---')
    brief = call_agent('Agent 1.3 (Architect)', ARCHITECT_SYSTEM_PROMPT, phase2_input)

    os.makedirs(article_folder, exist_ok=True)
    output_path = f'{article_folder}/03_LOCKED_BRIEF.md'
    with open(output_path, 'w') as f:
        f.write(brief)

    print(f'\n💾 Saved locally to: {output_path}')

    from tools.review_summary import generate_review_summary
    summary_text = generate_review_summary(
        step_name="Agent 1.3: Architect - Article 7 Brief",
        step_number=3,
        total_steps=8,
        article_folder=article_folder,
        topic="Zone 3: Expertise — Transform Knowledge Into Revenue",
        what_was_done="""Generated 3-5 angle options and framework pairings (Phase 1). You selected the preferred combination, then Phase 2 built the full Article 7 brief with loops, proof, CTA, and narrative flow.""",
        what_needs_review="""Please review the locked brief to ensure it reflects your chosen angle and framework. If you want to try another combination, re-run this script and pick a different option before proceeding to Title Generation.""",
        next_step="Title Generation Agent will use the approved brief to produce 20+ headline options."
    )
    print(summary_text)

    # Save to Google Drive
    try:
        from tools.google_drive_integration import GoogleDriveIntegration
        drive = GoogleDriveIntegration()

        base_folder_id = os.environ.get("GOOGLE_DRIVE_BASE_FOLDER_ID", "1-dZhiWh_-wtj3avmI9Ya6IO16eVyq_DL")
        article_name = "Article: Zone 3 - Expertise"
        article_drive_folder = drive.get_or_create_folder(article_name, base_folder_id)
        briefs_folder = drive.get_or_create_folder("Briefs & Outlines", article_drive_folder)

        doc_content = summary_text + "\n\n" + "="*70 + "\n\nLOCKED ARTICLE 7 BRIEF\n\n" + "="*70 + "\n\n" + brief
        doc_name = "Agent 1.3 - Architect (Angles & Brief)"
        result = drive.create_google_doc(doc_content, doc_name, briefs_folder)
        if result:
            doc_id, doc_link = result
            print(f'📄 Created Google Doc: {doc_link}')
    except Exception as e:
        print(f'⚠️  Could not create Google Doc: {e}')

    print('\n📄 Brief Preview:')
    preview = brief[:2000] if len(brief) > 2000 else brief
    print(preview)
    if len(brief) > 2000:
        print('\n... (truncated, full content in file)')


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""Run Agent 1.3: Architect (Angle & Framework Generator)"""

import sys
import os
sys.path.insert(0, '.')

from agents.prompts import ARCHITECT_SYSTEM_PROMPT
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model_name = "gemini-2.5-pro"


def call_agent(agent_name, system_prompt, user_input):
    """Call Gemini agent"""
    print(f"\n🤖 {agent_name} is thinking...")
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt
    )
    response = model.generate_content(user_input)
    print(f"✅ {agent_name} finished.")
    return response.text


def load_data(folder):
    """Load textual data from folder"""
    content = ''
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.endswith(('.md', '.txt')):
                with open(os.path.join(folder, file), 'r') as f:
                    content += f.read() + '\n\n'
    return content[:8000] if len(content) > 8000 else content


article_folder = 'output/article_1'
analysis_file = f'{article_folder}/02_analysis.md'

if not os.path.exists(analysis_file):
    print(f'❌ Analysis file not found: {analysis_file}')
    print('   Run Agent 1.2 first!')
    sys.exit(1)

with open(analysis_file, 'r') as f:
    analysis_content = f.read()

# Load additional data sources
titles = load_data('data/titles')
rules = load_data('data/rules')

architect_input = f"ANALYSIS:\n{analysis_content}\n\nTITLES:\n{titles}\n\nRULES:\n{rules}"

print('\n--- AGENT 1.3: ARCHITECT (Angles & Frameworks) ---')
brief = call_agent('Agent 1.3 (Architect)', ARCHITECT_SYSTEM_PROMPT, architect_input)

# Save brief locally
os.makedirs(article_folder, exist_ok=True)
output_path = f'{article_folder}/03_LOCKED_BRIEF.md'
with open(output_path, 'w') as f:
    f.write(brief)

print(f'\n💾 Saved locally to: {output_path}')

# Print review summary
from tools.review_summary import print_review_summary, generate_review_summary
summary_text = generate_review_summary(
    step_name="Agent 1.3: Architect - Article 7 Brief",
    step_number=3,
    total_steps=8,
    article_folder=article_folder,
    topic="Zone 3: Expertise — Transform Knowledge Into Revenue",
    what_was_done="""Generated 3-5 angle options (with contrarian hooks, emotional triggers, and positioning) and suggested 2-3 framework pairings for each. Built a full Article 7 brief including loops, framework placement, proof points, and CTA guidance.""",
    what_needs_review="""Please review:
1. The angle options – which resonates most with how you want to approach Zone 3?
2. The recommended framework pairings – do they align with Jay's Zone 3 methodology?
3. The locked Article 7 brief – does the structure feel strong? Are the loops, hooks, and CTA direction on point?

You can approve as-is, edit, or regenerate.""",
    next_step="Title Generation Agent will use the approved brief to produce 20+ headline options."
)
print(summary_text)

# Save to Google Drive (Briefs & Outlines)
try:
    from tools.google_drive_integration import GoogleDriveIntegration
    drive = GoogleDriveIntegration()

    base_folder_id = os.environ.get("GOOGLE_DRIVE_BASE_FOLDER_ID", "1-dZhiWh_-wtj3avmI9Ya6IO16eVyq_DL")
    article_name = "Article: Zone 3 - Expertise"
    article_drive_folder = drive.get_or_create_folder(article_name, base_folder_id)
    briefs_folder = drive.get_or_create_folder("Briefs & Outlines", article_drive_folder)

    doc_content = summary_text + "\n\n" + "="*70 + "\n\nLOCKED ARTICLE 7 BRIEF\n\n" + "="*70 + "\n\n" + brief
    doc_name = "Agent 1.3 - Architect (Angles & Brief)"
    result = drive.create_google_doc(doc_content, doc_name, briefs_folder)
    if result:
        doc_id, doc_link = result
        print(f'📄 Created Google Doc: {doc_link}')
except Exception as e:
    print(f'⚠️  Could not create Google Doc: {e}')

# Show preview
print('\n📄 Brief Preview:')
preview = brief[:2000] if len(brief) > 2000 else brief
print(preview)
if len(brief) > 2000:
    print('\n... (truncated, full content in file)')



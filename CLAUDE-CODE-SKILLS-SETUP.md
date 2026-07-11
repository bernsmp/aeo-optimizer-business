# Claude Code Skills Setup

## 🎯 Installing Anthropic Skills Repository

This guide will help you install all available skills from the [Anthropic Skills repository](https://github.com/anthropics/skills.git) to your Claude Code workspace.

---

## 📦 Available Skill Sets

The repository contains two main plugin sets:

1. **document-skills** - Document manipulation (Word, PDF, PowerPoint, Excel)
2. **example-skills** - Creative, development, and enterprise skills

---

## 🚀 Installation Steps

### Step 1: Add the Marketplace

In Claude Code, run this command:

```
/plugin marketplace add anthropics/skills
```

This registers the Anthropic skills repository as a plugin marketplace.

### Step 2: Install Document Skills

Install the document manipulation skills:

```
/plugin install document-skills@anthropic-agent-skills
```

**Includes:**
- **docx** - Create, edit, and analyze Word documents
- **pdf** - PDF manipulation toolkit (extract, create, merge, split)
- **pptx** - Create, edit, and analyze PowerPoint presentations
- **xlsx** - Create, edit, and analyze Excel spreadsheets

### Step 3: Install Example Skills

Install all the example skills:

```
/plugin install example-skills@anthropic-agent-skills
```

**Includes:**
- **algorithmic-art** - Create generative art using p5.js
- **canvas-design** - Design visual art in .png and .pdf formats
- **slack-gif-creator** - Create animated GIFs for Slack
- **web-artifacts-builder** - Build HTML artifacts with React, Tailwind, shadcn/ui
- **mcp-builder** - Guide for creating MCP servers
- **webapp-testing** - Test web apps using Playwright
- **brand-guidelines** - Apply Anthropic's brand colors and typography
- **internal-comms** - Write internal communications
- **theme-factory** - Style artifacts with professional themes
- **skill-creator** - Guide for creating effective skills
- **template-skill** - Template for new skills

---

## ✅ Verification

After installation, you can verify skills are available by:

1. Asking Claude Code to use a specific skill (e.g., "Use the PDF skill to extract text from document.pdf")
2. Checking the plugin marketplace in Claude Code
3. Skills should be available across all your projects automatically

---

## 📝 Usage Examples

Once installed, you can use skills in any Claude Code project:

### Document Skills:
- "Use the PDF skill to extract form fields from invoice.pdf"
- "Use the docx skill to create a Word document with tracked changes"
- "Use the xlsx skill to analyze data in spreadsheet.xlsx"

### Example Skills:
- "Use the algorithmic-art skill to create generative art"
- "Use the web-artifacts-builder skill to create a React component"
- "Use the theme-factory skill to apply a professional theme"

---

## 🔧 Alternative: Manual Installation via UI

If you prefer using the UI:

1. Select `Browse and install plugins` in Claude Code
2. Select `anthropic-agent-skills`
3. Select `document-skills` → `Install now`
4. Select `example-skills` → `Install now`

---

## 📚 Reference

- **Repository:** https://github.com/anthropics/skills.git
- **Documentation:** See repository README for detailed skill descriptions
- **Skills API:** https://docs.anthropic.com/en/docs/build-with-skills

---

## 🎯 What This Enables

Once installed, these skills will be available across **all your Claude Code projects**, including:

- ✅ **AEO Optimizer Business** projects
- ✅ **Louie Bernstein** website build
- ✅ **Paw Origins** dashboard
- ✅ Any future projects

Skills enhance Claude's capabilities for:
- Document manipulation and analysis
- Creative design and art generation
- Web development and testing
- Enterprise workflows
- And much more!

---

**Note:** Skills are installed at the Claude Code workspace level, so they'll be available in all projects automatically. No need to reinstall for each project!


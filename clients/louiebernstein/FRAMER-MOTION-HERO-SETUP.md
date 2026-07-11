# Framer Motion Hero Component Setup

## 🎯 Component Overview

This document provides instructions for integrating the animated background ripple effect hero component using Framer Motion.

**Component:** `BackgroundCells` - Animated background with interactive cell effects
**Location:** `components/ui/background-ripple-effect.tsx` (or `components/background-ripple-effect.tsx`)

---

## 📋 Prerequisites

### 1. Project Setup Requirements

The project must support:
- ✅ **shadcn/ui** project structure
- ✅ **Tailwind CSS**
- ✅ **TypeScript**

### 2. If Project Doesn't Have These:

#### Setup shadcn/ui:
```bash
npx shadcn@latest init
```

Follow the prompts:
- **Style:** Default
- **Base color:** Slate
- **CSS variables:** Yes
- **Components directory:** `components/ui` (IMPORTANT!)

#### Install Tailwind CSS (if not already installed):
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

#### TypeScript (should be included with Next.js):
```bash
# TypeScript is included with Next.js TypeScript template
# If not, install:
npm install -D typescript @types/react @types/node
```

---

## 📁 Component Path Structure

### Default shadcn Structure:
```
components/
└── ui/              # shadcn components go here
    ├── button.tsx
    ├── card.tsx
    └── background-ripple-effect.tsx  # ← Our component
```

### Why `/components/ui` is Important:
- **shadcn convention:** All shadcn components are in `/components/ui`
- **Consistency:** Matches shadcn CLI expectations
- **Organization:** Separates custom components from shadcn components
- **Utils import:** The `cn` utility from `@/lib/utils` expects this structure

### Alternative Structure (if not using shadcn):
If you're not using shadcn, you can place it in:
```
components/
└── background-ripple-effect.tsx
```

But you'll need to ensure `@/lib/utils` exists for the `cn` function.

---

## 🔧 Installation Steps

### Step 1: Install Dependencies

```bash
npm install framer-motion
```

### Step 2: Ensure Utils File Exists

Create or verify `lib/utils.ts` exists:

```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

If it doesn't exist, install required dependencies:
```bash
npm install clsx tailwind-merge
```

### Step 3: Create Component File

**Path:** `components/ui/background-ripple-effect.tsx`

Copy the component code (already created in this directory).

### Step 4: Update Hero Component

Update `components/Hero.tsx` to use the BackgroundCells component:

```tsx
"use client";

import { BackgroundCells } from "@/components/ui/background-ripple-effect";

export default function Hero() {
  return (
    <BackgroundCells className="bg-slate-950">
      <div className="text-center">
        <h1 className="md:text-2xl lg:text-7xl font-medium bg-clip-text text-transparent bg-gradient-to-b from-neutral-100 to-neutral-400">
          Fractional Sales Leader
        </h1>
        <p className="mt-4 text-xl text-neutral-300">
          Less Spend. More Sales.
        </p>
        <p className="mt-2 text-lg text-neutral-400">
          I'll organize, optimize, and train your sales team, so you don't have to.
        </p>
      </div>
    </BackgroundCells>
  );
}
```

---

## 🎨 Customization Options

### Background Color
Change the background color by modifying the `className` prop:

```tsx
<BackgroundCells className="bg-slate-950">  {/* Dark background */}
<BackgroundCells className="bg-neutral-900"> {/* Alternative dark */}
<BackgroundCells className="bg-blue-950">   {/* Blue tint */}
```

### Content Positioning
Adjust the content position by modifying the wrapper div:

```tsx
<div className="relative z-50 mt-40 pointer-events-none select-none">
  {/* Change mt-40 to adjust vertical position */}
  {/* mt-20 = less space, mt-60 = more space */}
</div>
```

### Text Styling
Customize the text gradient:

```tsx
<h1 className="md:text-2xl lg:text-7xl font-medium bg-clip-text text-transparent bg-gradient-to-b from-neutral-100 to-neutral-400">
  {/* Change gradient colors: */}
  {/* from-blue-100 to-blue-400 = blue gradient */}
  {/* from-white to-gray-300 = white to gray */}
</h1>
```

### Cell Colors
Modify cell border colors in the component:

```tsx
<Pattern cellClassName="border-blue-600 relative z-[100]" />  {/* Active cells */}
<Pattern className="opacity-[0.5]" cellClassName="border-neutral-700" />  {/* Background cells */}
```

---

## 📝 Usage Example

### Basic Usage:
```tsx
import { BackgroundCells } from "@/components/ui/background-ripple-effect";

export default function Hero() {
  return (
    <BackgroundCells className="bg-slate-950">
      <h1>Your Hero Content</h1>
    </BackgroundCells>
  );
}
```

### With Louie's Content:
```tsx
import { BackgroundCells } from "@/components/ui/background-ripple-effect";

export default function Hero() {
  return (
    <BackgroundCells className="bg-slate-950">
      <div className="text-center space-y-4">
        <h1 className="md:text-4xl lg:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-neutral-100 to-neutral-400">
          Fractional Sales Leader
        </h1>
        <p className="text-2xl text-neutral-300 font-medium">
          Less Spend. More Sales.
        </p>
        <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
          I'll organize, optimize, and train your sales team, so you don't have to.
        </p>
        <div className="flex gap-4 justify-center mt-8">
          <a 
            href="https://www.linkedin.com/in/sales-processes/" 
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Learn More
          </a>
          <a 
            href="https://calendly.com/louiebernstein/30minutes" 
            className="px-6 py-3 bg-neutral-700 text-white rounded-lg hover:bg-neutral-600 transition"
          >
            Schedule Discussion
          </a>
        </div>
      </div>
    </BackgroundCells>
  );
}
```

---

## ⚙️ Component Features

### Interactive Effects:
- **Mouse Tracking:** Cells light up as mouse moves
- **Click Effects:** Ripple animation on cell click
- **Hover Effects:** Cells animate on hover
- **Smooth Animations:** Framer Motion powered transitions

### Performance:
- **Optimized:** Uses CSS masks for performance
- **Responsive:** Works on all screen sizes
- **Accessible:** Maintains pointer-events for content

---

## 🐛 Troubleshooting

### Issue: `cn` function not found
**Solution:** Ensure `lib/utils.ts` exists with the `cn` function, or install dependencies:
```bash
npm install clsx tailwind-merge
```

### Issue: Component not animating
**Solution:** Ensure Framer Motion is installed:
```bash
npm install framer-motion
```

### Issue: Tailwind classes not working
**Solution:** Verify Tailwind is configured in `tailwind.config.ts`:
```typescript
content: [
  './app/**/*.{ts,tsx}',
  './components/**/*.{ts,tsx}',
]
```

### Issue: Import path error
**Solution:** Check your `tsconfig.json` paths:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

---

## ✅ Checklist

- [ ] Install framer-motion: `npm install framer-motion`
- [ ] Verify shadcn/ui setup (or install: `npx shadcn@latest init`)
- [ ] Create `components/ui/` directory (if using shadcn)
- [ ] Create `lib/utils.ts` with `cn` function (if doesn't exist)
- [ ] Copy `background-ripple-effect.tsx` to `components/ui/`
- [ ] Update Hero component to use BackgroundCells
- [ ] Test component renders correctly
- [ ] Test animations work on hover/click
- [ ] Verify responsive design

---

## 🎯 Integration with Build Instructions

This component should be integrated into the Hero section of the homepage. Update the build instructions to:

1. Install framer-motion dependency
2. Create the component file
3. Update Hero component to use BackgroundCells
4. Style the hero content appropriately

---

**Component is ready to use!** 🚀



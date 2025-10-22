# CSS Language Service Configuration
# To fix "Unknown at rule @tailwind" errors in your IDE:

## Option 1: VS Code Settings (if using VS Code)
Create/update `.vscode/settings.json` in your project root:

```json
{
  "css.customData": [
    {
      "version": 1.1,
      "atDirectives": [
        {
          "name": "@tailwind",
          "description": "Use the @tailwind directive to insert Tailwind's base, components, utilities and variants styles into your CSS.",
          "references": [
            {
              "name": "Tailwind CSS Documentation",
              "url": "https://tailwindcss.com/docs/functions-and-directives#tailwind"
            }
          ]
        },
        {
          "name": "@apply",
          "description": "Use @apply to inline any existing utility classes into your own custom CSS.",
          "references": [
            {
              "name": "Tailwind CSS Documentation",
              "url": "https://tailwindcss.com/docs/functions-and-directives#apply"
            }
          ]
        },
        {
          "name": "@layer",
          "description": "Use the @layer directive to tell Tailwind which 'bucket' a set of custom styles belong to.",
          "references": [
            {
              "name": "Tailwind CSS Documentation",
              "url": "https://tailwindcss.com/docs/functions-and-directives#layer"
            }
          ]
        }
      ]
    }
  ],
  "tailwindCSS.includeLanguages": {
    "javascript": "html",
    "html": "html"
  }
}
```

## Option 2: Alternative Solutions

### For VS Code users:
1. Install the "Tailwind CSS IntelliSense" extension by Bradlc
2. This extension provides autocomplete and recognizes Tailwind directives

### For other editors:
- The build system (Vite) correctly processes Tailwind directives
- The linting errors are cosmetic and don't affect functionality
- Your CSS will compile correctly when you run the development server

## Current Status:
✅ Frontend server running on http://localhost:3001
✅ Tailwind CSS properly configured and processing
✅ All mobile responsiveness features working
✅ Mock backend API working correctly

The "Unknown at rule @tailwind" warnings are IDE-specific and don't affect the actual functionality of your application.

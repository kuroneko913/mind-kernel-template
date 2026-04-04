---
description: Update Mind Kernel model with new patches
---

This workflow guides you through the process of updating the Mind Kernel model, which is now split into multiple modules for better manageability.

1. **Pull Latest Changes**
   - Ensure you are on the main branch and pull the latest changes.
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Read Meta Configuration**
   - **MANDATORY**: Read `kernel/meta.json` to understand the latest `publication_policy`, `system_guidelines`, and `module_definitions`.
   - Ensure your updates comply with these rules.

3. **Identify the Target Module**
   - Determine which file needs updating:
     - `kernel/identity.json`: Core identity/cognition (Stable)
     - `kernel/backlog.json`: Active issues/experiments (High churn)
     - `kernel/patterns.json`: Acquired patterns (Library)
     - `kernel/meta.json`: Design rules/AI instructions (System)

4. **Apply Changes**
   - Update the relevant JSON file(s).
   - If a challenge in `backlog.json` is completed, move the resulting logic to `patterns.json` and remove it from the backlog.

5. **Verify Growth**
   - Run the semantic analysis script to ensure your changes are correctly evaluated as growth.
   ```bash
   python3 scripts/analyze_growth.py --commit HEAD
   ```

6. **Commit and Tag**
   - Commit the changes and create a git tag matching the newest version string.

   ```bash
   git add .
   git commit -m "feat: [Module] Description of change"
   git tag <version-string>
   git push origin main --tags
   ```
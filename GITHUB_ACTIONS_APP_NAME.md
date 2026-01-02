# GitHub Actions - Configuring APP_NAME

This guide explains how to customize the application name (`APP_NAME`) when deploying through GitHub Actions.

---

## 📋 Quick Setup

### **Step 1: Go to Repository Settings**

1. Navigate to your GitHub repository
2. Click **Settings** (top right)
3. In the left sidebar, click **Secrets and variables** → **Actions**

### **Step 2: Add APP_NAME Variable**

1. Click the **Variables** tab (not Secrets!)
2. Click **New repository variable**
3. Name: `APP_NAME`
4. Value: Your custom app name (e.g., `hotel-manager`, `restaurant-pos`, `my-app`)
5. Click **Add variable**

### **Step 3: Deploy!**

Go to **Actions** tab and run your workflow. It will use your custom `APP_NAME`.

---

## 🎯 How It Works

### **Default Behavior (Without Setting APP_NAME)**

If you don't set `APP_NAME`, it defaults to `basic-auth`:

- **Dev**: Deploys to stack `basic-auth-dev`
- **Staging**: Deploys to stack `basic-auth-staging`
- **Prod**: Deploys to stack `basic-auth-prod`

### **Custom APP_NAME**

If you set `APP_NAME=hotel-manager`:

- **Dev**: Deploys to stack `hotel-manager-dev`
- **Staging**: Deploys to stack `hotel-manager-staging`
- **Prod**: Deploys to stack `hotel-manager-prod`

**All resources get renamed:**
- Tables: `hotel-manager-dev-users`, `hotel-manager-dev-tokens`, etc.
- Lambda: `hotel-manager-dev-api`
- API Gateway: `hotel-manager-dev-api`

---

## 🏗️ Multi-Client Setup

### **Scenario: Deploying for Different Clients**

You have **one codebase**, but want separate deployments for different clients:

#### **Option 1: Use Branches**

Create separate branches for each client:

```bash
# Branch for Client A (Hotel)
git checkout -b client/hotel
# Set APP_NAME=hotel-manager in GitHub variables for this branch

# Branch for Client B (Restaurant)
git checkout -b client/restaurant
# Set APP_NAME=restaurant-pos in GitHub variables for this branch
```

#### **Option 2: Use Multiple Repositories**

Fork the repo for each client and set different `APP_NAME` in each repo.

#### **Option 3: Use Workflow Inputs (Advanced)**

Modify the workflow to accept `APP_NAME` as input:

```yaml
on:
  workflow_dispatch:
    inputs:
      app_name:
        description: 'Application name'
        required: false
        default: 'basic-auth'

env:
  APP_NAME: ${{ github.event.inputs.app_name || vars.APP_NAME || 'basic-auth' }}
```

---

## ✅ Validation Rules

**APP_NAME must:**
- Be **lowercase**
- Use **alphanumeric** characters and **hyphens** only
- Start and end with an **alphanumeric** character
- Examples:
  - ✅ `hotel-manager`
  - ✅ `my-app-123`
  - ✅ `restaurant-pos`
  - ❌ `HotelManager` (uppercase not allowed)
  - ❌ `-myapp` (can't start with hyphen)
  - ❌ `my_app` (underscores not allowed)

---

## 🔐 Secrets vs Variables

### **Use Variables for APP_NAME**
- ✅ Variables are for **non-sensitive** configuration
- ✅ `APP_NAME` is not a secret
- ✅ Set it in **Secrets and variables → Actions → Variables**

### **Use Secrets for Sensitive Data**
- 🔒 JWT_SECRET
- 🔒 REFRESH_TOKEN_SECRET
- 🔒 MASTER_SECRET_KEY
- 🔒 AWS_ACCESS_KEY_ID
- 🔒 AWS_SECRET_ACCESS_KEY

---

## 📊 Example Deployments

### **Example 1: Hotel Management System**

**Setup:**
- `APP_NAME=hotel-manager`

**Result:**
```
Stack: hotel-manager-prod
Tables:
  - hotel-manager-prod-users
  - hotel-manager-prod-tokens
Lambda: hotel-manager-prod-api
API: https://xxx.execute-api.region.amazonaws.com/prod/
```

### **Example 2: Multiple Environments**

Same app, different environments:

```
APP_NAME=my-app ENVIRONMENT=dev   → my-app-dev
APP_NAME=my-app ENVIRONMENT=staging → my-app-staging
APP_NAME=my-app ENVIRONMENT=prod → my-app-prod
```

### **Example 3: Multiple Clients in Same AWS Account**

```
Client A: APP_NAME=hotel-abc    → hotel-abc-prod
Client B: APP_NAME=hotel-xyz    → hotel-xyz-prod
Client C: APP_NAME=gym-fit      → gym-fit-prod
```

All coexist without conflicts!

---

## 🛠️ Troubleshooting

### **Problem: Workflow still uses `basic-auth`**

**Solution:** Make sure you added `APP_NAME` as a **Variable**, not a Secret.

### **Problem: Stack name mismatch error**

**Solution:** If you're changing `APP_NAME` after deployment:
1. Delete the old stack: `aws cloudformation delete-stack --stack-name basic-auth-dev`
2. Or deploy with new name (creates new stack)

### **Problem: Permission denied**

**Solution:** Ensure your AWS credentials have permissions to create resources with the new names.

---

## 🎓 Summary

1. **Add `APP_NAME` variable** in GitHub Settings → Actions → Variables
2. **Value**: Your custom app name (lowercase, alphanumeric + hyphens)
3. **Deploy**: Run your workflow - it uses the custom name automatically
4. **Result**: All resources named `{APP_NAME}-{ENVIRONMENT}-{resource}`

**No code changes needed!** The workflows automatically use the variable.

---

## 📞 Need Help?

- Check [template.yaml](template.yaml) to see how `AppName` parameter is used
- Check [.github/workflows/](. github/workflows/) to see how workflows reference `APP_NAME`
- Review [deploy-sam.sh](deploy-sam.sh) for manual deployment with custom names

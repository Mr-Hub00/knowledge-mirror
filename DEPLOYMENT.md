# Django Render Deployment Guide

## 1. Save and Stage Your Changes

Make sure all your code (especially `settings.py`) is saved.

```sh
git add .
```

## 2. Commit Your Changes

Write a clear commit message:

```sh
git commit -m "Update settings.py: auto-allow Render host, fix ALLOWED_HOSTS/CSRF"
```

## 3. Push to Your Remote Branch

Replace `knowledge` with your branch name if different:

```sh
git push origin knowledge
```

## 4. Trigger a Clean Deploy on Render

1. Go to your [Render dashboard](https://dashboard.render.com/).
2. Select your service.
3. Click **Manual Deploy**.
4. Choose **Clear build cache & deploy**.

## 5. Set/Check Environment Variables on Render

In your Render service → **Environment** tab, set:

- **ALLOWED_HOSTS**
  ```
  iamhub-fresh-b0gi.onrender.com,iamhub.net,www.iamhub.net,.onrender.com
  ```
- **CSRF_TRUSTED_ORIGINS**
  ```
  https://iamhub-fresh-b0gi.onrender.com,https://iamhub.net,https://www.iamhub.net,https://*.onrender.com
  ```
- **DJANGO_SECRET_KEY** (should already be set and strong)

## 6. Confirm Static Files Are Collected

Your `render.yaml` should include:

```yaml
buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput
```

## 7. Check the Build Logs

Look for lines like:

```
ALLOWED_HOSTS: [...]
CSRF_TRUSTED_ORIGINS: [...]
```

Make sure your Render domain(s) are present in both lists.

## 8. Test Your Site

- Visit: `https://iamhub-fresh-b0gi.onrender.com/storacha/health`
- Visit: `https://iamhub-fresh-b0gi.onrender.com/admin`

You should **not** see any `DisallowedHost` errors.

## 9. (Optional) Remove Debug Prints

After confirming everything works, remove or comment out the `print()` lines in `settings.py`:

```python
# print("ALLOWED_HOSTS:", ALLOWED_HOSTS)
# print("CSRF_TRUSTED_ORIGINS:", CSRF_TRUSTED_ORIGINS)
```

Then repeat steps 1–4 to deploy the cleanup.

---

**Troubleshooting:**

- If you see `DisallowedHost`, check the build logs for what Django sees in `ALLOWED_HOSTS`.
- Make sure your environment variables are set with **no quotes, no spaces, no extra commas**.
- If you change environment variables, always redeploy with **Clear build cache**.

---

**You’re ready for production!
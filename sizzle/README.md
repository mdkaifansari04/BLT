<h1 align="center">🔥 Sizzle - Daily Check-in & Time Tracking</h1>
<h3 align="center">Stay productive, track your time, and keep your team in sync</h3>

<p align="center">
  <strong>A powerful Django app for daily status reports and time logging within the OWASP BLT platform</strong>
</p>

---

## 📖 Overview

**Sizzle** is a Django application designed to help teams and individuals stay productive through daily check-ins and time tracking. It's integrated into the OWASP BLT platform to provide developers and security researchers with tools to track their work, share daily progress, and maintain accountability.

### ✨ Key Features

- ⏱️ **Time Tracking** - Log time spent on GitHub issues and tasks
- 📝 **Daily Status Reports** - Share what you did, what's next, and any blockers
- 🏆 **Leaderboard** - See top contributors based on time logged
- 📊 **Reports & Analytics** - View individual and team progress over time
- ⏰ **Reminder Settings** - Get daily reminders to submit your check-ins
- 🎯 **Goal Tracking** - Mark goals as accomplished and track your mood
- 🔗 **GitHub Integration** - Link time logs to GitHub issues

---

## 🏗️ Architecture

Sizzle is organized as a standalone Django app within the BLT project with the following structure:

```
sizzle/
├── __init__.py
├── admin.py          # Django admin configuration
├── apps.py           # App configuration
├── models.py         # Data models
├── views.py          # View logic
├── urls.py           # URL routing
├── tests.py          # Tests
├── templates/        # HTML templates
│   ├── sizzle.html
│   ├── checkin.html
│   ├── add_sizzle_checkin.html
│   ├── checkin_detail.html
│   ├── sizzle_daily_status.html
│   ├── sizzle_docs.html
│   ├── time_logs.html
│   └── user_sizzle_report.html
└── migrations/       # Database migrations
```

---

## 📊 Data Models

### TimeLog
Tracks time spent on tasks and GitHub issues.

**Fields:**
- `user` - User who logged the time (ForeignKey to User)
- `organization` - Optional organization (ForeignKey to Organization)
- `start_time` - When the work started (DateTimeField)
- `end_time` - When the work ended (DateTimeField, nullable)
- `duration` - Calculated duration (DurationField, auto-calculated)
- `github_issue_url` - Link to GitHub issue (URLField, optional)
- `created` - Timestamp of log creation (DateTimeField)

**Methods:**
- `save()` - Automatically calculates duration when end_time is set

### DailyStatusReport
Daily check-in reports for team synchronization.

**Fields:**
- `user` - User submitting the report (ForeignKey to User)
- `date` - Date of the report (DateField)
- `previous_work` - What was done yesterday (TextField)
- `next_plan` - What will be done today (TextField)
- `blockers` - Any blockers or issues (TextField)
- `goal_accomplished` - Whether goals were met (BooleanField)
- `current_mood` - User's current mood (CharField, default: "Happy 😊")
- `created` - Timestamp of report creation (DateTimeField)

**Meta:**
- Unique constraint on `(user, date)` - one report per user per day
- Ordered by `-date` (most recent first)
- Indexed on `(user, date)` for performance

### ReminderSettings
User preferences for daily reminder notifications.

**Fields:**
- `user` - User (OneToOneField to User)
- `reminder_time` - Time to send reminders in user's timezone (TimeField)
- `reminder_time_utc` - Time in UTC (TimeField, auto-calculated)
- `timezone` - User's timezone (CharField, default: "UTC")
- `is_active` - Enable/disable reminders (BooleanField)
- `last_reminder_sent` - Last reminder timestamp (DateTimeField, nullable)
- `created_at` - When settings were created (DateTimeField)
- `updated_at` - When settings were last updated (DateTimeField)

**Methods:**
- `save()` - Automatically converts reminder_time to UTC
- `get_timezone_choices()` - Returns list of available timezones

---

## 🛣️ URL Routes

All Sizzle routes are prefixed with `/sizzle/`:

| Route | View | Description |
|-------|------|-------------|
| `/sizzle/` | `sizzle` | Main dashboard with leaderboard |
| `/sizzle/check-in/` | `checkIN` | View all team check-ins |
| `/sizzle/add-sizzle-checkin/` | `add_sizzle_checkIN` | Add a new check-in |
| `/sizzle/check-in/<id>/` | `checkIN_detail` | View specific check-in details |
| `/sizzle/sizzle-docs/` | `sizzle_docs` | Documentation page |
| `/sizzle/api/timelogsreport/` | `TimeLogListAPIView` | API endpoint for time logs |
| `/sizzle/time-logs/` | `TimeLogListView` | View user's time logs |
| `/sizzle/sizzle-daily-log/` | `sizzle_daily_log` | Submit daily status report |
| `/sizzle/user-sizzle-report/<username>/` | `user_sizzle_report` | View user's report |

---

## 🎨 Views & Functionality

### Main Dashboard (`sizzle`)
- Displays leaderboard with top contributors by time logged
- Shows user's most recent time log entry
- Aggregates and formats total duration
- Integrates with GitHub to display issue titles

### Check-in System (`checkIN`, `add_sizzle_checkIN`, `checkIN_detail`)
- View all team check-ins with date range filtering
- Add new daily status reports
- View detailed check-in information
- See previous day's report for continuity

### Time Tracking (`TimeLogListView`, `TimeLogListAPIView`)
- Track active time logs
- View historical time logs
- API endpoint for programmatic access
- Integration with organizations
- Token-based authentication support

### Daily Logs (`sizzle_daily_log`)
- Submit daily status reports
- Track goal accomplishment
- Record current mood
- View report history

### User Reports (`user_sizzle_report`)
- View individual user's time tracking history
- Grouped by date with aggregated durations
- Display GitHub issue information

---

## 🚀 Usage

### For Users

#### Logging Time
1. Navigate to `/sizzle/time-logs/`
2. Start a time log with a GitHub issue URL
3. Stop the timer when done
4. Duration is automatically calculated

#### Daily Check-ins
1. Go to `/sizzle/add-sizzle-checkin/`
2. Fill in:
   - What you worked on yesterday
   - What you plan to work on today
   - Any blockers
   - Whether you accomplished your goals
   - Your current mood
3. Submit the report

#### Viewing Progress
- Check the leaderboard at `/sizzle/`
- View your time logs at `/sizzle/time-logs/`
- See team check-ins at `/sizzle/check-in/`

### For Administrators

#### Django Admin
Access the admin panel to manage:
- Time logs
- Daily status reports
- Reminder settings

#### API Integration
Use the API endpoint `/sizzle/api/timelogsreport/` with authentication tokens to programmatically access time log data.

**Query Parameters:**
- `start_date` - Start date in ISO format
- `end_date` - End date in ISO format

**Authentication:**
- Token-based authentication required
- Include token in Authorization header

---

## 🔧 Configuration

### Settings Integration

Sizzle is configured in `blt/settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'sizzle',
    # ...
]
```

### URL Configuration

In `blt/urls.py`:

```python
urlpatterns = [
    # ...
    path("sizzle/", include("sizzle.urls")),
    # ...
]
```

---

## 🗄️ Database Setup

Run migrations to set up Sizzle tables:

```bash
python manage.py makemigrations sizzle
python manage.py migrate sizzle
```

---

## 🔌 Dependencies

Sizzle integrates with the following BLT components:

- **User Model** - From `django.contrib.auth.models`
- **Organization Model** - From `website.models`
- **Utilities** - `format_timedelta`, `get_github_issue_title` from `website.utils`

---

## 🎯 Best Practices

### Time Logging
- Always link time logs to GitHub issues for better tracking
- Stop timers promptly to ensure accurate duration
- Review your time logs regularly

### Daily Check-ins
- Be honest about blockers - the team can help!
- Keep reports concise but informative
- Submit check-ins consistently for best results

### Team Collaboration
- Review team check-ins to stay synchronized
- Use the leaderboard for friendly competition
- Celebrate accomplishments together

---

## 🐛 Troubleshooting

### Time Log Not Saving
- Ensure `start_time` is before `end_time`
- Check that GitHub issue URL is valid
- Verify user is authenticated

### Daily Report Already Exists
- Only one report per user per day is allowed
- Edit existing report instead of creating a new one

### Reminders Not Working
- Check `ReminderSettings.is_active` is `True`
- Verify timezone is correctly set
- Ensure `reminder_time_utc` is calculated properly

---

## 🤝 Contributing

Contributions to Sizzle are welcome! Please follow the BLT contributing guidelines:

1. Read the [BLT Contributing Guide](../CONTRIBUTING.md)
2. Follow code style guidelines (Black, isort, ruff)
3. Run `pre-commit` before committing
4. Add tests for new features
5. Update this README if adding new functionality

---

## 📝 License

Sizzle is part of the OWASP BLT project and is licensed under **AGPL-3.0**. See [LICENSE.md](../LICENSE.md) for details.

---

## 📧 Support

- 🌐 **BLT Website**: [owaspblt.org](https://owaspblt.org)
- 💬 **Slack**: [Join OWASP Slack](https://owasp.org/slack/invite)
- 🐛 **Issues**: [GitHub Issues](https://github.com/OWASP-BLT/BLT/issues)

---

<p align="center">
  <strong>⭐ Part of the OWASP BLT Platform</strong><br>
  Made with ❤️ by the OWASP BLT Community
</p>

# Money Roundup - Project Completion Plan

**Last Updated**: 2026-01-26

## Project Overview
Money Roundup is a financial advice application that analyzes user spending habits and provides personalized guidance based on their financial goals. The app integrates with banks via Plaid and sends daily email notifications about spending patterns.

---

## Current State Summary

### What's Working ✅
- **User authentication**: Registration, email verification, password reset (JWT-based)
- **Plaid bank linking**: Users can securely connect their bank accounts
- **Account viewing**: Can fetch and display linked accounts
- **Email infrastructure**: Both development (SMTP) and production (AWS SES) configured

### Tech Stack
- **Backend**: FastAPI, SQLAlchemy (async), SQLite (needs PostgreSQL for production)
- **Frontend**: React 18 + TypeScript, Vite, Tailwind CSS
- **External Services**: Plaid API (banking), AWS SES (email)
- **Deployment**: Docker + AWS Beanstalk ready

---

## Critical Missing Features ❌

### 1. Daily Spending Email Digest (CORE FEATURE - PRIORITY 1)
**Status**: Infrastructure exists but logic is stubbed out
- Background scheduler commented out in `main.py:11`
- `fetch_transactions()` function incomplete
- No transaction aggregation or email composition logic
- APScheduler configured but never runs

**What's needed**:
- Enable scheduler in main.py
- Implement transaction fetching and storage
- Build spending aggregation logic
- Create email templates for daily digest
- Add transaction categorization

### 2. Goals/Budgeting System (PRIORITY 2)
**Status**: Partially built then removed from main branch
- Evidence: Commit `e8080ea` mentions "Goal CRUD"
- Test files exist in `__pycache__` but actual code removed
- Essential for "financial advice based on goals"

**What's needed**:
- Restore Goal model and CRUD operations
- Create API endpoints for goal management
- Build frontend UI for setting/viewing goals
- Implement goal vs. actual spending comparison

### 3. Financial Analysis/Advice Logic (PRIORITY 3)
**Status**: Completely missing
- No spending pattern analysis
- No comparison against goals
- No personalized advice generation
- No intelligent transaction categorization

**What's needed**:
- Transaction categorization engine
- Spending trend analysis
- Goal achievement tracking
- Recommendation algorithm (rule-based or ML)
- Insights generation (e.g., "You spent 20% more on dining")

---

## Important Issues to Address ⚠️

### Security Concerns
- [ ] Move hardcoded credentials from `.env` to environment variables
- [ ] Tighten CORS policy (currently allows all origins `["*"]`)
- [ ] Add rate limiting on API endpoints
- [ ] Remove committed secrets (Plaid, Google OAuth, email passwords)
- [ ] Add input sanitization and validation

### Database Issues
- [ ] **CRITICAL**: Implement Alembic migrations (tables currently drop/recreate on startup)
- [ ] Migrate from SQLite to PostgreSQL for production
- [ ] Remove legacy `UserOld` model
- [ ] Fix mixed sync/async session usage
- [ ] Standardize ID types (UUID vs string)

### Frontend Issues
- [ ] Add loading states for all async operations
- [ ] Implement proper error handling (beyond alerts)
- [ ] Add password confirmation validation
- [ ] Fix hardcoded backend URLs
- [ ] Add success feedback for user actions
- [ ] Make URLs consistent (currently mixing 8000 and 8080)

### Disabled Features
- [ ] Enable Google OAuth (code commented out but credentials exist)
- [ ] Uncomment background scheduler startup
- [ ] Test and verify AWS Beanstalk deployment

### Code Quality
- [ ] Remove unused imports
- [ ] Clean up dead code (e.g., unused helper functions in account router)
- [ ] Remove console.log statements from frontend
- [ ] Standardize error handling patterns
- [ ] Add API documentation (Swagger/OpenAPI)
- [ ] Fix inconsistent route prefixes

---

## Implementation Roadmap

### Phase 1: Core Functionality (Make it work)
**Goal**: Get the MVP working end-to-end

1. **Enable Background Scheduler**
   - Uncomment `setup_app()` in `main.py:11`
   - Test scheduler starts correctly
   - Verify job runs on schedule

2. **Implement Transaction Fetching**
   - Complete `fetch_transactions()` function
   - Store transactions in database (create Transaction model)
   - Handle Plaid API pagination
   - Add error handling for API failures

3. **Build Daily Email Digest**
   - Aggregate spending data by day/category
   - Calculate totals and comparisons
   - Create email templates (HTML + plain text)
   - Test email delivery via both SMTP and SES

4. **Add Database Migrations**
   - Install and configure Alembic
   - Create initial migration from current schema
   - Add migration for Transaction model
   - Document migration workflow

**Estimated Effort**: 2-3 focused sessions

### Phase 2: Financial Intelligence (Make it useful)
**Goal**: Turn data into insights

5. **Restore Goals Feature**
   - Recreate Goal model (fields: category, amount, period, user_id)
   - Build CRUD API endpoints
   - Add frontend UI for goal management
   - Store and retrieve goals per user

6. **Add Spending Analysis**
   - Compare actual spending vs. goals
   - Identify spending trends (weekly, monthly)
   - Calculate category breakdowns
   - Detect unusual spending patterns

7. **Generate Financial Advice**
   - Create recommendation engine (start with rule-based)
   - Examples:
     - "You're 20% over budget on dining this month"
     - "You've saved $150 more than last month"
     - "Consider reducing entertainment spending by $50"
   - Include advice in daily emails

8. **Transaction Categorization**
   - Use Plaid's category data (if available)
   - Build fallback categorization logic
   - Allow users to recategorize transactions
   - Learn from user corrections

**Estimated Effort**: 4-5 focused sessions

### Phase 3: Polish (Make it production-ready)
**Goal**: Secure, performant, user-friendly

9. **Security Hardening**
   - Move all secrets to environment variables
   - Configure CORS with specific allowed origins
   - Add rate limiting (e.g., Flask-Limiter or SlowAPI)
   - Implement request validation on all endpoints
   - Add security headers

10. **Improve Frontend UX**
    - Add loading spinners/skeletons
    - Implement toast notifications for success/errors
    - Add form validation with helpful error messages
    - Create confirmation dialogs for destructive actions
    - Improve responsive design

11. **Switch to PostgreSQL**
    - Update database configuration
    - Test migrations with PostgreSQL
    - Update Docker Compose for local Postgres
    - Document connection setup

12. **API Documentation**
    - Enable FastAPI's automatic Swagger docs
    - Add docstrings to all endpoints
    - Document request/response schemas
    - Add example requests

13. **Comprehensive Testing**
    - Add unit tests for business logic
    - Create integration tests for API endpoints
    - Add frontend tests (React Testing Library)
    - Set up CI/CD for automated testing
    - Aim for >80% coverage

**Estimated Effort**: 5-6 focused sessions

### Phase 4: Nice-to-Haves (Make it delightful)
**Goal**: Extra features that enhance the experience

14. **Enable Google OAuth**
    - Uncomment OAuth code
    - Test OAuth flow end-to-end
    - Handle OAuth errors gracefully
    - Add "Sign in with Google" button

15. **Data Visualizations**
    - Add charts library (e.g., Recharts, Chart.js)
    - Create spending over time graphs
    - Show category breakdowns as pie/bar charts
    - Add trend lines for goals

16. **Mobile Responsive Design**
    - Test on various screen sizes
    - Optimize touch interactions
    - Consider PWA features

17. **Export Functionality**
    - Allow users to export transactions (CSV/JSON)
    - Generate spending reports (PDF)
    - Backup user data

18. **Additional Features**
    - Recurring transaction detection
    - Bill payment reminders
    - Savings goal tracking
    - Net worth calculation (if account balances available)
    - Multi-user support (family budgeting)

**Estimated Effort**: 8-10 focused sessions

---

## Quick Win to Get Started

**Goal**: See tangible progress in 1-2 hours

1. Uncomment line 11 in `src/moneyroundup/main.py`
2. Implement basic transaction fetching and storage
3. Create a simple daily email showing:
   - Total spent yesterday
   - Top 3 spending categories
   - Comparison to previous week
4. Test the email sends correctly

**This would make your app actually do its core job!**

---

## Technical Debt Inventory

### High Priority
- [ ] Database migrations system (Alembic)
- [ ] Remove hardcoded credentials
- [ ] Fix table drop/recreate on startup
- [ ] Background scheduler not running

### Medium Priority
- [ ] PostgreSQL migration
- [ ] Remove legacy UserOld model
- [ ] Fix mixed sync/async patterns
- [ ] API documentation
- [ ] Increase test coverage

### Low Priority
- [ ] Clean up unused imports
- [ ] Remove console.log statements
- [ ] Standardize error responses
- [ ] Code formatting/linting setup

---

## Architecture Decisions to Consider

### Transaction Storage
- **Option A**: Store all transactions locally (better for analysis, more storage)
- **Option B**: Query Plaid API on-demand (less storage, potential API limits)
- **Recommendation**: Hybrid - store recent transactions, query on-demand for history

### Advice Generation
- **Option A**: Rule-based system (simpler, more predictable)
- **Option B**: Machine learning (more sophisticated, requires training data)
- **Recommendation**: Start with rules, add ML later if needed

### Email Frequency
- **Current**: Daily digest
- **Consider**: Weekly summary option, instant alerts for large transactions
- **Recommendation**: Make frequency configurable per user

### Goal Types
- **Simple**: Monthly spending limits by category
- **Advanced**: Savings goals, debt payoff plans, net worth targets
- **Recommendation**: Start simple, expand based on user feedback

---

## Success Metrics

Define what "done" looks like for this side project:

### MVP Success Criteria
- [ ] User can register and verify email
- [ ] User can link bank account via Plaid
- [ ] Daily email sends automatically with spending summary
- [ ] User can set spending goals by category
- [ ] User receives advice comparing actual vs. goals

### Production Ready Criteria
- [ ] All data persisted in PostgreSQL
- [ ] Database migrations working
- [ ] No hardcoded credentials
- [ ] >70% test coverage
- [ ] API documentation complete
- [ ] Deployed to AWS Beanstalk

### Stretch Goals
- [ ] 10+ active users
- [ ] Google OAuth enabled
- [ ] Mobile responsive
- [ ] Data visualizations
- [ ] User testimonials/feedback

---

## Resources & References

### Documentation
- [Plaid API Docs](https://plaid.com/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/)
- [React Plaid Link](https://github.com/plaid/react-plaid-link)

### Current Commit State
- Last analyzed commit: `3ecf183` - "can now send email from SES"
- Goals feature commit: `e8080ea` - "Goal CRUD" (partially implemented, removed)

### Environment Variables Needed
```
# Database
DATABASE_URL=postgresql://...

# Plaid
PLAID_CLIENT_ID=
PLAID_SECRET=
PLAID_ENV=sandbox

# AWS
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=

# Email
EMAIL_FROM=
SMTP_HOST= (for dev)
SMTP_USER=
SMTP_PASSWORD=

# Auth
SECRET= (JWT secret)
VERIFICATION_TOKEN_SECRET=
RESET_PASSWORD_TOKEN_SECRET=

# OAuth (optional)
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=
```

---

## Notes & Observations

### Strengths of Current Implementation
- Modern async architecture (FastAPI + aiosqlite)
- Secure bank linking via Plaid
- Clean separation of concerns (routers, models, services)
- Docker containerization
- Dual email service (dev/prod)

### Key Insights
1. The hardest parts (auth, bank integration) are already done
2. Missing piece is the "intelligence layer" - turning transactions into insights
3. Infrastructure is solid, needs business logic implementation
4. Security posture needs improvement before public launch
5. Database persistence is fragile without migrations

### Questions to Answer
- How many days of transaction history to store?
- What spending categories to track?
- How to handle multiple bank accounts per user?
- What advice algorithms to implement?
- Should users be able to customize email frequency?

---

## Next Session Checklist

When you're ready to work on this project, start here:

1. [ ] Review this plan and prioritize features
2. [ ] Set up local development environment
3. [ ] Enable background scheduler (quick win!)
4. [ ] Create Transaction model and migration
5. [ ] Implement basic transaction fetching
6. [ ] Test daily email sends correctly
7. [ ] Commit and push progress

**Remember**: Done is better than perfect. Get the MVP working first, then iterate!

---

*This plan is a living document. Update it as you make progress and priorities shift.*

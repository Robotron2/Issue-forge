# Issue #1 — chore: PostgreSQL & Prisma Foundation

## Description

Integrate a PostgreSQL database connection into the PadiPay Relayer API using the Prisma ORM. This is the foundational prerequisite for all Phase 2 features and data modeling.

---

## Requirements & Context

- Add Prisma CLI and Prisma Client dependencies.
- Setup the base `schema.prisma` file.
- Configure `.env` database connection strings.
- Implement Zod validation for database environment variables in the existing configuration module to ensure fail-fast behavior if the DB URL is missing.

---

## Suggested Execution

```bash
git checkout -b chore/prisma-foundation
```

---

## Suggested Commit Message

```text
chore: configure postgresql and prisma foundation
```

---

## Definition of Done

- [ ] Prisma CLI and Client are installed.
- [ ] `schema.prisma` is initialized.
- [ ] Database environment variables are strictly validated by Zod at application startup.

<br><br>

# Issue #2 — feat: Core Identity Data Models

## Description

Design the database schema for the `User` entity and its strictly associated models, representing the core identity in the PadiPay ecosystem.

---

## Requirements & Context

- **Dependencies:** Issue #1
- Define the `User` model in the Prisma schema.
- Define a `Role` enum with options: `USER`, `ADMIN`, `MEDIATOR`.
- Define a `Wallet` model mapping 1:1 to the User. This model stores provider metadata (e.g., provider public addresses, IDs) but zero private keys.
- Run the initial database migration.

---

## Suggested Execution

```bash
git checkout -b feat/core-identity-models
```

---

## Suggested Commit Message

```text
feat: define user, role, and wallet database schemas
```

---

## Definition of Done

- [ ] `User`, `Role`, and `Wallet` models are defined in `schema.prisma`.
- [ ] Database migration is successfully generated and applied.

<br><br>

# Issue #3 — feat: Escrow Orchestration Data Models

## Description

Build the off-chain database representation for tracking user intent regarding Escrows. This allows the backend to track intent, associate buyers and sellers, and bridge web2 state with on-chain Soroban EscrowIds.

---

## Requirements & Context

- **Dependencies:** Issue #1
- Define an `EscrowIntent` model to bridge off-chain Web2 state with the on-chain `EscrowId`.
- Fields should include buyer reference, seller reference, amount, status, and the nullable `EscrowId` used by the Soroban smart contract.
- Run the database migration.

---

## Suggested Execution

```bash
git checkout -b feat/escrow-orchestration-models
```

---

## Suggested Commit Message

```text
feat: define escrow intent database schema
```

---

## Definition of Done

- [ ] `EscrowIntent` model is defined in `schema.prisma`.
- [ ] Database migration is successfully generated and applied.

<br><br>

# Issue #4 — feat: Data Access Layer

## Description

Establish the application's Data Access Layer by creating a centralized Prisma client singleton and dependency-injected repositories.

---

## Requirements & Context

- **Dependencies:** Issue #2, Issue #3
- Scaffold the Prisma client singleton to prevent connection leaks.
- Implement Dependency Injected repositories: `UserRepository`, `WalletRepository`, and `EscrowIntentRepository`.
- Ensure these repositories align with the existing DI patterns used in the `escrow.service.js`.

---

## Suggested Execution

```bash
git checkout -b feat/data-access-layer
```

---

## Suggested Commit Message

```text
feat: implement data access layer and repositories
```

---

## Definition of Done

- [ ] Prisma singleton instance is created.
- [ ] `UserRepository`, `WalletRepository`, and `EscrowIntentRepository` are implemented and injectable.

<br><br>

# Issue #5 — feat: Password Security & Core Auth Endpoints

## Description

Secure the backend API by implementing standard email and password authentication endpoints alongside secure password hashing.

---

## Requirements & Context

- **Dependencies:** Issue #4
- Implement a robust password hashing service (e.g., using bcrypt).
- Build the Email & Password Registration endpoint.
- Build the Email & Password Login endpoint.
- Ensure Zod validation on incoming auth payloads.

---

## Suggested Execution

```bash
git checkout -b feat/core-auth-endpoints
```

---

## Suggested Commit Message

```text
feat: implement password hashing and core auth endpoints
```

---

## Definition of Done

- [ ] Registration endpoint securely hashes passwords before DB insertion.
- [ ] Login endpoint validates credentials and returns a success payload.

<br><br>

# Issue #6 — feat: JWT Authorization

## Description

Implement JSON Web Token (JWT) issuing and verification to protect sensitive API routes.

---

## Requirements & Context

- **Dependencies:** Issue #5
- Implement a JWT issuance service.
- Add JWT secret configuration to Zod validation in `env.config.js`.
- Build an Express middleware to extract and verify JWTs on protected routes.
- Update the login endpoint to return the signed JWT.

---

## Suggested Execution

```bash
git checkout -b feat/jwt-authorization
```

---

## Suggested Commit Message

```text
feat: implement jwt authorization middleware and issuance
```

---

## Definition of Done

- [ ] JWT issuance service is functional.
- [ ] Login endpoint returns a valid token.
- [ ] Authorization middleware successfully protects and denies access to routes based on token validity.

<br><br>

# Issue #7 — feat: Google Sign-In

## Description

Expand the authentication layer to support OAuth (Google Sign-In), reducing onboarding friction for users.

---

## Requirements & Context

- **Dependencies:** Issue #6
- Integrate Google OAuth token verification service (verifying idTokens provided by clients).
- Build a Google Auth endpoint that handles a hybrid Register/Login flow.
- The flow must resolve to the same JWT system used by standard email logins.

---

## Suggested Execution

```bash
git checkout -b feat/google-sign-in
```

---

## Suggested Commit Message

```text
feat: implement google sign-in verification and auth flow
```

---

## Definition of Done

- [ ] Valid Google tokens allow a user to register or log in.
- [ ] A signed PadiPay JWT is returned upon successful OAuth verification.

<br><br>

# Issue #8 — feat: Password Recovery

## Description

Implement a standard password recovery flow allowing users to securely regain access to their accounts.

---

## Requirements & Context

- **Dependencies:** Issue #5
- Implement password reset token generation and secure DB storage.
- Build a "Forgot Password" token request endpoint.
- Build a "Reset Password" confirmation endpoint that accepts the token and updates the password hash.

---

## Suggested Execution

```bash
git checkout -b feat/password-recovery
```

---

## Suggested Commit Message

```text
feat: implement password recovery and reset flow
```

---

## Definition of Done

- [ ] Reset tokens are securely generated and persisted.
- [ ] Password reset endpoint properly invalidates tokens and updates credentials.

<br><br>

# Issue #9 — feat: User Profile APIs

## Description

Create the RESTful API endpoints for authenticated users to manage their core profiles.

---

## Requirements & Context

- **Dependencies:** Issue #6
- Build `GET /api/users/me` (returning secured Profile details and user roles).
- Build `PATCH /api/users/me` (allowing basic user account updates).
- Protect these endpoints using the JWT authorization middleware.

---

## Suggested Execution

```bash
git checkout -b feat/user-profile-apis
```

---

## Suggested Commit Message

```text
feat: implement user profile retrieval and update endpoints
```

---

## Definition of Done

- [ ] Authenticated users can retrieve their profiles.
- [ ] Authenticated users can apply valid updates to their profile.
- [ ] Unauthenticated requests are blocked.

<br><br>

# Issue #10 — feat: Account APIs

## Description

Provide an endpoint for retrieving top-level account status, separating logical account properties from personal user profile details.

---

## Requirements & Context

- **Dependencies:** Issue #6
- Build `GET /api/accounts/me` (returning general account information and status flags).
- Protect this endpoint using the JWT authorization middleware.

---

## Suggested Execution

```bash
git checkout -b feat/account-apis
```

---

## Suggested Commit Message

```text
feat: implement account retrieval endpoint
```

---

## Definition of Done

- [ ] Authenticated users can retrieve their account status successfully.

<br><br>

# Issue #11 — feat: Embedded Provider Abstraction

## Description

Create generic architectural abstractions for embedded wallet provisioning, ensuring the backend is strictly decoupled from specific third-party wallet SDKs.

---

## Requirements & Context

- **Dependencies:** Issue #4
- Define a generic Wallet Provider Interface.
- Implement Wallet Provider Adapter and Wallet Provider Service abstractions.
- Ensure the abstractions support the provisioning and querying of managed wallets without storing private keys.

---

## Suggested Execution

```bash
git checkout -b feat/wallet-provider-abstraction
```

---

## Suggested Commit Message

```text
feat: implement generic wallet provider adapter and interfaces
```

---

## Definition of Done

- [ ] Wallet provider interface is defined.
- [ ] Dependency injection configuration accepts the new wallet provider service.

<br><br>

# Issue #12 — feat: Automated Provisioning Flow

## Description

Hook the wallet creation mechanics seamlessly into the authentication pipeline so users instantly receive a managed wallet upon signing up.

---

## Requirements & Context

- **Dependencies:** Issue #5, Issue #7, Issue #11
- Wire the generic wallet creation service strictly into the User Registration pipeline.
- This must cover both the Email registration path and the Google OAuth registration path.
- Record the generated wallet metadata strictly via the `WalletRepository`.

---

## Suggested Execution

```bash
git checkout -b feat/automated-wallet-provisioning
```

---

## Suggested Commit Message

```text
feat: automate wallet provisioning during user registration
```

---

## Definition of Done

- [ ] Successful registration via email creates a linked `Wallet` record.
- [ ] Successful registration via Google creates a linked `Wallet` record.

<br><br>

# Issue #13 — feat: Wallet Details APIs

## Description

Provide RESTful API endpoints enabling authenticated users to fetch information about their automatically managed wallets.

---

## Requirements & Context

- **Dependencies:** Issue #12
- Build `GET /api/wallets/me`.
- The endpoint must return the managed wallet metadata and public Stellar addresses provided by the generic provider interface.
- Ensure the endpoint is protected by JWT authorization.

---

## Suggested Execution

```bash
git checkout -b feat/wallet-details-apis
```

---

## Suggested Commit Message

```text
feat: implement wallet details retrieval endpoint
```

---

## Definition of Done

- [ ] Authenticated users can retrieve their wallet public address and metadata.

<br><br>

# Issue #14 — feat: Funding Mechanics

## Description

Build the API endpoint allowing users to initiate funding to their managed wallet, bridging external liquidity into the PadiPay ecosystem.

---

## Requirements & Context

- **Dependencies:** Issue #11
- Build an endpoint to initiate managed wallet funding (utilizing the generic funding abstraction).
- This will likely interact with Testnet faucets or generic provider abstractions.
- Ensure strict Zod validation on any funding payloads.

---

## Suggested Execution

```bash
git checkout -b feat/funding-mechanics
```

---

## Suggested Commit Message

```text
feat: implement managed wallet funding endpoint
```

---

## Definition of Done

- [ ] Authenticated users can successfully invoke the funding endpoint to top up their managed wallet balances.

<br><br>

# Issue #15 — feat: Withdrawal Mechanics

## Description

Enable users to extract their funds by initiating a withdrawal from their managed wallet to an external Stellar address.

---

## Requirements & Context

- **Dependencies:** Issue #11
- Build an endpoint for withdrawing USDC from the managed wallet to an external Stellar address.
- Implement pre-flight balance validation logic prior to withdrawal execution to prevent over-drafting.
- Validate destination addresses strictly using the Stellar SDK.

---

## Suggested Execution

```bash
git checkout -b feat/withdrawal-mechanics
```

---

## Suggested Commit Message

```text
feat: implement usdc withdrawal mechanics and balance validation
```

---

## Definition of Done

- [ ] Withdrawal endpoint correctly validates external addresses and available balances.
- [ ] Withdrawal requests successfully invoke the generic provider abstraction.

<br><br>

# Issue #16 — feat: Escrow Funding Orchestration

## Description

Bridge the user's managed wallet with the escrow creation process, allowing a buyer to fund a new escrow directly from their managed balance.

---

## Requirements & Context

- **Dependencies:** Issue #11, Issue #14
- Build an endpoint to fund a specific Escrow (tracked via `EscrowIntent`) using the user's managed wallet balance.
- Verify the user possesses adequate funds before executing the escrow funding transaction.

---

## Suggested Execution

```bash
git checkout -b feat/escrow-funding-orchestration
```

---

## Suggested Commit Message

```text
feat: implement escrow funding endpoint using managed wallets
```

---

## Definition of Done

- [ ] Escrows can be seamlessly funded by withdrawing directly from the user's managed wallet provider abstraction.

<br><br>

# Issue #17 — feat: Intent Tracking Endpoints

## Description

Connect the placeholder escrow endpoints to the new database models, enabling stateful tracking of off-chain Web2 intent.

---

## Requirements & Context

- **Dependencies:** Issue #4
- Wire the existing placeholder `/submit-escrow` route to create `EscrowIntent` DB records before building Soroban transactions.
- Implement Zod validation to ensure buyer and seller references exist and are valid.

---

## Suggested Execution

```bash
git checkout -b feat/intent-tracking-endpoints
```

---

## Suggested Commit Message

```text
feat: wire submit-escrow endpoint to intent tracking database
```

---

## Definition of Done

- [ ] Invoking `/submit-escrow` successfully creates a trackable `EscrowIntent` in the database.

<br><br>

# Issue #18 — feat: On-Chain Synchronization

## Description

Complete the escrow orchestration loop by linking the off-chain `EscrowIntent` records to the resulting on-chain Soroban `EscrowId`.

---

## Requirements & Context

- **Dependencies:** Issue #17
- Build a synchronization service/webhook handler to update the `EscrowIntent` DB status upon successful Stellar transaction completion.
- Specifically, the off-chain `EscrowIntent` must be updated to store the on-chain `EscrowId` so future actions (release/refund) can be correctly routed to the blockchain.

---

## Suggested Execution

```bash
git checkout -b feat/on-chain-synchronization
```

---

## Suggested Commit Message

```text
feat: implement on-chain synchronization for escrow intents
```

---

## Definition of Done

- [ ] Successful transaction submissions correctly update the corresponding `EscrowIntent` record with the blockchain `EscrowId` and confirmed status.

<br><br>
## Testing

# Issue #19 — test: Prisma Database Integration Test Framework

## Description

Establish a robust testing framework for Prisma to ensure that database integration tests do not pollute the primary development database or interfere with each other during concurrent execution.

---

## Requirements & Context

- Configure a separate test database or in-memory SQLite equivalent specifically for Jest integration tests.
- Create global setup and teardown hooks to migrate the test schema before tests and drop it afterward.
- Implement a utility to truncate tables between individual test cases, ensuring test isolation.

---

## Suggested Execution

```bash
git checkout -b test/prisma-integration-framework
```

---

## Suggested Commit Message

```text
test: setup prisma test database and teardown utilities
```

---

## Definition of Done

- [ ] A dedicated test database environment is configured.
- [ ] Setup and teardown hooks execute reliably via Jest.
- [ ] Database state is cleanly reset between individual test runs.

<br><br>

# Issue #20 — test: Data Access Layer Integration Tests

## Description

Ensure the integrity of the Data Access Layer by writing integration tests for the Prisma Repositories.

---

## Requirements & Context

- Requires Issue #19 to be complete.
- Write tests for `UserRepository`, `WalletRepository`, and `EscrowIntentRepository`.
- Verify complex queries, relations (e.g. User to Wallet), and cascading behaviors work exactly as expected against a real test database.

---

## Suggested Execution

```bash
git checkout -b test/data-access-repositories
```

---

## Suggested Commit Message

```text
test: implement integration tests for prisma repositories
```

---

## Definition of Done

- [ ] Integration tests exist for all methods on the primary repositories.
- [ ] Tests execute against the Prisma test database successfully.

<br><br>

# Issue #21 — test: Authentication Flow Contract Tests

## Description

Secure the login and registration flows by implementing comprehensive contract and integration tests to prevent authentication regressions.

---

## Requirements & Context

- Write Supertest-based HTTP contract tests for the Registration, Login, and Google Auth endpoints.
- Test edge cases: Duplicate emails, invalid passwords, malformed Google OAuth tokens, and missing fields.
- Verify password hashes are never exposed in the response payload.

---

## Suggested Execution

```bash
git checkout -b test/authentication-flows
```

---

## Suggested Commit Message

```text
test: implement contract tests for authentication endpoints
```

---

## Definition of Done

- [ ] All success and failure paths for registration and login are covered.
- [ ] Edge cases trigger the correct Zod validation errors.

<br><br>

# Issue #22 — test: JWT Authorization Middleware Isolation

## Description

Validate the integrity of the route protection mechanism by writing isolated unit and integration tests for the JWT middleware.

---

## Requirements & Context

- Write unit tests verifying that the middleware correctly blocks expired, malformed, or missing tokens.
- Write tests verifying that valid tokens correctly extract user identities and attach them to the Express `req` object.

---

## Suggested Execution

```bash
git checkout -b test/jwt-middleware
```

---

## Suggested Commit Message

```text
test: add isolated unit tests for jwt authorization middleware
```

---

## Definition of Done

- [ ] JWT middleware correctly rejects unauthorized requests with a 401.
- [ ] JWT middleware correctly permits authorized requests.

<br><br>

# Issue #23 — test: Wallet Provider Abstraction Mock Tests

## Description

Ensure the generic Wallet Provider Abstraction gracefully handles failures without actually hitting third-party APIs during test execution.

---

## Requirements & Context

- Implement a robust Mock adapter for the generic Wallet Provider interface.
- Write unit tests verifying that the service correctly handles provider timeouts, 500 errors, and invalid provisioning responses.
- Verify that automated wallet provisioning fails gracefully during registration if the provider is down.

---

## Suggested Execution

```bash
git checkout -b test/wallet-provider-mocks
```

---

## Suggested Commit Message

```text
test: implement mock adapter and tests for wallet provider abstraction
```

---

## Definition of Done

- [ ] Mock adapter is available for dependency injection during tests.
- [ ] Error handling paths for provider failures are fully covered.

<br><br>

# Issue #24 — test: USDC Operations Integration Tests

## Description

Prevent financial regressions by ensuring the USDC funding and withdrawal endpoints correctly enforce business logic.

---

## Requirements & Context

- Write integration tests for the Funding and Withdrawal API routes.
- Utilize the mock wallet provider to simulate sufficient and insufficient balance scenarios.
- Verify that withdrawals gracefully fail when external Stellar addresses are invalid.

---

## Suggested Execution

```bash
git checkout -b test/usdc-operations
```

---

## Suggested Commit Message

```text
test: add integration tests for usdc funding and withdrawal flows
```

---

## Definition of Done

- [ ] Funding mechanics are thoroughly tested.
- [ ] Withdrawal mechanics successfully block over-drafting and invalid addresses.

<br><br>

# Issue #25 — test: Escrow Orchestration Integration Tests

## Description

Verify the bridge between off-chain user intent and on-chain Escrow IDs.

---

## Requirements & Context

- Test the `/submit-escrow` route's ability to create an off-chain `EscrowIntent` database record.
- Write a test verifying that the On-Chain Synchronization service successfully updates the `EscrowIntent` record with the final `EscrowId` once a transaction completes.

---

## Suggested Execution

```bash
git checkout -b test/escrow-orchestration
```

---

## Suggested Commit Message

```text
test: add integration tests for escrow orchestration endpoints
```

---

## Definition of Done

- [ ] Intent tracking logic is covered.
- [ ] On-chain synchronization logic correctly mutates database state.

<br><br>

# Issue #26 — test: End-to-End Backend Journey

## Description

Create a holistic End-to-End (E2E) test simulating a complete user journey through the backend to ensure the entire dependency injection tree is wired correctly.

---

## Requirements & Context

- Test the full flow: Register User -> Generate JWT -> Fetch Profile -> Fetch Wallet -> Submit Escrow Intent.
- This test should run against an ephemeral test database and utilize mock wallet providers, confirming that no middleware, validation, or dependency injection links are broken in a production-like environment.

---

## Suggested Execution

```bash
git checkout -b test/e2e-backend-journey
```

---

## Suggested Commit Message

```text
test: implement e2e backend user journey test
```

---

## Definition of Done

- [ ] E2E test runs successfully as part of the test suite.
- [ ] Modifying one component in the chain correctly triggers an E2E failure.

<br><br>

## Documentation

# Issue #27 — docs: Phase 2 API Reference

## Description

Create comprehensive API documentation for the new authentication, wallet, and escrow endpoints introduced in Phase 2.

---

## Requirements & Context

- Document the new routes (`/api/auth/*`, `/api/users/*`, `/api/wallets/*`) using a standard format (e.g., Swagger/OpenAPI or detailed Markdown in the `docs/` folder).
- Include request payloads, expected responses, JWT requirements, and error codes.

---

## Suggested Execution

```bash
git checkout -b docs/api-reference
```

---

## Suggested Commit Message

```text
docs: create phase 2 api reference documentation
```

---

## Definition of Done

- [ ] API documentation accurately reflects the implemented Phase 2 routes.
- [ ] Example JSON payloads are provided.

<br><br>

# Issue #28 — docs: Wallet Provider Integration Guide

## Description

Document the Generic Wallet Provider Architecture to ensure future contributors know exactly how to integrate concrete providers (like Privy or Turnkey) when the time comes.

---

## Requirements & Context

- Write a markdown guide explaining the Wallet Provider Interface.
- Provide a step-by-step example of how to implement a new Provider Adapter and inject it into the service container.

---

## Suggested Execution

```bash
git checkout -b docs/wallet-provider-guide
```

---

## Suggested Commit Message

```text
docs: create wallet provider adapter integration guide
```

---

## Definition of Done

- [ ] `docs/wallet-provider-guide.md` is published and linked in the README.

<br><br>

# Issue #29 — docs: Database Schema and ERD Documentation

## Description

Provide visual and textual documentation of the Prisma database schema so contributors can quickly understand the data architecture.

---

## Requirements & Context

- Generate or manually create an Entity Relationship Diagram (ERD) showing the relationship between Users, Roles, Wallets, and EscrowIntents.
- Document the constraints and uniqueness guarantees of the schema.

---

## Suggested Execution

```bash
git checkout -b docs/database-schema
```

---

## Suggested Commit Message

```text
docs: add database schema erd and relationships documentation
```

---

## Definition of Done

- [ ] An ERD is generated and embedded in the docs.
- [ ] Relationships and cascading rules are clearly explained.

<br><br>

# Issue #30 — docs: Backend Onboarding & Environment Guide

## Description

Update the project onboarding guides to reflect the new requirements for setting up the local development environment.

---

## Requirements & Context

- Update `docs/setup-guide.md` to include instructions for spinning up local PostgreSQL (e.g., via Docker Compose).
- Document how to run Prisma migrations and seed the database for local testing.

---

## Suggested Execution

```bash
git checkout -b docs/onboarding-updates
```

---

## Suggested Commit Message

```text
docs: update setup guide for postgres and prisma environment
```

---

## Definition of Done

- [ ] Local setup instructions accurately reflect the Phase 2 architecture.
- [ ] Instructions for `npx prisma db push` or migrations are included.

<br><br>

## Refactoring & Security Hardening

# Issue #31 — refactor: Implement Rate Limiting Middleware

## Description

Protect the application from brute-force attacks and abuse by implementing strict rate limiting on public-facing and authentication endpoints.

---

## Requirements & Context

- Integrate `express-rate-limit` or a similar robust mechanism.
- Apply strict limits to `/api/auth/register`, `/api/auth/login`, and `/api/auth/recover`.
- Apply broader limits to authenticated API routes.

---

## Suggested Execution

```bash
git checkout -b refactor/rate-limiting
```

---

## Suggested Commit Message

```text
refactor: implement rate limiting middleware for api endpoints
```

---

## Definition of Done

- [ ] Authentication endpoints are strictly rate-limited.
- [ ] Rate limit violations return a standardized 429 Too Many Requests response.

<br><br>

# Issue #32 — refactor: Secure Data Serialization (Response Stripping)

## Description

Ensure sensitive data (like password hashes or internal database IDs) never accidentally leaks to the client via API responses.

---

## Requirements & Context

- Implement a serialization utility or Prisma extension to automatically strip sensitive fields (e.g., `passwordHash`) from User objects before returning them to the controller.
- Apply this utility to all User Profile and Account endpoints.

---

## Suggested Execution

```bash
git checkout -b refactor/secure-serialization
```

---

## Suggested Commit Message

```text
refactor: implement secure data serialization utility for user responses
```

---

## Definition of Done

- [ ] `passwordHash` is provably stripped from all API responses.
- [ ] Utility is reusable for future sensitive data models.

<br><br>

# Issue #33 — refactor: Request Correlation IDs

## Description

Improve the traceability of requests as they travel through the backend architecture by attaching a unique Correlation ID to every incoming request.

---

## Requirements & Context

- Implement an Express middleware that generates a unique UUID (or extracts an existing header like `X-Correlation-ID`) for every request.
- Attach this ID to the Express `req` object and ensure it is included in all error logs and standardized responses.

---

## Suggested Execution

```bash
git checkout -b refactor/correlation-ids
```

---

## Suggested Commit Message

```text
refactor: implement request correlation ids for traceability
```

---

## Definition of Done

- [ ] Correlation IDs are generated and attached to all requests.
- [ ] Centralized error handler logs the Correlation ID alongside error details.

<br><br>

# Issue #34 — refactor: HTTP Security Headers

## Description

Harden the Express application against common web vulnerabilities by configuring secure HTTP headers.

---

## Requirements & Context

- Integrate and configure the `helmet` middleware.
- Configure strict Content Security Policies, HSTS, and prevent MIME-type sniffing.
- Ensure CORS is strictly configured to only allow the official PadiPay frontend domains.

---

## Suggested Execution

```bash
git checkout -b refactor/security-headers
```

---

## Suggested Commit Message

```text
refactor: configure helmet and strict cors policies
```

---

## Definition of Done

- [ ] `helmet` is installed and registered globally.
- [ ] CORS is restricted to validated origins.

<br><br>

# Issue #35 — refactor: Standardize Audit Logging

## Description

Implement immutable audit logs for highly sensitive business actions to ensure security and compliance observability.

---

## Requirements & Context

- Abstract a lightweight Audit Logging service.
- Hook this service into critical pathways: Registration, Failed Logins, Escrow Intent Creation, and USDC Withdrawals.
- Output these logs in a structured format distinct from standard application debug logs.

---

## Suggested Execution

```bash
git checkout -b refactor/audit-logging
```

---

## Suggested Commit Message

```text
refactor: abstract and implement standardized audit logging
```

---

## Definition of Done

- [ ] Audit logs are generated for critical security and financial actions.
- [ ] Audit service is injected properly into controllers or core services.

<br><br>

## DevOps & Engineering Quality

# Issue #36 — ci: Automated Dependency Vulnerability Scanning

## Description

Protect the application from supply chain attacks by automating dependency auditing.

---

## Requirements & Context

- Configure GitHub Actions to run `npm audit` or utilize an external tool (like Dependabot or Snyk) on all pull requests.
- Fail the CI build if High or Critical vulnerabilities are introduced.

---

## Suggested Execution

```bash
git checkout -b ci/vulnerability-scanning
```

---

## Suggested Commit Message

```text
ci: automate dependency vulnerability scanning in github actions
```

---

## Definition of Done

- [ ] Vulnerability scans execute automatically on PRs.
- [ ] Build fails on critical severity alerts.

<br><br>

# Issue #37 — ci: Code Coverage Reporting

## Description

Enforce code quality standards by visualizing test coverage and failing builds that drop below required thresholds.

---

## Requirements & Context

- Update the existing CI pipeline to generate Jest coverage reports.
- Enforce the 80% coverage threshold configured in `package.json` by failing the GitHub Action step if coverage drops.
- Optionally integrate a visualization tool like Codecov.

---

## Suggested Execution

```bash
git checkout -b ci/code-coverage
```

---

## Suggested Commit Message

```text
ci: integrate coverage reporting and enforce thresholds
```

---

## Definition of Done

- [ ] CI pipeline fails if Jest coverage drops below required minimums.
- [ ] Coverage reports are generated as CI artifacts.

<br><br>

# Issue #38 — ci: Optimize Docker Build

## Description

Improve deployment times and security by optimizing the existing `Dockerfile` for a production Node.js environment.

---

## Requirements & Context

- Implement multi-stage builds to exclude development dependencies from the final image.
- Ensure the application runs as an unprivileged, non-root user within the container.
- Optimize layer caching to speed up consecutive builds.

---

## Suggested Execution

```bash
git checkout -b ci/docker-optimization
```

---

## Suggested Commit Message

```text
ci: optimize dockerfile for production sizes and security
```

---

## Definition of Done

- [ ] Dockerfile utilizes a multi-stage build.
- [ ] Production container runs as a non-root user.
- [ ] Resulting image size is significantly reduced.

<br><br>

# Issue #39 — chore: Setup Structured JSON Logging

## Description

Replace standard `console.log` statements with a high-performance, structured JSON logger to improve observability in production environments.

---

## Requirements & Context

- Integrate a logging library such as Pino or Winston.
- Replace all existing `console.error` and `console.log` statements across the application.
- Ensure the logger formats logs as JSON in production but remains human-readable in local development.

---

## Suggested Execution

```bash
git checkout -b chore/structured-logging
```

---

## Suggested Commit Message

```text
chore: implement structured json logging across application
```

---

## Definition of Done

- [ ] Pino or Winston is installed and configured.
- [ ] Centralized error handler and boot sequences use the new structured logger.

<br><br>

# Issue #40 — feat: Advanced Health Check Endpoint

## Description

Enhance the basic scaffolded health check to verify downstream dependency connectivity, ensuring container orchestration systems (like Kubernetes) can accurately assess readiness.

---

## Requirements & Context

- Update the `/health` endpoint to query the Prisma Database connection.
- Verify connectivity to the Stellar RPC node.
- Return a detailed JSON payload detailing the health of these downstream dependencies, and return a 503 HTTP status if any critical dependency is offline.

---

## Suggested Execution

```bash
git checkout -b feat/advanced-health-check
```

---

## Suggested Commit Message

```text
feat: implement advanced health check verifying database and rpc connectivity
```

---

## Definition of Done

- [ ] Health endpoint accurately reflects Prisma database connectivity.
- [ ] Health endpoint accurately reflects Stellar RPC connectivity.
- [ ] HTTP 503 is returned if readiness conditions are unmet.
